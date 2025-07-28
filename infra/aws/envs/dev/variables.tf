variable "env" {
  description = "Environment name (e.g. dev, staging, prod)"
  type        = string
}

variable "use_ec2" {
  type    = bool
  default = true
}

variable "use_batch" {
  type    = bool
  default = false
}

variable "subnet_ids" {
  type = list(string)
}

variable "security_group_id" {
  type = string
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to deploy EC2 instance"
}

variable "key_name" {
  type        = string
  description = "Name of the SSH key pair"
}
