# Service Health & Uptime Monitor (Render Deployment)

## Призначення
Власний мікросервіс на Python (Flask + Gunicorn), який перевіряє доступність HTTP/HTTPS-ендпойнтів (`GET /check`), зберігає історію останніх перевірок (`GET /history`) і повертає стан сервісу (`GET /health`). Застосунок контейнерується у Docker, тестується у CI та розгортається на **Render** через GitHub Actions із IaC-описом у Terraform.

## Локальний запуск
```bash
docker build -t uptime-monitor:local .
docker run -d -p 8080:8080 -e APP_ENV=local --name uptime-local uptime-monitor:local
curl http://localhost:8080/health
```

## Деплой (Render + Docker Hub + GitHub Actions)
1. Створіть сервіс на Render (Image-backed Web Service з Docker Hub образу `<DOCKER_USERNAME>/uptime-monitor:latest` або через конфігурацію `infra/` з офіційним Terraform-провайдером `render-oss/render`).
2. Додайте необхідні секрети в GitHub Secrets репозиторію (`DOCKER_USERNAME`, `DOCKER_TOKEN`, `RENDER_DEPLOY_HOOK_URL`).
3. Запуште зміни у гілку `main` у каталозі `students/yourname/` — GitHub Actions прожене `pytest`, збере і завантажить Docker-образ у Docker Hub, перевірить валідність Terraform (`terraform validate`) та запустить деплой на Render через Deploy Hook.

## Змінні середовища та GitHub Secrets
### Змінні середовища застосунку
- `APP_ENV` — середовище запуску (`local` або `production`).
- `TARGET_URL` — цільовий URL за замовчуванням для `/check` (за замовчуванням `https://httpbin.org/get`).
- `PORT` — порт HTTP-сервера (за замовчуванням `8080`, автоматично передається Render).

### GitHub Secrets
- `DOCKER_USERNAME` — ім'я користувача Docker Hub.
- `DOCKER_TOKEN` — токен доступу Docker Hub.
- `RENDER_DEPLOY_HOOK_URL` — Deploy Hook URL вебсервісу з налаштувань Render.
- `RENDER_API_KEY` — (опціонально, для локального `terraform apply` з `infra/`) API-ключ Render.
- `RENDER_OWNER_ID` — (опціонально, для локального `terraform apply` з `infra/`) ID воркспейсу/власника в Render.
