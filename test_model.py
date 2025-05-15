
from tensorflow.keras.models import load_model

try:
    model = load_model("skinai_model.h5")
    print("✅ Modelo carregado com sucesso!")
except Exception as e:
    print("❌ Erro ao carregar o modelo:")
    print(e)
