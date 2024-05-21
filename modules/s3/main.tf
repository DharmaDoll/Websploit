 # Create S3 bucket to store CodeBuild artifacts
 resource "aws_s3_bucket" "bucket" {
    bucket = "this-is-test-bucket-tf-my"
    acl    = "public-read"  # パブリックリードアクセスを設定
    versioning {
      enabled = true
    }
 }
 
 resource "aws_s3_bucket_policy" "bucket_policy" {
   bucket = aws_s3_bucket.bucket.id
   policy = data.aws_iam_policy_document.allow_codebuild_lambda.json
 }
 
 # CodeBuildからのみ書き込み可能
 data "aws_iam_policy_document" "allow_codebuild_lambda" {
  statement {
    sid    = "AllowCodeBuildToPutObject"
    actions = ["s3:PutObject"]
    resources = ["${aws_s3_bucket.bucket.arn}/*"]
    principals {
      type        = "AWS"
      identifiers = [var.codebuild_role_arn]
    }
   }
 
   statement {
     sid    = "All"
     actions = ["s3:GetObject"]
     resources = ["${aws_s3_bucket.bucket.arn}/*"]
     principals {
       type        = "AWS"
       identifiers = ["*"]
     }
   }
 }



