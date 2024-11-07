import asyncio
import logging
import os
import random
import time
from datetime import datetime

import cv2
import numpy as np
import requests
import schedule
# from telegram import Update
from ultralytics import YOLO

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('person_detection.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Configurações
CAMERA_ENDPOINT = "http://192.168.0.15/capture"
TELEGRAM_BOT_TOKEN = ""
TELEGRAM_CHAT_ID = ""
CHECK_INTERVAL_SECONDS = 30
SAVE_IMAGES = True
IMAGES_DIR = "detected_images"

# Criar diretório para salvar imagens se não existir
if SAVE_IMAGES and not os.path.exists(IMAGES_DIR):
    os.makedirs(IMAGES_DIR)


class PersonDetector:
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
            logger.error("Erro ao baixar imagem: %s", str(e))
            image_files = [f for f in os.listdir(
                "images/") if f.endswith(".jpg") or f.endswith(".png")]
            if image_files:
                random_file = random.choice(image_files)
                image = cv2.imread(os.path.join("images/", random_file))
                logger.info("Usando imagem aleatória: %s", random_file)
                return image

            logger.error("Não há imagens disponíveis na pasta local")
            return None

    def detect_person(self, image):
        try:
            # Executar detecção
            results = self.model(image)

            # Verificar se há pessoas (classe 0 no COCO dataset)
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    if box.cls == 0:  # 0 é o índice para 'person' no COCO dataset
                        return True, box
            return False, None
        except Exception as e:
            logger.error("Erro na detecção: %s", str(e))
            return False, None

    async def send_telegram_alert(self, image_path=None):
        pass

    def save_image(self, image):
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            image_path = os.path.join(IMAGES_DIR, f"detection_{timestamp}.jpg")
            cv2.imwrite(image_path, image)
            return image_path
        except Exception as e:
            logger.error("Erro ao salvar imagem: %s", str(e))
            return None

    def check_camera(self):
        logger.info("Iniciando verificação da câmera")

        # Baixar imagem
        image = self.download_image()
        if image is None:
            return

        # Detectar pessoa
        person_detected, box = self.detect_person(image)

        if person_detected:
            logger.info("Pessoa detectada!")

            # Salvar imagem se configurado
            image_path = None
            if SAVE_IMAGES:
                if box is not None:
                    # Desenhar caixa de detecção na imagem
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                image_path = self.save_image(image)

            # Enviar alerta
            asyncio.run(self.send_telegram_alert(image_path))
        else:
            logger.info("Nenhuma pessoa detectada")


def main():
    detector = PersonDetector()

    detector.check_camera()

    # Agendar a verificação
    # schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(detector.check_camera)

    logger.info("Monitoramento iniciado - verificando a cada %s segundos",
                CHECK_INTERVAL_SECONDS)

    # Loop principal
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()
