 output "lambda_role_arn" {
   value = aws_iam_role.lambda.arn  # Change this to your actual IAM role resource and attribute
   description = "The ARN of the created Lambda IAM role"
 }