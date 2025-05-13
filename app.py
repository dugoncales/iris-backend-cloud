from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    return jsonify({
        "diagnostico": "Melanoma",
        "risco": "Alto",
        "recomendacao": "Procure um dermatologista"
    })

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

