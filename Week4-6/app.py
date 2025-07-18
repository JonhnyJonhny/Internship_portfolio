from flask import Flask, jsonify
import redis
import os

app = Flask(__name__)

# Redis configuration
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_port = int(os.getenv("REDIS_PORT", 6379))

try:
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    r.ping()
except redis.ConnectionError as e:
    print("Redis connection failed:", e)
    r = None

@app.route("/")
def index():
    if r:
        visits = r.incr("counter")
        return jsonify(message="Welcome to the Python app!", visits=visits)
    else:
        return jsonify(error="Redis unavailable"), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
