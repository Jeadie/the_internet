resource "aws_apigatewayv2_api" "backend" {
  name          = "backend"
  description   = "API for backend resources of the_internet" 
  
  protocol_type = "HTTP"

}

resource "aws_apigatewayv2_stage" "default_backend" {
  api_id = aws_apigatewayv2_api.backend.id

  name        = "default_backend_stage"
  auto_deploy = true

}

// Connect API gateway to `internet_content` lambda
resource "aws_apigatewayv2_integration" "internet_content_integration" {
  api_id = aws_apigatewayv2_api.backend.id

  integration_uri    = aws_lambda_function.internet_content.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "internet_content_get_route" {
  api_id = aws_apigatewayv2_api.backend.id

  route_key = "GET /api"
  target    = "integrations/${aws_apigatewayv2_integration.internet_content_integration.id}"
}

resource "aws_apigatewayv2_route" "internet_content_post_route" {
  api_id = aws_apigatewayv2_api.backend.id

  route_key = "POST /api"
  target    = "integrations/${aws_apigatewayv2_integration.internet_content_integration.id}"
}

// Permissions to allow API gateway to call Lambda
resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.internet_content.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.backend.execution_arn}/*/*"
}


// TODO: Get this certificate in terraform
resource "aws_apigatewayv2_domain_name" "api_domain" {
  domain_name     = "api.onceaday.link"

  domain_name_configuration {
    certificate_arn = "arn:aws:acm:us-east-1:383495223751:certificate/af929853-2e80-41c5-ad81-ca2dd8bd367a"
    endpoint_type = "REGIONAL"
    security_policy = "TLS_1_2"
  }

}

// TODO: get this hosted zone id in terraform
resource "aws_route53_record" "api_domain_record" {
  name    = aws_apigatewayv2_domain_name.api_domain.domain_name
  type    = "A"
  zone_id  = "Z102289216LD1O6ETDCYH"

  alias {
    name                   = aws_apigatewayv2_domain_name.api_domain.domain_name_configuration[0].target_domain_name
    zone_id                = aws_apigatewayv2_domain_name.api_domain.domain_name_configuration[0].hosted_zone_id
    evaluate_target_health = false
  }
}


resource "aws_apigatewayv2_api_mapping" "api_domain_to_gateway" {
  api_id      = aws_apigatewayv2_api.backend.id
  stage  = aws_apigatewayv2_stage.default_backend.id
  domain_name = aws_apigatewayv2_domain_name.api_domain.domain_name
}