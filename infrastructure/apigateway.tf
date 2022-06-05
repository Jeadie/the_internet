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