data "aws_secretsmanager_secret_version" "secrets" {
    secret_id = "prod/the_internets/secrets"
}