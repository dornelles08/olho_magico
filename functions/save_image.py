"""
Módulo responsável por salvar imagens processadas em disco.

Este módulo contém funções para salvar imagens que passaram por detecção
ou processamento, mantendo um registro temporal no nome do arquivo.

Functions:
    save_image: Salva uma imagem em disco com timestamp no nome do arquivo.
"""

import os
from datetime import datetime

import cv2


def save_image(image, images_dir, logger) -> str | None:
    """
    Salva a imagem com detecção em disco.
    Args:
        image: Imagem em formato numpy array (BGR)
    Returns:
        str: Caminho do arquivo salvo em caso de sucesso
        None: Em caso de erro ao salvar
    """

    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_path = os.path.join(images_dir, f"detection_{timestamp}.jpg")
        cv2.imwrite(image_path, image)
        return image_path
    except Exception as e:
        logger.error("Erro ao salvar imagem: %s", str(e))
        return None
