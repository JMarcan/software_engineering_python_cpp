# Designate a cloud provider, region, and credentials
provider "aws" {
    profile = "default"
    region = var.region
}

data "archive_file" "lambda_zip" {
    type        = "zip"
    source_dir  = "source"
    output_path = "lambda.zip"
}

resource "aws_iam_role" "iam_role_lambda" {
  name        = "iam_role_lambda"
  description = "Allows Lambda Function to call AWS services."
  assume_role_policy = <<EOF
{
	"Version": "2012-10-17",
	"Statement": [{
		"Action": "sts:AssumeRole",
		"Principal": { "Service": "lambda.amazonaws.com" },
		"Effect": "Allow",
		"Sid": "" } ]
}
EOF
}

resource "aws_lambda_function" "greet_function" {
  filename         = "lambda.zip"
  source_code_hash = "data.archive_file.lambda_zip.output_base64sha256"
  function_name    = "greeting"
  role             = aws_iam_role.iam_role_lambda.arn # reference IAM Role with required permissions
  handler          = "lambda.lambda_handler"
  runtime          = "python3.6"
  memory_size      = 128
  timeout          = 30
  
  environment {
    variables = {
      greeting = "HiFromTerraform"
    }
  }
}


# Define Policy
resource "aws_iam_policy" "lambda_logging" {
  name        = "lambda_logging"
  path        = "/"
  description = "IAM policy for logging from a lambda"

  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:*:*:*",
      "Effect": "Allow"
    }
  ]
}
EOF
}

# Attach policy to role
resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.iam_role_lambda.name
  policy_arn = aws_iam_policy.lambda_logging.arn
}

# Create CloudWatch Log Group
resource "aws_cloudwatch_log_group" "greeting" {
  name              = "/aws/lambda/greeting"
  retention_in_days = 7
}



