locals {
  scrape_cron_schedule = "cron(0 0 * * * *)" 
  lambda_name = "scraper.zip"
}

data "archive_file" "content_scraper_package" {  
  type = "zip"  
  source_dir = "../lambda/content/" 
  output_path = local.lambda_name
}

resource "aws_lambda_function" "content_scraper" {
    function_name = "content-scraper"
    filename      = local.lambda_name
    source_code_hash = data.archive_file.content_scraper_package.output_base64sha256
    role          = aws_iam_role.scraper_lambda_role.arn
    runtime       = "python3.9"
    handler       = "main.handler"
}

resource "aws_lambda_permission" "allow_cloudwatch_to_invoke" {
  function_name = aws_lambda_function.content_scraper.function_name
  statement_id = "CloudWatchInvoke"
  action = "lambda:InvokeFunction"

  source_arn = aws_cloudwatch_event_rule.web_scrape_cron_job.arn
  principal = "events.amazonaws.com"
}

resource "aws_cloudwatch_event_rule" "web_scrape_cron_job" {
  name = "web-scrape-cron-job"
  schedule_expression = "rate(50 minutes)"
}

resource "aws_cloudwatch_event_target" "invoke_lambda" {
  rule = aws_cloudwatch_event_rule.web_scrape_cron_job.name
  arn = aws_lambda_function.content_scraper.arn
}

resource "aws_iam_role" "scraper_lambda_role" {
  name = "${local.internet_content_binary_filename}_role"
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

resource "aws_iam_role_policy_attachment" "scraper_lambda_policy" {
  role       = aws_iam_role.scraper_lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "scraper_dynamodb-lambda-policy" {
   name = "dynamodb_lambda_policy"
   role = aws_iam_role.scraper_lambda_role.id

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

