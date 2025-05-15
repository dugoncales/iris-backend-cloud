from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/analyze", methods=["POST"])
def analyze():
    # Aqui você pode colocar a lógica real com o modelo .h5
    # Por enquanto estamos simulando uma resposta

    return jsonify({
        "diagnostico": "Melanoma",
        "confianca": "92%",
        "descricao": "O melanoma é um tipo agressivo de câncer de pele que pode se espalhar rapidamente para outras partes do corpo.",
        "link": "https://dermnetnz.org/topics/melanoma",
        "recomendacao": "Consulte um dermatologista com urgência para investigação e tratamento adequado."
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
