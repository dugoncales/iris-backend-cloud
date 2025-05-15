from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Carrega o modelo .h5
model = load_model("skinai_model.h5")

# Dicionário de resultados (exemplo, personalize depois)
resultados = {
    0: {
        "diagnostico": "Melanoma",
        "risco": "Alto",
        "recomendacao": "Procure um dermatologista",
        "link": "https://www.oncoguia.org.br/conteudo/melanoma/1306/1"
    },
    1: {
        "diagnostico": "Nevus",
        "risco": "Baixo",
        "recomendacao": "Monitoramento anual recomendado",
        "link": "https://www.sbd.org.br/dermatologia/atlas/nevo/"
    }
    # Adicione mais se necessário
}

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files["file"]
    image = Image.open(file.stream).resize((224, 224))
    img_array = np.array(image) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)
    predicted_class = np.argmax(prediction)

    resultado = resultados.get(predicted_class, {
        "diagnostico": "Desconhecido",
        "risco": "Indefinido",
        "recomendacao": "Repetir a imagem ou consultar dermatologista",
        "link": ""
    })

    return jsonify(resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
