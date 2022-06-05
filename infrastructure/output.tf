output "api_url" {
  description = "Base URL for backend API Gateway "

  value = aws_apigatewayv2_stage.default_backend.invoke_url
}