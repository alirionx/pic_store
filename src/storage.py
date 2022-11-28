import os
import datetime
import json
import io
import uuid
from minio import Minio
from PIL import Image


#-Some Globals--------------------------------------------
IMAGE_FORMAT = "jpeg"
IMAGE_MAX_WIDTH = 1920
IMAGE_MAX_HEIGHT = 1080
THUMB_MAX_WIDTH = 480
THUMB_MAX_HEIGHT = 360


#---------------------------------------------------------
class FileSystem:

  #-Init object-----------------------
  def __init__(self):
    self.storage_type = "FileSystem"
    self.pics_path = "./data/pics"

    if os.environ.get("FILESYSTEM_PICS_PATH"):
      self.pics_path = os.environ.get("FILESYSTEM_PICS_PATH")

    self.check_data_dir()

  #-The Methods--------------------
  def check_data_dir(self):
    if not os.path.isdir(self.pics_path):
      os.makedirs(self.pics_path)

  #----------------------
  def list_pictures(self):
    res = os.listdir(self.pics_path)
    data = []
    for filename in res:
      cur_path = os.path.join(self.pics_path, filename)
      if not os.path.isfile(cur_path):
        continue
      item = os.stat(cur_path)
      new_item = {
        "filename": filename,
        "uploaded": int(item.st_mtime),
        "size": item.st_size,
      }
      data.append(new_item)
    return data

  #----------------------
  def save_picture(self, image_payload:bytes, thumb_payload:bytes, id:str=None, format:str=IMAGE_FORMAT):
    if not id:
      id = uuid.uuid4()
    
    image_filename = str(id) + "." + format
    thumb_filename = str(id) + ".thumb." + format
    image_path = os.path.join(self.pics_path, image_filename)
    thumb_path = os.path.join(self.pics_path, thumb_filename)
    
    with open(image_path, "wb") as fl:
      fl.write(image_payload)
    with open(thumb_path, "wb") as fl:
      fl.write(thumb_payload)

  #----------------------
  def get_picture_as_byte(self, filename:str):
    pic_path = os.path.join(self.pics_path, filename)
    with open(pic_path, "rb") as fl:
      stream = fl.read()
    return stream

  #----------------------
  def delete_picture(self, filename:str):
    pic_path = os.path.join(self.pics_path, filename)
    os.unlink(pic_path)

  #----------------------
  #----------------------
  #----------------------
    

#---------------------------------------------------------
class MinIo:

  #-Init object-----------------------
  def __init__(self):
    self.storage_type = "Minio - Object Storage"
    self.minio_server = "localhost"
    self.minio_port = 9000
    self.minio_tls = False    
    self.minio_user = "minio"    
    self.minio_password = "minio"    
    self.minio_bucket = "pictures"    
    self.minio_cli = None

    #--------------
    self.check_envs()
    self.build_minio_cli()
    self.check_bucket()

  #-The Methods-----------------------
  def check_envs(self):
    env_list = []
    for key,val in self.__dict__.items():
      if key.startswith("minio"):
        env_list.append(key.upper())
    
    for env in env_list:
      if os.environ.get(env):
        setattr(self, env.lower(), os.environ.get(env))
    # print(self.__dict__.items())

  #----------------------
  def build_minio_cli(self):
    self.minio_cli = Minio(
      "%s:%s" %(self.minio_server, int(self.minio_port)),
      access_key = self.minio_user,
      secret_key = self.minio_password,
      secure=bool(self.minio_tls)
    )
  
  #----------------------
  def check_bucket(self):
    res = self.minio_cli.list_buckets()
    # print(res)
    if not self.minio_cli.bucket_exists(self.minio_bucket):
      self.minio_cli.make_bucket(self.minio_bucket)

  #----------------------
  def list_pictures(self):
    res = self.minio_cli.list_objects(
      bucket_name=self.minio_bucket
    )
    data = []
    for item in res:
      new_item = {
        "filename": item.__dict__["_object_name"],
        "uploaded": int(datetime.datetime.timestamp(item.__dict__["_last_modified"])), # Kleinigkeit ;)
        "size": item.__dict__["_size"]
      }
      data.append(new_item)
    return data

  #----------------------
  def save_picture(self, image_payload:bytes, thumb_payload:bytes, id:str=None, format:str=IMAGE_FORMAT):
    if not id:
      id = uuid.uuid4()
    
    image_object_name = str(id) + "." + format
    thumb_object_name = str(id) + ".thumb." + format
    self.minio_cli.put_object(
      bucket_name=self.minio_bucket,
      object_name=image_object_name, 
      data=io.BytesIO(image_payload),
      length=len(image_payload)
    )
    self.minio_cli.put_object(
      bucket_name=self.minio_bucket,
      object_name=thumb_object_name, 
      data=io.BytesIO(thumb_payload),
      length=len(thumb_payload)
    )
    
  #----------------------
  def get_picture_as_byte(self, filename:str):
    res = self.minio_cli.get_object(
      object_name=filename,
      bucket_name=self.minio_bucket
    )
    return res.read()

  #----------------------
  def delete_picture(self, filename:str):
    self.minio_cli.remove_object(
      object_name=filename,
      bucket_name=self.minio_bucket,
    )

  #---------------------- 
  #----------------------



#---------------------------------------------------------
if os.environ.get("STORAGE_BACKEND") == "minio":
  StorageType = MinIo
else:
  StorageType = FileSystem
  
#-------------------------------------
class PicStore(StorageType):

  def __init__(self):
    super().__init__()
    print(self.storage_type)

  def convert_picture(self, payload:bytes):
    img = Image.open(io.BytesIO(payload))

    if img.width >= img.height:
      resize_factor = img.height / img.width
      if img.width > IMAGE_MAX_WIDTH: 
        new_width = IMAGE_MAX_WIDTH
      else:
        new_width = img.width
      new_height = int(new_width * resize_factor)
    else:
      resize_factor = img.width / img.height
      if img.height > IMAGE_MAX_HEIGHT: 
        new_height = IMAGE_MAX_HEIGHT
      else:
        new_height = img.height
      new_width = int(new_height * resize_factor)

    new_img = img.resize( (new_width, new_height) )
    blo = io.BytesIO()
    new_img.save(blo, format=IMAGE_FORMAT)
    blo.seek(0)
    image_payload = blo.read()
    # print(len(new_payload))

    #--------------------------
    if img.width >= img.height:
      resize_factor = img.height / img.width
      new_width = THUMB_MAX_WIDTH
      new_height = int(new_width * resize_factor)
    else:
      resize_factor = img.width / img.height
      new_height = IMAGE_MAX_HEIGHT
      new_width = int(new_height * resize_factor)

    new_img = img.resize( (new_width, new_height) )

    blo = io.BytesIO()
    new_img.save(blo, format=IMAGE_FORMAT)
    blo.seek(0)
    thumb_payload = blo.read()
    
    return image_payload, thumb_payload

#---------------------------------------------------------