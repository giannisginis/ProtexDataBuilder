module "ecr" {
  source = "../../modules/ecr"
  env    = var.env
}

module "ec2" {
  source = "../../modules/ec2"
  count  = var.use_ec2 ? 1 : 0
  env    = var.env
  image_uri = module.ecr.repository_url
  vpc_id     = var.vpc_id
  key_name   = var.key_name
}

module "batch" {
  source = "../../modules/batch"
  count  = var.use_batch ? 1 : 0
  env    = var.env
  image_uri = module.ecr.repository_url
  subnet_ids        = var.subnet_ids
  security_group_id = var.security_group_id
}
