
import sys
import os
import time
import json
import asyncio

from datetime import datetime

import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import status as HTTPStatus
from fastapi.responses import StreamingResponse 
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, validator
from typing import Literal

from storage import PicStore, IMAGE_FORMAT, THUMB_TAG
from meta import MetaStore

#-Models-------------------------------------------------------
class Picture(BaseModel):
  filename: str
  uploaded: int
  size: int

class Meta(BaseModel):
  filename: str
  name: str | None = None
  location: str | None = None
  date: str | None = None
  comment: str | None = None
  album: str | None = None
  format: Literal["Landscape", "Portrait", "Square"] | None = None

  # @validator("title")
  # def validate_no_sql_injection(cls, value):
  #   if "delete from" in value:
  #     raise ValueError("Our terms strictly prohobit SQLInjection Attacks")
  #   return value


#-Build and prep the App----------------------------------------
app = FastAPI()
app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_methods=["*"],
  allow_headers=["*"],
  allow_credentials=True
)


#-Initial Things-------------------------------------------------
@app.on_event("startup")
def startup_event():
  global myMetaStore
  global myPicStore
  myMetaStore = MetaStore()
  myPicStore = PicStore()


#-The Routes----------------------------------------------------
@app.get("/api/", tags=["api_root"])
async def api_root():
  data = {
    "message": "Hello from the Pic Store API",
    "timestamp": int(time.time())
  }
  return data

#--------------------
@app.get("/api/pictures", tags=["storage"], response_model=list[Picture])
@app.get("/api/thumbs", tags=["storage"], response_model=list[Picture])
async def api_images_get(request: Request):
  if "thumb" in str(request.url): typ = "thumb"
  else: typ = "picture"

  data = myPicStore.list_images(typ=typ)
  return data

#--------------------
@app.get("/api/picture/{filename}", tags=["storage"], response_model=Picture)
@app.get("/api/thumb/{filename}", tags=["storage"])
def api_image_get(filename, request: Request):
  if "thumb" in str(request.url): typ = "thumb"
  else: typ = "picture"

  res = myPicStore.get_image_by_filename(filename=filename)
  return res

#--------------------
@app.get("/api/dl/picture/{filename}", tags=["storage"])
@app.get("/api/dl/thumb/{filename}", tags=["storage"])
def api_image_get(filename, request: Request):
  if "thumb" in str(request.url): typ = "thumb"
  else: typ = "picture"

  try:
    stream = myPicStore.get_image_as_byte(filename=filename, typ=typ)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))
  return StreamingResponse(stream, media_type="image/%s" %IMAGE_FORMAT)


#--------------------
@app.post("/api/picture", tags=["storage"])
async def api_pictures_post(file: UploadFile):
  payload = await file.read()
  image_payload, thumb_payload = myPicStore.convert_picture(payload=payload)
  new_filename = myPicStore.save_picture(image_payload=image_payload, thumb_payload=thumb_payload)

  myMetaStore.add_picture_meta( {"filename": new_filename } )

  new_item = {
    "picture": myPicStore.get_image_by_filename(filename=new_filename),
    "thumb": myPicStore.get_image_by_filename(filename=new_filename, typ="thumb")
  }
  return new_item

#--------------------
@app.delete("/api/image/{filename}", tags=["storage"])
def api_image_delete(filename):
  try:
    myPicStore.delete_image(filename=filename)
    myMetaStore.delete_picture_meta(filename=filename)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))

  return filename

#--------------------
@app.get("/api/meta", tags=["meta"], response_model=list[Meta])
async def api_meta_get():
  data = myMetaStore.get_pictures_meta()
  return data

#--------------------
@app.get("/api/meta/{filename}", tags=["meta"])
async def api_meta_item_get(filename):
  try:
    data = myMetaStore.get_picture_meta(filename=filename)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))
  return data

#--------------------
@app.post("/api/meta", tags=["meta"])
async def api_meta_item_post(item:Meta):
  filename_list = []
  images_data = myPicStore.list_images()
  for img in images_data:
    filename_list.append(img["filename"])
  if item.filename not in filename_list:
    msg = "picture with filename '%s' does not exsist." %item.filename
    return HTTPException(status_code=400, detail=msg)
  
  data = myMetaStore.add_picture_meta(data=dict(item))
  return item

#--------------------
@app.put("/api/meta/{filename}", tags=["meta"])
async def api_meta_item_post(filename, item:Meta):
  filename_list = []
  images_data = myPicStore.list_images()
  for img in images_data:
    filename_list.append(img["filename"])
  if item.filename not in filename_list:
    msg = "picture with filename '%s' does not exsist." %item.filename
    return HTTPException(status_code=400, detail=msg)
  
  myMetaStore.update_picture_meta(filename=filename, data=dict(item))
  return item

#--------------------
@app.delete("/api/meta/{filename}", tags=["meta"])
async def api_meta_item_post(filename):
  try:
    myMetaStore.delete_picture_meta(filename=filename)
  except Exception as e:
    return HTTPException(status_code=400, detail=str(e))
  
  return filename

#--------------------


#--------------------
#--------------------

#-------------------------------------------
base_path = os.path.abspath("./")
spa_dir = "spa"
spa_path = os.path.join(base_path, spa_dir)

if not os.path.isdir(spa_path):
  os.makedirs(spa_path)
info_file_path = os.path.join(spa_path, "index.html")

if not os.path.isfile(info_file_path):
  with open(info_file_path, "w") as fl:
    fl.write("<h2>Don't forget to compile the SPA and copy it here</h2>")

app.mount("/", StaticFiles(directory=spa_path, html=True), name="static")

#-------------------------------------------




#-The Runner---------------------------------------------------------
if __name__ == "__main__":

  if "dev".lower() in sys.argv:
    print("Dev Mode")
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=5000, reload=True)
  else:
    print("Prod Mode")
    uvicorn.run(app="__main__:app", host="0.0.0.0", port=5000)