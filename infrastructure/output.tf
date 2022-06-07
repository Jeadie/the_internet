output "api_url" {
  description = "Base URL for backend API Gateway "

  value = aws_apigatewayv2_stage.default_backend.invoke_url
}

# output "frontend_s3_bucket" {
#   description = "Where to upload the frontend."
#   value = aws_static_website.website_root_s3_bucket
# }