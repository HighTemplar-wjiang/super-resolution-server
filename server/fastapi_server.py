import os
import aiofiles
from typing import List
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse

from server_path import *
from super_resolution import SuperResolution

# Server app.
app = FastAPI()

# Models.
sr_model = SuperResolution("fsrcnn", 3)


#
# @app.post("/files/")
# async def create_files(files: List[bytes] = File(...)):
#
#     for file in files:
#         pass
#     return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfile/")
async def create_upload_file(image: UploadFile = File(...)):

    # Write file to cache.
    async with aiofiles.open(os.path.join(cache_path, image.filename), "wb") as cache_file:
        while True:
            content = await image.read(1024)
            if content:
                await cache_file.write(content)
            else:
                break
    print(f"[INFO] File {image.filename} cached.")

    # Invoke super resolution.
    output_sr_filename = await sr_model.super_sample(image.filename)
    if output_sr_filename:
        return FileResponse(os.path.join(cache_path, output_sr_filename))
    else:
        return {"Error": "Processed failed."}


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <input name="image" type="file" accept="image/*">
    <input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
