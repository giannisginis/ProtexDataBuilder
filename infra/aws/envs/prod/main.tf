terraform {
  required_version = ">= 1.3"
}

# Discover default VPC
data "aws_vpc" "default" {
  default = true
}

# Discover default subnets in VPC
data "aws_subnets" "default" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Discover default security group
data "aws_security_group" "default" {
  filter {
    name   = "group-name"
    values = ["default"]
  }
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

# Deploy ECR
module "ecr" {
  source = "../../modules/ecr"
  env    = var.env
}

# Deploy EC2 (optional, disabled in prod)
module "ec2" {
  source     = "../../modules/ec2"
  count      = var.use_ec2 ? 1 : 0
  env        = var.env
  image_uri  = module.ecr.repository_url
  vpc_id     = data.aws_vpc.default.id
  key_name   = var.key_name
}

# Deploy AWS Batch (enabled in prod)
module "batch" {
  source            = "../../modules/batch"
  count             = var.use_batch ? 1 : 0
  env               = var.env
  image_uri         = module.ecr.repository_url
  subnet_ids        = data.aws_subnets.default.ids
  security_group_id = data.aws_security_group.default.id
}
