"""
Face Detection and Recognition System

This module implements a face detection and recognition system using OpenCV and face_recognition.
It can detect faces in images from a camera endpoint and match them against known faces.

Key features:
- Real-time face detection and recognition
- Integration with camera endpoints
- Logging of detection events
- Saving of detected face images
- Configurable check intervals

Dependencies:
- OpenCV
- face_recognition
- numpy
- requests
- ultralytics YOLO
"""

import logging
import os
import time

import cv2
import face_recognition
import schedule
from ultralytics import YOLO

from functions.download_image import download_image
from functions.save_image import save_image

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("face_recognition.log"), logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Configurações
CAMERA_ENDPOINT = os.getenv("CAMERA_ENDPOINT")
CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS"))
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
            os.path.join(KNOW_IMAGES_DIR, filename)
        )
        face_encoding = face_recognition.face_encodings(image)[0]
        known_face_encodings.append(face_encoding)
        known_face_names.append(os.path.splitext(filename)[0])


class FaceRecognizer:
    """
    A class for detecting and recognizing faces in images using YOLO and face_recognition.
    This class provides functionality to:
    - Download images from a camera endpoint or use local images as fallback
    - Detect faces in images using face_recognition library
    - Compare detected faces against a known database of face encodings
    - Process and identify individuals in real-time or from stored images
    Attributes:
        model (YOLO): A YOLO model instance for object detection
    """

    def __init__(self):
        self.model = YOLO("yolov8n.pt")

    def detect_faces(self, image):
        """
        Detects and recognizes faces in the given image.
        Args:
            image (numpy.ndarray): Input image in OpenCV format (BGR)
        Returns:
            tuple: A tuple containing:
                - list: Face locations as tuples of (top, right, bottom, left) coordinates
                - list: Names of recognized individuals, 'Unknown' for unrecognized faces
        The function will:
        1. Detect face locations in the image
        2. Generate face encodings for detected faces
        3. Compare against known face encodings to identify individuals
        4. Return locations and names of detected faces
        If an error occurs during detection, returns (None, None)
        """

        try:
            # Detectar rostos na imagem
            face_locations = face_recognition.face_locations(image)
            # if len(face_locations) == 0:
            #     logger.info("Nenhum rosto detectado")
            #     return None, []

            face_encodings = face_recognition.face_encodings(image, face_locations)

            # Reconhecer rostos
            names = []
            for face_encoding in face_encodings:
                # Comparar o rosto com os rostos conhecidos
                matches = face_recognition.compare_faces(
                    known_face_encodings, face_encoding
                )
                name = "Unknown"

                # Se houver correspondência, usar o nome
                if True in matches:
                    matched_indexes = [i for i, match in enumerate(matches) if match]
                    for i in matched_indexes:
                        name = known_face_names[i]
                        break

                names.append(name.split("_")[0])

            return face_locations, names
        except Exception as e:
            logger.error("Erro na detecção de rosto: %s", str(e))
            return None, None

    def check_camera(self):
        """
        Checks the camera feed for faces, processes detections and sends alerts.

        This function performs the following steps:
        1. Downloads the latest image from the camera
        2. Detects and recognizes faces in the image
        3. Draws bounding boxes and names around detected faces
        4. Saves the annotated image
        5. Sends a Telegram alert with the detection results

        Returns:
            None
        """

        logger.info("Iniciando verificação da câmera")

        # Baixar imagem
        image = download_image(CAMERA_ENDPOINT, logger)
        if image is None:
            return

        # Detectar rostos
        face_locations, names = self.detect_faces(image)

        if face_locations is not None:
            logger.info("Rostos detectados!")

            # Desenhar caixas de detecção na imagem
            for (top, right, bottom, left), name in zip(face_locations, names):
                # Desenhar retângulo
                cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)

                # Escrever nome
                cv2.putText(
                    image,
                    name,
                    (left, top - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    4,
                    (0, 255, 0),
                    2,
                )

            # Salvar imagem
            image_path = save_image(image, IMAGES_DIR, logger)

            # TODO - Enviar alerta
            logger.info(image_path)
        else:
            logger.info("Nenhum rosto detectado")


def main():
    """Função principal que inicializa o reconhecedor facial e agenda verificações periódicas.
    Esta função:
    1. Cria uma instância do reconhecedor facial
    2. Configura a verificação periódica da câmera
    3. Mantém o programa em execução, realizando as verificações agendadas
    Returns:
        None
    """

    recognizer = FaceRecognizer()

    schedule.every(CHECK_INTERVAL_SECONDS).seconds.do(recognizer.check_camera)

    logger.info(
        "Monitoramento iniciado - verificando a cada %s segundos",
        CHECK_INTERVAL_SECONDS,
    )

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
