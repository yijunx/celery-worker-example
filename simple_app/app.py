from flask import Flask, request
import time
import random


app = Flask(__name__)


@app.route("/elPsyCongaroo", methods=['POST'])
def lyra():
    wordline = request.args.get("worldline")
    if wordline is None:
        return "error...please add worldline as an integer in query parameter..."
    time.sleep(1)
    return {"wordline": int(wordline), "result": random.randint(0, 100)}
