
from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
import os

app = Flask(__name__)
CORS(app)

MODEL_PATH = "skinai_model.h5"
model = tf.keras.models.load_model(MODEL_PATH)

labels = ["Melanoma", "Nevus", "Queratose Seborreica"]

@app.route("/analyze", methods=["POST"])
def analyze():
    if 'file' not in request.files:
        return jsonify({"erro": "Nenhuma imagem recebida"}), 400

    image_file = request.files['file']
    image_path = os.path.join("temp.jpg")
    image_file.save(image_path)

    img = Image.open(image_path).resize((224, 224)).convert("RGB")
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)[0]
    class_index = int(np.argmax(prediction))
    confidence = float(prediction[class_index])

    return jsonify({
        "diagnostico": labels[class_index],
        "confianca": f"{confidence:.2%}",
        "recomendacao": "Procure um dermatologista se tiver duvida."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
