"""
Módulo para detecção de pessoas em imagens usando YOLO.

Este módulo implementa um sistema de detecção de pessoas utilizando o modelo YOLO,
com funcionalidades para monitoramento contínuo através de câmeras IP. O sistema
inclui:

- Detecção automática de pessoas em intervalos configuráveis
- Logging de eventos e detecções
- Salvamento de imagens com detecções
- Integração com câmeras IP através de endpoints HTTP

Attributes:
    CAMERA_ENDPOINT (str): URL do endpoint da câmera para captura de imagens
    CHECK_INTERVAL_SECONDS (int): Intervalo em segundos entre verificações
    SAVE_IMAGES (bool): Flag para habilitar/desabilitar salvamento de imagens
    IMAGES_DIR (str): Diretório onde as imagens detectadas serão salvas

Dependencies:
    - OpenCV (cv2)
    - Ultralytics YOLO
    - NumPy
    - Requests
    - Schedule
"""

import logging
import os
import time

import cv2
import schedule
from dotenv import load_dotenv
from ultralytics import YOLO

from functions.download_image import download_image
from functions.save_image import save_image

load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("person_detection.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configurações
CAMERA_ENDPOINT = os.getenv("CAMERA_ENDPOINT")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS"))
SAVE_IMAGES = True
IMAGES_DIR = "detected_images"


class PersonDetector:
    """
    Classe responsável por detectar pessoas em imagens usando o modelo YOLO.
    Esta classe fornece funcionalidades para:
    - Carregar e inicializar o modelo YOLO
    - Fazer download de imagens de uma câmera remota
    - Detectar pessoas nas imagens capturadas
    - Salvar imagens com detecções
    Attributes:
        model: Instância do modelo YOLO carregado para detecção de objetos
    """

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect_person(self, image):
        """
        Detecta pessoas em uma imagem usando o modelo YOLO.
        Args:
            image: Imagem em formato numpy array (BGR)
        Returns:
            tuple: (bool, box)
                - bool: True se uma pessoa foi detectada, False caso contrário
                - box: Coordenadas da caixa de detecção se uma pessoa foi encontrada, None caso contrário
        """

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

    def check_camera(self):
        """
        Realiza a verificação da câmera para detectar pessoas.

        Este método executa os seguintes passos:
        1. Baixa uma imagem da câmera
        2. Executa a detecção de pessoas na imagem
        3. Se uma pessoa for detectada:
           - Desenha uma caixa de detecção na imagem (se houver)
           - Salva a imagem (se configurado)
           - Registra a detecção nos logs

        Returns:
            None
        """

        logger.info("Iniciando verificação da câmera")

        # Baixar imagem
        image = download_image(CAMERA_ENDPOINT, logger)
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
                image_path = save_image(image, IMAGES_DIR, logger)

            # TODO - Enviar alerta
            logger.info(image_path)
        else:
            logger.info("Nenhuma pessoa detectada")


def main():
    """
    Função principal que inicializa o detector de pessoas e configura o agendamento
    das verificações periódicas da câmera. O programa roda continuamente,
    verificando a câmera no intervalo definido em CHECK_INTERVAL_SECONDS.
    """

    if not CAMERA_ENDPOINT:
        logger.error("A URL da câmera não está configurada.")
        return
    if CHECK_INTERVAL_SECONDS <= 0 or CHECK_INTERVAL_SECONDS is None:
        logger.error("O intervalo de verificação deve ser maior que zero ou não nulo.")
        return

    if SAVE_IMAGES and not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)

    detector = PersonDetector()

    schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(detector.check_camera)

    logger.info(
        "Monitoramento iniciado - verificando a cada %s segundos",
        CHECK_INTERVAL_SECONDS,
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
