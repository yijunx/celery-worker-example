from flask import Flask, request
import time
import random


app = Flask(__name__)


@app.route("/random_number", methods=["POST"])
def lyra():
    time.sleep(1)
    return {"random_number": random.randint(0, 100)}
