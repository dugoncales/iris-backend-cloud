from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Carrega o modelo treinado
MODEL_PATH = "skinai_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

# Mapeia classes do modelo
classes = ["Melanoma", "Nevus", "Seborrheic Keratosis"]

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files.get("file")
    if not file:
        return jsonify({"erro": "Nenhuma imagem recebida"}), 400

    try:
        image = Image.open(file).convert("RGB")
        image = image.resize((224, 224))
        array = np.expand_dims(np.array(image) / 255.0, axis=0)
        prediction = model.predict(array)[0]
        class_index = int(np.argmax(prediction))
        confidence = float(prediction[class_index])

        return jsonify({
            "diagnostico": classes[class_index],
            "confianca": f"{confidence:.2%}",
            "recomendacao": "Procure um dermatologista"
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
