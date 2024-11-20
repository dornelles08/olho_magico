"""
Este módulo contém funções para download de imagens de câmeras.

O módulo fornece funcionalidades para:
- Download de imagens de endpoints de câmera via HTTP
- Conversão de bytes para formato numpy array
- Tratamento de erros durante o download

Dependências:
    - numpy
    - requests
    - opencv-python (cv2)
"""

import cv2
import numpy as np
import requests


def download_image(camera_endpoint, logger):
    """
    Faz o download de uma imagem do endpoint da câmera.
    Returns:
        numpy.ndarray: Imagem em formato numpy array (BGR) se o download for bem-sucedido.
        None: Se ocorrer um erro no download.
    """

    try:
        response = requests.get(camera_endpoint, timeout=5)
        response.raise_for_status()

        # Converter a resposta em uma imagem
        image_array = np.asarray(bytearray(response.content), dtype=np.uint8)
        image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        return image
    except Exception as e:
        logger.error("Erro ao baixar imagem: %s", str(e))
        return None
