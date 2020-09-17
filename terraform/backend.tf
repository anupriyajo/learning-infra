terraform {
  backend "s3" {
    bucket = "python-state"
    key = "state.tfstate"
    region = "eu-central-1"
  }
}