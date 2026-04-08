variable "aws_region" {
  default = "us-east-1"
}

variable "app_name" {
  default = "tripledger"
}

variable "db_username" {
  default = "sanjay"
}

variable "db_password" {
  description = "Database password"
  sensitive   = true
}

variable "anthropic_api_key" {
  description = "Anthropic API key"
  sensitive   = true
}

variable "secret_key" {
  description = "JWT secret key"
  sensitive   = true
}