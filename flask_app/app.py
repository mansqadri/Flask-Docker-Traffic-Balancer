from flask import Flask
import argparse
import redis
import os

app = Flask(__name__)

# Connect to Redis
redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.StrictRedis(host=redis_host, port=6379, decode_responses=True)

@app.route('/')
def hello():
    app_name = os.getenv('APP_NAME', 'Flask App')
    app_key = f"{app_name}_hits"
    total_key = "total_hits"

    redis_client.incr(app_key)
    redis_client.incr(total_key)

    app_hits = redis_client.get(app_key)
    total_hits = redis_client.get(total_key)
    other_app_hits = int(total_hits)-int(app_hits)

    return f"""
    <h1>Welcome from {app_name}</h1>
    <h2>Hits on this app: {app_hits}</h2>
    <h2>Hits on the other app: {other_app_hits}</h2>
    <h2>Total Hits: {total_hits}</h2>
    """

if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--message', default='Hello, World!', help='Custom message for the Flask app')
    # args = parser.parse_args()
    # os.environ['APP_NAME'] = args.name

    # custom_message = args.message  
    app.run(host='0.0.0.0')  
