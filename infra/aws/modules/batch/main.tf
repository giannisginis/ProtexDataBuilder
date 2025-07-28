resource "aws_batch_compute_environment" "pipeline" {
  type                     = "MANAGED"
  service_role             = aws_iam_role.batch_service.arn

  compute_resources {
    type        = "EC2"
    min_vcpus   = 0
    max_vcpus   = 4
    desired_vcpus = 0
    instance_type = ["c5.large"]
    subnets          = var.subnet_ids
    security_group_ids = [var.security_group_id]
    instance_role    = aws_iam_instance_profile.ecs_instance_profile.arn
  }
  depends_on = [aws_iam_role_policy_attachment.batch_service_policy]
}

resource "aws_batch_job_queue" "queue" {
  name     = "pipeline-job-queue-${var.env}"
  state    = "ENABLED"
  priority = 1

  compute_environment_order {
    order               = 1
    compute_environment = aws_batch_compute_environment.pipeline.arn
  }
}

resource "aws_batch_job_definition" "job" {
  name       = "pipeline-job-def-${var.env}"
  type       = "container"
  platform_capabilities = ["EC2"]

  container_properties = jsonencode({
    image: var.image_uri,
    vcpus: 2,
    memory: 4096,
    command: ["run", "--video", "/data/video.mp4", "--output", "/data/output"],
    environment: [],
    jobRoleArn: aws_iam_role.batch_job.arn
  })
}

resource "aws_iam_role" "batch_service" {
  name = "batch-service-role-${var.env}"

  assume_role_policy = jsonencode({
    Version: "2012-10-17",
    Statement: [{
      Effect: "Allow",
      Principal: { Service: "batch.amazonaws.com" },
      Action: "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_role_policy_attachment" "batch_service_policy" {
  role       = aws_iam_role.batch_service.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSBatchServiceRole"
}

resource "aws_iam_role" "batch_job" {
  name = "batch-job-role-${var.env}"

  assume_role_policy = jsonencode({
    Version: "2012-10-17",
    Statement: [{
      Effect: "Allow",
      Principal: { Service: "ecs-tasks.amazonaws.com" },
      Action: "sts:AssumeRole"
    }]
  })
}

resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "ecs-instance-profile-${var.env}"
  role = aws_iam_role.batch_job.name
}
