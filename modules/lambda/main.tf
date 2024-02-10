 resource "aws_iam_role" "lambda" {
   name = "lambda_role"
 
   assume_role_policy = jsonencode({
     "Version" : "2012-10-17",
     "Statement" : [
       {
       "Effect" : "Allow",
       "Principal" : {
           "Service" : "lambda.amazonaws.com"
       },
       "Action" : "sts:AssumeRole"
       }
     ]
   })
   #... 他のパラメータ ...
 }