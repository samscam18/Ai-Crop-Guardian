variable "instance_type" {
  description = "EC2 instance type for ECS tasks"
  default     = "t3.medium"
}

variable "desired_count" {
  description = "Desired number of ECS tasks"
  default     = 2
}

variable "weather_api_key" {
  description = "OpenWeatherMap API key"
  type        = string
  sensitive   = true
}