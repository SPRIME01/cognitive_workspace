terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }

  backend "s3" {
    # These values will be replaced by environment-specific values
    bucket = "cognitive-workspace-terraform-state"
    key    = "state/terraform.tfstate"
    region = "us-west-2"
  }
}

provider "aws" {
  region = var.aws_region
}

# Variables
variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "cognitive-workspace"
}

# Tags to be applied to all resources
locals {
  common_tags = {
    Environment = var.environment
    Project     = var.app_name
    ManagedBy   = "terraform"
  }
}

# VPC and Networking resources would be defined here

# Output values
output "aws_region" {
  value = var.aws_region
}
