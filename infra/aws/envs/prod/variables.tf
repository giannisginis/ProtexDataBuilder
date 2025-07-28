variable "env" {
  description = "Environment name (dev/staging/prod)"
  type        = string
}

variable "use_batch" {
  description = "Whether to deploy AWS Batch resources"
  type        = bool
  default     = false
}

variable "use_ec2" {
  description = "Whether to deploy EC2 runner"
  type        = bool
  default     = true
}

variable "key_name" {
  description = "SSH key name to access EC2 (if enabled)"
  type        = string
}

variable "aws_region" {
  description = "AWS region to deploy resources in"
  type        = string
  default     = "eu-west-1"
}
