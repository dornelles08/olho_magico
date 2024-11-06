import asyncio
import logging
import os
import random
import time
from datetime import datetime

import cv2
import face_recognition
import numpy as np
import requests
import schedule
# from telegram import Bot
from ultralytics import YOLO

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('face_recognition.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações
CAMERA_ENDPOINT = "http://192.168.0.30/capture"
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
CHECK_INTERVAL_SECONDS = 30
SAVE_IMAGES = True
KNOW_IMAGES_DIR = "known_faces"
IMAGES_DIR = "detected_images"

if SAVE_IMAGES and not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)

if not os.path.exists(KNOW_IMAGES_DIR):
    os.makedirs(KNOW_IMAGES_DIR)

# Carregar imagens de referência e nomes
known_face_encodings = []
known_face_names = []
for filename in os.listdir(KNOW_IMAGES_DIR):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image = face_recognition.load_image_file(
            os.path.join(KNOW_IMAGES_DIR, filename))
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename)[0])


class FaceRecognizer:
    def __init__(self):
        # Carregar modelo YOLO
        self.model = YOLO('yolov8n.pt')
        # Inicializar bot do Telegram
        # self.bot = Bot(token=TELEGRAM_BOT_TOKEN)

    def download_image(self):
        try:
            response = requests.get(CAMERA_ENDPOINT, timeout=5)
            response.raise_for_status()

            # Converter a resposta em uma imagem
            image_array = np.asarray(
                bytearray(response.content), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            return image
        except Exception as e:
            logger.error("Erro ao baixar imagem da câmera: %s", str(e))

            # Se a URL da câmera não funcionar, buscar uma imagem aleatória
            image_files = [f for f in os.listdir(
                "images") if f.endswith(".jpg") or f.endswith(".png")]
            if image_files:
                random_file = random.choice(image_files)
                image = cv2.imread(os.path.join("images", random_file))
                logger.info("Usando imagem aleatória: %s", random_file)
                return image

            logger.error("Não há imagens disponíveis na pasta local")
            return None

    def detect_faces(self, image):
        try:
            # Detectar rostos na imagem
            face_locations = face_recognition.face_locations(image)
            if len(face_locations) == 0:
                logger.info("Nenhum rosto detectado")
                return None, []

            face_encodings = face_recognition.face_encodings(
                image, face_locations)

            # Reconhecer rostos
            names = []
            for face_encoding in face_encodings:
                # Comparar o rosto com os rostos conhecidos
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding)
                name = "Unknown"

                # Se houver correspondência, usar o nome
                if True in matches:
                    matched_indexes = [
                        i for i, match in enumerate(matches) if match]
                    for i in matched_indexes:
                        name = known_face_names[i]
                        break

                names.append(name.split("_")[0])

            return face_locations, names
        except Exception as e:
            logger.error("Erro na detecção de rosto: %s", str(e))
            return None, None

    async def send_telegram_alert(self, image_path, names):
        pass

    def save_image(self, image, name):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(
                IMAGES_DIR, f"detection_{name}_{timestamp}.jpg")
            cv2.imwrite(image_path, image)
            return image_path
        except Exception as e:
            logger.error(f"Erro ao salvar imagem: {str(e)}")
            return None

    def check_camera(self):
        logger.info("Iniciando verificação da câmera")

        # Baixar imagem
        image = self.download_image()
        if image is None:
            return

        # Detectar rostos
        face_locations, names = self.detect_faces(image)

        if face_locations is not None:
            logger.info("Rostos detectados!")

            # Desenhar caixas de detecção na imagem
            for (top, right, bottom, left), name in zip(face_locations, names):
                # Desenhar retângulo
                cv2.rectangle(image, (left, top),
                              (right, bottom), (0, 255, 0), 2)

                # Escrever nome
                cv2.putText(image, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 4, (0, 255, 0), 2)

            # Salvar imagem
            image_path = self.save_image(image, names)

            # Enviar alerta
            asyncio.run(self.send_telegram_alert(image_path, names))
        else:
            logger.info("Nenhum rosto detectado")


def main():
    recognizer = FaceRecognizer()

    recognizer.check_camera()

    # Agendar a verificação
    # schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(recognizer.check_camera)

    logger.info("Monitoramento iniciado - verificando a cada %s segundos",
                CHECK_INTERVAL_SECONDS)

    # Loop principal
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()
