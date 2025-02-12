from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse, FileResponse

app = FastAPI()


@app.post("/files")
async def upload_file(uploaded_file: UploadFile):
    file = uploaded_file.file
    filename = uploaded_file.filename
    with open(f"{filename}_1", "wb") as f:
        f.write(file.read())


@app.post("/several_files")
async def upload_files(uploaded_files: list[UploadFile]):
    for uploaded_file in uploaded_files:
        file = uploaded_file.file
        filename = uploaded_file.filename
        with open(f"{filename}_1", "wb") as f:
            f.write(file.read())


# загрузка файла на локальном хранилище
@app.get("/files/{filename}")
async def get_file(filename: str):
    return FileResponse(filename)

"""-----------------------------------------------"""

# загрузка стримингово файла с разбиением по чанкам
def iterfile(filaname: str):
    with open(filaname, "rb") as file:
        while chunk := file.read(1024 * 1024):
            yield chunk


@app.get("/files/streaming/{filename}")
async def get_streaming_file(filename: str):
    return StreamingResponse(iterfile(filename), media_type="video.mp4")