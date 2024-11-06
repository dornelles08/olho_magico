import os
import shutil
from datetime import datetime

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

# Criar pasta de upload se não existir
UPLOAD_DIR = "known_faces"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)


@app.post("/upload-face/")
async def upload_face(name: str, file: UploadFile = File(...)):
    try:
        # Validar se é uma imagem
        if not file.content_type.startswith("image/"):
            return JSONResponse(
                status_code=400,
                content={"message": "O arquivo deve ser uma imagem"}
            )

        # Gerar nome único para o arquivo
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_extension = os.path.splitext(file.filename)[1]
        new_filename = f"{name}_{timestamp}{file_extension}"

        # Caminho completo onde a imagem será salva
        file_path = os.path.join(UPLOAD_DIR, new_filename)

        # Salvar o arquivo
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "message": "Imagem enviada com sucesso",
            "filename": new_filename,
            "filepath": file_path
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"message": f"Erro ao fazer upload da imagem: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
