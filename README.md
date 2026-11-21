# Монітор справності та часу безперебійної роботи сервісу (розгортання на Render)

## Призначення
Власний мікросервіс на Python (Flask + Gunicorn), який перевіряє доступність HTTP/HTTPS-ендпойнтів (`GET /check`), зберігає історію останніх перевірок (`GET /history`), повертає стан сервісу (`GET /health`) та перенаправляє кореневий запит (`GET /`) на `/health`. Застосунок упаковується у Docker, перевіряється у CI, розгортається на Render через GitHub Actions та має IaC-опис у Terraform.

## Локальний запуск
```bash
docker build -t uptime-monitor:local .
docker run -d -p 8080:8080 -e APP_ENV=local --name uptime-local uptime-monitor:local
curl http://localhost:8080/health
