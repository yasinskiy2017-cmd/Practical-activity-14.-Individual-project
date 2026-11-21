import os
from datetime import datetime, timezone
from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

APP_ENV = os.getenv("APP_ENV", "local")
DEFAULT_TARGET = os.getenv("TARGET_URL", "https://httpbin.org/get")
CHECKS_LOG = []


@app.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "platform": "render",
            "env": APP_ENV,
            "default_target": DEFAULT_TARGET,
            "time_utc": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.get("/check")
def check_target():
    target = request.args.get("url", DEFAULT_TARGET).strip()
    if not target.startswith(("http://", "https://")):
        return jsonify({"error": "URL must start with http:// or https://"}), 400

    try:
        resp = requests.get(target, timeout=5)
        record = {
            "target": target,
            "reachable": True,
            "status_code": resp.status_code,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
    except requests.RequestException as exc:
        record = {
            "target": target,
            "reachable": False,
            "error": str(exc),
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    CHECKS_LOG.append(record)
    return jsonify(record), 200 if record["reachable"] else 502


@app.get("/history")
def history():
    return jsonify({"count": len(CHECKS_LOG), "items": CHECKS_LOG[-20:]})


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
