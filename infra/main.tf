terraform {
  required_version = ">= 1.5.0"
  required_providers {
    render = {
      source  = "render-oss/render"
      version = "~> 1.3"
    }
  }
}

provider "render" {
  api_key  = var.render_api_key
  owner_id = var.render_owner_id
}

resource "render_web_service" "uptime_monitor" {
  name   = var.service_name
  plan   = "free"
  region = var.region

  runtime_source = {
    image = {
      image_url = var.docker_image
      tag       = "latest"
    }
  }

  health_check_path = "/health"

  env_vars = {
    APP_ENV = {
      value = "production"
    }
    TARGET_URL = {
      value = "https://httpbin.org/get"
    }
  }
}
