#  terraform {  
 #    backend "s3" {
 #      bucket = "mybucket"
 #      key    = "path/to/my/key"
 #      region = "us-east-1"
 #      # DynamoDB を使って state ファイルのロックを行うための設定
 #      dynamodb_table = "mytable"
 #      encrypt = true
 #    }
 #  }
 #}
 #この設定を適用するためには、`terraform init` コマンドを再度実行する必要があります。S3バケットとDynamoDBテーブルがまだ存在しない場合は、事前に作成しておく必要があります。
 
 provider "aws" {
   region = "ap-northeast-1"
  #  profile = "my-profile"
 }
 
 module "s3" {
   source = "./modules/s3"
   codebuild_role_arn = module.codebuild.codebuild_role_arn
 }
 
 module "codebuild" {
   source = "./modules/codebuild"
   bucket_arn  = module.s3.bucket_arn
   bucket_name = module.s3.bucket_name
 }
  
 module "eventbridge" {
   source = "./modules/eventbridge"
   codebuild_arn = module.codebuild.codebuild_arn
 }