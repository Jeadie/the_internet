locals {
  internet_content_binary_filename = "internet_content_lambda"
}

// Lambda for internet_content Golang Lambda (source code in /lambda)
resource "aws_lambda_function" "internet_content" {
  filename      = data.archive_file.internet_content_zip.output_path
  function_name = "internet_content"
  role          = aws_iam_role.lambda_role.arn
  handler       = local.internet_content_binary_filename
  source_code_hash = filebase64sha256(data.archive_file.internet_content_zip.source_file)
  
  runtime          = "go1.x"

  environment {
    variables = {
      STAGE = var.environment_stage
    }
  }
}

// Use terraform to Zip the Golang binary
data "archive_file" "internet_content_zip" {
  type        = "zip"
  source_file = local.internet_content_binary_filename
  output_path = "${local.internet_content_binary_filename}.zip"
  
}

// IAM role for lambda
resource "aws_iam_role" "lambda_role" {
  name = "${local.internet_content_binary_filename}_iam_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
  
}

// Basic Lambda permissions
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

// Allow lambda to call `internet_content` DynamoDb
resource "aws_iam_role_policy" "dynamodb-lambda-policy" {
   name = "dynamodb_lambda_policy"
   role = aws_iam_role.lambda_role.id

   policy = jsonencode({
      "Version" : "2012-10-17",
      "Statement" : [
        {
           "Effect" : "Allow",
           "Action" : ["dynamodb:*"],
           "Resource" : "${aws_dynamodb_table.internet_content.arn}"
        }
      ]
   })
}
