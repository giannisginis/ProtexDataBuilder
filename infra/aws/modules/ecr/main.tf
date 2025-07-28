resource "aws_ecr_repository" "this" {
  name = "dataset-pipeline-${var.env}"
  image_tag_mutability = "MUTABLE"
  force_delete = true
}
