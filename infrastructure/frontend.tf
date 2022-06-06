
# TODO: Use a better module, later
#  Module reference: https://registry.terraform.io/modules/cloudmaniac/static-website/aws/latest
module "aws_static_website" {
  source = "cloudmaniac/static-website/aws"

  # This is the domain as defined in Route53
  domains-zone-root       = "onceaday.link"

  # Domains used for CloudFront
  website-domain-main     = "onceaday.link"
  website-domain-redirect = "www.onceaday.link"

  # Don't redirect these domains to this static website (useful for beta.onceaday.link)
  website-additional-domains = [api.onceaday.link]
}