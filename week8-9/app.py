from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host="redis-master", port=6379, decode_responses=True)

@app.route("/")
def home():
    try:
        r.set("ping", "pong")
        return f"Redis says: {r.get('ping')}"
    except Exception as e:
        return f"Redis error: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
