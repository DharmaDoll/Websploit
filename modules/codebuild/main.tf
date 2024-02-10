 # # AWS CodeBuild Project
 resource "aws_codebuild_project" "project" {
  name          = "my_codebuild_pj"
  service_role  = aws_iam_role.codebuild.arn
  build_timeout = "5"
  description = "CodeBuild project that runs a script and uploads the artifacts to S3 bucket"
  
  artifacts {
    type      = "S3"
    location  = var.bucket_name
    packaging = "ZIP"
  }
  environment {
    compute_type = "BUILD_GENERAL1_SMALL"
    image        = "aws/codebuild/standard:4.0"
    type         = "LINUX_CONTAINER"
    privileged_mode = true
    environment_variable {
       name  = "S3_BUCKET"
       value = var.bucket_name
     }
  }
 
  source {
      type            = "NO_SOURCE"
      buildspec = <<-EOF
    version: 0.2
  
    phases:
      build:
        commands:
          - echo "Running scripts..."
    				- docker pull vuls/go-exploitdb:latest
          - for src in exploitdb inthewild githubrepos awesomepoc;
            do
              docker run --rm -v local_volume:/go-exploitdb vuls/go-exploitdb fetch $src
            done
          - echo '[+] Database import is complete.'
          - sleep 5
          - mkdir -p ../data
          - docker run --name go-exploitdb -d -v local_volume:/go-exploitdb --entrypoint="tail" vuls/go-exploitdb "-f" "/dev/null"
          - docker cp go-exploitdb://go-exploitdb/go-exploitdb.sqlite3 .
          - docker stop go-exploitdb && docker rm go-exploitdb
          - aws s3 cp ./go-exploitdb.sqlite3 s3://bucket-name
    EOF
    }
 }
 
 data "aws_iam_policy_document" "codebuild" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
  }
 }
 
 data "aws_iam_policy_document" "codebuild_s3_access" {
   statement {
     actions   = ["s3:PutObject"]
     resources = [var.bucket_arn]
   }
 }
 
 resource "aws_iam_role" "codebuild" {
   name               = "codebuild_role"
   assume_role_policy = data.aws_iam_policy_document.codebuild.json
 }
 
 resource "aws_iam_role_policy" "codebuild_s3_access" {
   role   = aws_iam_role.codebuild.id
   policy = data.aws_iam_policy_document.codebuild_s3_access.json
 }