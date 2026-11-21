# Монітор справності та часу безперебійної роботи сервісу (розгортання на Render)

## Призначення
Власний мікросервіс на Python (Flask + Gunicorn), який перевіряє доступність HTTP/HTTPS-ендпойнтів (`GET /check`), зберігає історію останніх перевірок (`GET /history`), повертає стан сервісу (`GET /health`) та перенаправляє кореневий запит (`GET /`) на `/health`. Застосунок упаковується у Docker, перевіряється у CI, розгортається на Render через GitHub Actions та має IaC-опис у Terraform.

## Локальний запуск
```bash
docker build -t uptime-monitor:local .
docker run -d -p 8080:8080 -e APP_ENV=local --name uptime-local uptime-monitor:local
curl http://localhost:8080/health
```

## Розгортання (Render + Docker Hub + GitHub Actions)
1. Створіть веб-сервіс на Render із використанням образу з Docker Hub (`<DOCKER_USERNAME>/uptime-monitor:latest`) або через конфігурацію в каталозі `infra/` з офіційним Terraform-провайдером `render-oss/render`.
2. Додайте необхідні секрети в репозиторій GitHub (`DOCKER_USERNAME`, `DOCKER_TOKEN`, `RENDER_DEPLOY_HOOK_URL`).
3. Запуште зміни у гілку `main` репозиторію (`Practical-activity-14.-Individual-project`) — GitHub Actions запускає `pytest`, збирає та пушить Docker-образ у Docker Hub, перевіряє конфігурацію Terraform (`terraform validate`) і запускає розгортання на Render через Deploy Hook.

## Змінні середовища та секрети GitHub

### Змінні середовища застосунку
* `APP_ENV` — середовище запуску (`local` або `production`).
* `TARGET_URL` — цільовий URL за замовчуванням для `/check` (за замовчуванням `[https://httpbin.org/get](https://httpbin.org/get)`).
* `PORT` — порт HTTP-сервера (за замовчуванням `8080`, автоматично передається Render).

### Секрети GitHub
* `DOCKER_USERNAME` — ім'я користувача Docker Hub.
* `DOCKER_TOKEN` — токен доступу Docker Hub.
* `RENDER_DEPLOY_HOOK_URL` — Deploy Hook URL із налаштувань веб-сервісу на Render.
* `RENDER_API_KEY` — (опціонально, для роботи з Terraform-провайдером Render із `infra/`) API-ключ Render.
* `RENDER_OWNER_ID` — (опціонально, для роботи з Terraform-провайдером Render із `infra/`) ідентифікатор власника/акаунта на Render.
