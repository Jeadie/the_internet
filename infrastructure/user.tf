
resource "aws_cognito_user_pool" "onceaday_users" {
  name = "onceaday_users"
  
  alias_attributes = ["email"]
  auto_verified_attributes = ["email"]

  username_configuration {
    case_sensitive = false
  }
  verification_message_template {
    email_message = "You'll need this {####}."
    default_email_option = "CONFIRM_WITH_CODE"    
    email_subject = "Please verify your onceaday.fyi account"
  }

  # email_configuration {
  #   from_email_address = "robots@onceaday.link"
  # }

  schema {
      attribute_data_type      = "String"
      developer_only_attribute = false
      mutable                  = false
      name                     = "subscription_type"
      required                 = false
  }

  account_recovery_setting {
    recovery_mechanism {
      name     = "verified_email"
      priority = 1
    }
  }
}

resource "aws_cognito_user_pool_client" "onceaday_webapp" {
  name = "onceaday_webapp"

  user_pool_id = aws_cognito_user_pool.onceaday_users.id
  // JS SDK does not support client secrets
  //  https://github.com/aws-amplify/amplify-js/tree/main/packages/amazon-cognito-identity-js#configuration
  generate_secret = false
}

resource "aws_cognito_user_group" "free_user_group" {
    name = "free_user_group"
    description = "Users who are on the free subscription."

    user_pool_id = aws_cognito_user_pool.onceaday_users.id
    # role_arn = 
}

resource "aws_cognito_user_group" "premium_user_group" {
    name = "premium_user_group"
    description = "Users who are on paid subscription."

    user_pool_id = aws_cognito_user_pool.onceaday_users.id
    # role_arn = 
}

resource "aws_cognito_user" "me" {
  user_pool_id = aws_cognito_user_pool.onceaday_users.id
  username     = "jackeadie"
  password = var.cognito_password
  attributes = {
    email = "jackeadie@duck.com"
  }
}

resource "aws_cognito_user_in_group" "premium_me" {
  user_pool_id = aws_cognito_user_pool.onceaday_users.id
  group_name   = aws_cognito_user_group.premium_user_group.name
  username     = aws_cognito_user.me.username
}