output "lambda_function" {
  value = aws_lambda_function.greet_function.arn
  description = "Output of the lamda function name"
}
