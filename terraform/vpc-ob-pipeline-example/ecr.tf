
module "ecr-repo-outlier-bio-disambiguate" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/disambiguate"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-fastqc" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/fastqc"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-kallisto" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/kallisto"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-multiqc" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/multiqc"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-skewer" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/skewer"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-star" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/star"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-samtools" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/samtools"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-s3sync" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/s3sync"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-gdc" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/gdc"
  num_of_last_images_to_keep = 30
}

module "ecr-repo-outlier-bio-sra" {
  source = "../modules/ecr-repo"
  name = "outlier-bio/sra"
  num_of_last_images_to_keep = 30
}
