module "ecr-repo-star" {
  source = "../modules/ecr-repo"
  name = "star"
  num_of_last_images_to_keep = 7
}

module "ecr-repo-kraken" {
  source = "../modules/ecr-repo"
  name = "kraken"
  num_of_last_images_to_keep = 30
}
