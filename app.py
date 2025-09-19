
from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/", methods = ["GET"])
def home():
    return Response("Flask server is running....",mimetype="text/plain")

    
if __name__ == "__main__":
    app.run(port = 11000)