
variable "environment_stage" {
  description = "One of: LOCAL,BETA,PROD"
  default     = "LOCAL"
}

variable "cognito_password" {
  description = "Password of cognito user associated with premium user group"
  sensitive = true
}

variable "news_api_key" {
  description = "API key for the newsapi.org account"
  sensitive = true
}