variable "env" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "key_name" {
  type = string
}

variable "image_uri" {
  type = string
  description = "ECR image URI to pull"
}
