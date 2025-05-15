from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Carrega o modelo treinado
model = load_model("skinai_model.h5")

# Rótulos e descrições
lesoes_info = {
    "Melanoma": {
        "risco": "Alto",
        "descricao": "Tipo de câncer de pele potencialmente grave.",
        "link": "https://www.inca.gov.br/tipos-de-cancer/cancer-de-pele-melanoma",
        "recomendacao": "Procure um dermatologista imediatamente."
    },
    "Nevus": {
        "risco": "Baixo",
        "descricao": "Pinta ou sinal benigno comum na pele.",
        "link": "https://www.dermatologia.net/novo/base/doencas/nevo/",
        "recomendacao": "Apenas acompanhamento dermatológico de rotina."
    },
    "Carcinoma Basocelular": {
        "risco": "Médio",
        "descricao": "Câncer de pele mais comum e de crescimento lento.",
        "link": "https://www.tuasaude.com/carcinoma-basocelular/",
        "recomendacao": "Agende consulta com dermatologista para biópsia e tratamento."
    }
    # Adicione mais se desejar
}

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "Nenhuma imagem enviada."}), 400

    # Processamento da imagem
    image = Image.open(file.stream).resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)

    # Predição
    prediction = model.predict(image)[0]
    idx = np.argmax(prediction)
    confidence = float(prediction[idx])
    labels = list(lesoes_info.keys())
    label = labels[idx]
    info = lesoes_info[label]

    return jsonify({
        "diagnostico": label,
        "risco": info["risco"],
        "descricao": info["descricao"],
        "link": info["link"],
        "recomendacao": info["recomendacao"],
        "confianca": round(confidence * 100, 2)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
