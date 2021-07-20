from flask import Flask, request
import time
import random


app = Flask(__name__)

@app.route("/elPsyCongroo", methods=['POST'])
def lyra():
    wordline = request.args.get("worldline")
    time.sleep(1)
    return {"wordline": int(wordline), "result": random.randint(0, 100)}
