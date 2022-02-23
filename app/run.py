import hashlib
import os

import redis

from flask import Flask, request, render_template, Response

app = Flask(__name__)

salt = os.getenv("SECRET", "S0me_seCr3T-keY")

redis_host = os.getenv("REDIS_HOST", "localhost")
redis_client = redis.Redis(host=redis_host, port=6379, db=0)


def hash_password(password: str) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )


def check_password(password: str, hashed: bytes) -> bool:
    return hashed == hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000
    )


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register/", methods=["POST"])
def register():
    if request.method == "POST":
        email = request.values.get("email")
        hashed = hash_password(password=request.values.get("password"))
        redis_client.set(email, hashed)
        return Response()


@app.route("/login/", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.values.get("email")
        hashed = redis_client.get(email)
        if hashed and check_password(password=request.values.get("password"), hashed=hashed):
            return Response()
    return Response(status=400)


@app.route("/logout/", methods=["POST"])
def logout():
    if request.method == "POST":
        email = request.values.get("email")
        hashed = redis_client.get(email)
        if hashed and check_password(password=request.values.get("password"), hashed=hashed):
            redis_client.delete(email)
            return Response()
    return Response(status=400)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
