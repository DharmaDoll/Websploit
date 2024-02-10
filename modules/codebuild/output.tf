 output "codebuild_arn" {
   value = aws_codebuild_project.project.arn
   description = "The ARN of the CodeBuild project."
 }
 output "codebuild_role_arn" {
   value = aws_iam_role.codebuild.arn
   description = "The ARN of the CodeBuild IAM role."
 }



 