variable "project_name" {
  type        = string
  description = "Name prefix"
}

variable "vpc_id" {
  type        = string
  description = "VPC ID to create security groups in"
}

variable "app_port" {
  type        = number
  description = "Port your app listens on (ECS task container port)"
  default     = 80
}

variable "db_port" {
  type        = number
  description = "Database port (MySQL default 3306)"
  default     = 3306
}