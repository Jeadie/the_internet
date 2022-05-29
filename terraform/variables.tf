# core

variable "region" {
  description = "The AWS region to create resources in."
  default     = "us-east-1"
}


# networking

variable "public_subnet_1_cidr" {
  description = "CIDR Block for Public Subnet 1"
  default     = "10.0.1.0/24"
}
variable "public_subnet_2_cidr" {
  description = "CIDR Block for Public Subnet 2"
  default     = "10.0.2.0/24"
}
variable "private_subnet_1_cidr" {
  description = "CIDR Block for Private Subnet 1"
  default     = "10.0.3.0/24"
}
variable "private_subnet_2_cidr" {
  description = "CIDR Block for Private Subnet 2"
  default     = "10.0.4.0/24"
}
variable "availability_zones" {
  description = "Availability zones"
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]
}


# load balancer

variable "health_check_path" {
  description = "Health check path for the default target group"
  default     = "/ping/"
}


# ecs

variable "ecs_cluster_name" {
  description = "Name of the ECS cluster"
  default     = "production"
}
variable "amis" {
  description = "Which AMI to spawn."
  default = {
    us-east-1 = "ami-061c10a2cb32f3491"
  }
}
variable "instance_type" {
  default = "t2.micro"
}
variable "docker_image_url_django" {
  description = "Docker image to run in the ECS cluster"
  default     = "383495223751.dkr.ecr.us-east-1.amazonaws.com/the_internet:latest"
}
variable "docker_image_url_nginx" {
  description = "Docker image to run in the ECS cluster"
  default     = "383495223751.dkr.ecr.us-east-1.amazonaws.com/nginx:latest"
}
variable "app_count" {
  description = "Number of Docker containers to run"
  default     = 1
}
variable "allowed_hosts" {
  description = "Domain name for allowed hosts"
  default     = "YOUR DOMAIN NAME"
}


# logs

variable "log_retention_in_days" {
  default = 3
}


# key pair

variable "ssh_pubkey_file" {
  description = "Path to an SSH public key"
  default     = "~/.ssh/id_rsa.pub"
  sensitive = true
}


# auto scaling

variable "autoscale_min" {
  description = "Minimum autoscale (number of EC2)"
  default     = "1"
}
variable "autoscale_max" {
  description = "Maximum autoscale (number of EC2)"
  default     = "1"
}
variable "autoscale_desired" {
  description = "Desired autoscale (number of EC2)"
  default     = "1"
}


# rds

variable "rds_db_name" {
  description = "RDS database name"
  default     = "internet"
}
variable "rds_username" {
  description = "RDS database username"
  default     = "jeadie"
  sensitive = true
}
variable "rds_instance_class" {
  description = "RDS instance type"
  default     = "db.t3.micro"
}


# domain

variable "certificate_arn" {
  description = "AWS Certificate Manager ARN for validated domain"
  default     = "arn:aws:acm:us-east-1:383495223751:certificate/1b2a9231-2bee-4375-8dd2-a44227a4dddb"
}

variable "django_stage" {
  description = ""
  default = "production"
}

variable "django_superuser_username" {
  description = "Username used by django.setting DJANGO_SUPERUSER_PASSWORD"
  default = "jeadie"
}
variable "django_superuser_password" {
  description = "Password used by django.setting DJANGO_SUPERUSER_PASSWORD"
  default = "admin"
  sensitive = true
}
variable "django_superuser_email" {
  description = "Email used by django.setting DJANGO_SUPERUSER_EMAIL"
  default = "jackeadie@duck.com"
  sensitive = true
}