
# TODO: Use a better module, later
# TODO: Need to add CORS policy to S3 bucket manually
#  Module reference: https://registry.terraform.io/modules/cloudmaniac/static-website/aws/latest
# module "aws_static_website" {
#   source = "cloudmaniac/static-website/aws"

#   # This is the domain as defined in Route53
#   domains-zone-root       = "onceaday.link"

#   # Domains used for CloudFront
#   website-domain-main     = "onceaday.link"
#   website-domain-redirect = "www.onceaday.link"

#   # Don't redirect these domains to this static website (useful for beta.onceaday.link)
#   website-additional-domains = ["api.onceaday.link"]
# }

provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
}

  terraform {
    required_providers {
      aws = {
        source  = "hashicorp/aws"
        version = "4.8.0"
        }
    }
  }

locals {
  # This is the domain as defined in Route53
  domains-zone-root       = "onceaday.link"

  # Domains used for CloudFront
  website-domain-main     = "onceaday.link"
  website-domain-redirect = "www.onceaday.link"
}
 
data "aws_route53_zone" "main" {
  name         = local.domains-zone-root
  private_zone = false
}

resource "aws_route53_record" "wildcard_validation" {
  for_each = {
    for dvo in aws_acm_certificate.wildcard_website.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }
  name            = each.value.name
  type            = each.value.type
  zone_id         = data.aws_route53_zone.main.zone_id
  records         = [each.value.record]
  allow_overwrite = true
  ttl             = "60"
}

resource "aws_acm_certificate_validation" "wildcard_cert" {
  provider                = aws.us-east-1
  certificate_arn         = aws_acm_certificate.wildcard_website.arn
  validation_record_fqdns = [for k, v in aws_route53_record.wildcard_validation : v.fqdn]
}

resource "aws_acm_certificate" "wildcard_website" {
  provider                  = aws.us-east-1
  domain_name               = local.domains-zone-root
  subject_alternative_names = ["*.${local.domains-zone-root}"]
  validation_method         = "DNS"

  tags = {
    ManagedBy = "terraform"
    Changed   = formatdate("YYYY-MM-DD hh:mm ZZZ", timestamp())
  }

  lifecycle {
    ignore_changes = [tags["Changed"]]
  }

}

# Get the ARN of the issued certificate
data "aws_acm_certificate" "wildcard_website" {
  provider = aws.us-east-1

  depends_on = [
    aws_acm_certificate.wildcard_website,
    aws_route53_record.wildcard_validation,
    aws_acm_certificate_validation.wildcard_cert,
  ]

  domain      = local.website-domain-main
  statuses    = ["ISSUED"]
  most_recent = true
}

resource "aws_s3_bucket_policy" "update_website_root_bucket_policy" {
  bucket = aws_s3_bucket.website_root.id

  policy = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "PolicyForWebsiteEndpointsPublicContent",
  "Statement": [
    {
      "Sid": "PublicRead",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "s3:GetObject"
      ],
      "Resource": [
        "${aws_s3_bucket.website_root.arn}/*",
        "${aws_s3_bucket.website_root.arn}"
      ]
    }
  ]
}
POLICY
}

resource "aws_s3_bucket_website_configuration" "website_root" {
  bucket = aws_s3_bucket.website_root.bucket

  index_document {
    suffix = "index.html"
  }

  error_document {
    key = "404.html"
  }
}

resource "aws_s3_bucket_acl" "website_root" {
  bucket = aws_s3_bucket.website_root.id
  acl    = "public-read"
}

resource "aws_s3_bucket_logging" "website_root" {
  bucket = aws_s3_bucket.website_root.id

  target_bucket = aws_s3_bucket.website_logs.id
  target_prefix = "${local.website-domain-main}/"
}

resource "aws_s3_bucket" "website_root" {
  bucket = "${local.website-domain-main}-root"

  force_destroy = true

  tags = {
    ManagedBy = "terraform"
    Changed   = formatdate("YYYY-MM-DD hh:mm ZZZ", timestamp())
  }

  lifecycle {
    ignore_changes = [tags["Changed"]]
  }
}

resource "aws_s3_bucket_cors_configuration" "website_root" {
  bucket = aws_s3_bucket.website_root.bucket

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}
resource "aws_s3_bucket_acl" "website_logs" {
  bucket = aws_s3_bucket.website_logs.id
  acl    = "log-delivery-write"

  depends_on = [
    aws_s3_bucket.website_logs
  ]
}

resource "aws_s3_bucket" "website_logs" {
  bucket = "${local.website-domain-main}-logs"

  force_destroy = true

  tags = {
    ManagedBy = "terraform"
    Changed   = formatdate("YYYY-MM-DD hh:mm ZZZ", timestamp())
  }

  lifecycle {
    ignore_changes = [tags["Changed"]]
  }
}

# resource "aws_cloudfront_cache_policy" "website_cache_policy" {
#   name = "${local.website-domain-main}-cache-policy"
#   comment = "cache policy cloudfront -> S3 ${local.website-domain-main}"
#   # allowed_headers

# }

resource "aws_cloudfront_distribution" "website_cdn_root" {
  enabled     = true
  price_class = "PriceClass_All"
  aliases = [local.website-domain-main]
  
  origin {
    origin_id   = "origin-bucket-${aws_s3_bucket.website_root.id}"
    domain_name = aws_s3_bucket.website_root.website_endpoint

    custom_origin_config {
      origin_protocol_policy = "http-only"
      http_port            = 80
      https_port           = 443
      origin_ssl_protocols = ["TLSv1.2", "TLSv1.1", "TLSv1"]
    }
  }

  default_root_object = "index.html"

  logging_config {
    bucket = aws_s3_bucket.website_logs.bucket_domain_name
    prefix = "${local.website-domain-main}/"
  }

  default_cache_behavior {
    allowed_methods  = ["GET", "HEAD", "OPTIONS"]
    cached_methods   = ["GET", "HEAD", "OPTIONS"]
    target_origin_id = "origin-bucket-${aws_s3_bucket.website_root.id}"
    min_ttl          = "0"
    default_ttl      = "300"
    max_ttl          = "1200"

    viewer_protocol_policy = "redirect-to-https" # Redirects any HTTP request to HTTPS
    compress               = true
    # cache_policy_id = aws_cloudfront_cache_policy.website_cache_policy.id

    forwarded_values {
      query_string = false
      cookies {
        forward = "none"
      }
      headers = [ "Origin", "Access-Control-Request-Headers", "Access-Control-Request-Method" ]
    }
  }

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  viewer_certificate {
    acm_certificate_arn = data.aws_acm_certificate.wildcard_website.arn
    ssl_support_method  = "sni-only"
  }

  custom_error_response {
    error_caching_min_ttl = 300
    error_code            = 404
    response_page_path    = "/404.html"
    response_code         = 404
  }

  tags = {
    ManagedBy = "terraform"
    Changed   = formatdate("YYYY-MM-DD hh:mm ZZZ", timestamp())
  }

  lifecycle {
    ignore_changes = [
      tags["Changed"],
      viewer_certificate,
    ]
  }
}

resource "aws_route53_record" "website_cdn_root_record" {
  zone_id = data.aws_route53_zone.main.zone_id
  name    = local.website-domain-main
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.website_cdn_root.domain_name
    zone_id                = aws_cloudfront_distribution.website_cdn_root.hosted_zone_id
    evaluate_target_health = false
  }
}