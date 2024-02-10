 # Create a EventBridge Rule
 resource "aws_cloudwatch_event_rule" "every_two_days" {
  name                = "every-two-days"
  schedule_expression = "rate(2 days)"
 }
 
 # Attach the EventBridge Rule to CodeBuild
 resource "aws_cloudwatch_event_target" "run_codebuild_every_two_days" {
  rule      = aws_cloudwatch_event_rule.every_two_days.name
  target_id = "run_codebuild"
  arn       = var.codebuild_arn
  role_arn  = aws_iam_role.event_bridge.arn
 }
 
 resource "aws_iam_role" "event_bridge" {
   name               = "event_bridge_role"
   assume_role_policy = jsonencode({
     Version   = "2012-10-17",
     Statement = [
       {
         Action    = "sts:AssumeRole"
         Principal = { Service = "events.amazonaws.com" }
         Effect    = "Allow"
         Sid       = ""
       },
     ]
   })
 }
 
 resource "aws_iam_role_policy" "eventbridge_codebuild_access" {
 #   name = "example"
   role = "${aws_iam_role.event_bridge.id}"
   policy = jsonencode({
     Version   = "2012-10-17"
     Statement = [
       {
         Effect   = "Allow"
         Action   = [ "codebuild:StartBuild" ]
         Resource = var.codebuild_arn
       },
     ]
   })
 }