variable "render_api_key" {
  type        = string
  sensitive   = true
  description = "Render API Key"
}

variable "render_owner_id" {
  type        = string
  description = "Render Workspace/Owner ID (tea-... or usr-...)"
}

variable "docker_image" {
  type        = string
  description = "Full Docker Hub image name (e.g. username/uptime-monitor)"
}

variable "service_name" {
  type    = string
  default = "uptime-monitor"
}

variable "region" {
  type    = string
  default = "frankfurt"
}
