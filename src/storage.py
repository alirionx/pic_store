import os
import datetime
import json
import io
import uuid
from minio import Minio
from PIL import Image


#-Some Globals--------------------------------------------
IMAGE_FORMAT = "jpeg"
THUMB_TAG = "thumb"
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
    self.thumbs_path = "./data/thumbs"

    if os.environ.get("FILESYSTEM_PICS_PATH"):
      self.pics_path = os.environ.get("FILESYSTEM_PICS_PATH")
    if os.environ.get("FILESYSTEM_THUMBS_PATH"):
      self.pics_path = os.environ.get("FILESYSTEM_THUMBS_PATH")

    self.check_data_dir()

  #-The Methods--------------------
  def check_data_dir(self):
    if not os.path.isdir(self.pics_path):
      os.makedirs(self.pics_path)
    if not os.path.isdir(self.thumbs_path):
      os.makedirs(self.thumbs_path)

  #----------------------
  def get_image_by_filename(self, filename:str, typ:str="picture"):
    if typ == "thumb":
      cur_path = self.thumbs_path
    else:
      cur_path = self.pics_path
    cur_file_path = os.path.join(cur_path, filename)
    item = os.stat(cur_file_path)
    new_item = {
      "filename": filename,
      "uploaded": int(item.st_mtime),
      "size": item.st_size,
    }
    return new_item

  #----------------------
  def list_images(self, typ:str="picture"):
    if typ == "thumb":
      cur_path = self.thumbs_path
    else:
      cur_path = self.pics_path

    res = os.listdir(cur_path)
    data = []
    for filename in res:
      cur_file_path = os.path.join(cur_path, filename)
      if not os.path.isfile(cur_file_path):
        continue
      item = os.stat(cur_file_path)
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
    
    filename = str(id) + "." + format
    image_path = os.path.join(self.pics_path, filename)
    thumb_path = os.path.join(self.thumbs_path, filename)
    
    with open(image_path, "wb") as fl:
      fl.write(image_payload)
    with open(thumb_path, "wb") as fl:
      fl.write(thumb_payload)

    return filename

  #----------------------
  def get_image_as_byte(self, filename:str, typ:str="picture"):
    if typ == "thumb":
      cur_path = self.thumbs_path
    else:
      cur_path = self.pics_path

    pic_path = os.path.join(cur_path, filename)
    with open(pic_path, "rb") as fl:
      yield from fl

  #----------------------
  def delete_image(self, filename:str):
    image_path = os.path.join(self.pics_path, filename)
    thumb_path = os.path.join(self.thumbs_path, filename)
    os.unlink(image_path)
    os.unlink(thumb_path)

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
    self.minio_pics_bucket = "pictures"
    self.minio_thumbs_bucket = "thumbs"
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
    if not self.minio_cli.bucket_exists(self.minio_pics_bucket):
      self.minio_cli.make_bucket(self.minio_pics_bucket)
    if not self.minio_cli.bucket_exists(self.minio_thumbs_bucket):
      self.minio_cli.make_bucket(self.minio_thumbs_bucket)

  #----------------------
  def get_image_by_filename(self, filename:str, typ:str="picture"):
    if typ == "thumb":
      cur_bucket = self.minio_thumbs_bucket
    else:
      cur_bucket = self.minio_pics_bucket

    res = self.minio_cli.stat_object(
      bucket_name=cur_bucket,
      object_name=filename
    )
    # print(res.__dict__)
    item = {
      "filename": filename,
      "uploaded": int(datetime.datetime.timestamp(res.__dict__["_last_modified"])), # Kleinigkeit ;)
      "size": res.__dict__["_size"]
    }
    return item

  #----------------------
  def list_images(self, typ:str="picture"):
    if typ == "thumb":
      cur_bucket = self.minio_thumbs_bucket
    else:
      cur_bucket = self.minio_pics_bucket

    res = self.minio_cli.list_objects(
      bucket_name=cur_bucket
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
    
    object_name = str(id) + "." + format
    
    self.minio_cli.put_object(
      bucket_name=self.minio_pics_bucket,
      object_name=object_name, 
      data=io.BytesIO(image_payload),
      length=len(image_payload)
    )
    self.minio_cli.put_object(
      bucket_name=self.minio_thumbs_bucket,
      object_name=object_name, 
      data=io.BytesIO(thumb_payload),
      length=len(thumb_payload)
    )
    return object_name
    
  #----------------------
  def get_image_as_byte(self, filename:str, typ:str="picture"):
    if typ == "thumb":
      cur_bucket = self.minio_thumbs_bucket
    else:
      cur_bucket = self.minio_pics_bucket

    res = self.minio_cli.get_object(
      object_name=filename,
      bucket_name=cur_bucket
    )
    # return res.read()
    return res

  #----------------------
  def delete_image(self, filename:str):
    self.minio_cli.remove_object(
      object_name=filename,
      bucket_name=self.minio_pics_bucket,
    )
    self.minio_cli.remove_object(
      object_name=filename,
      bucket_name=self.minio_thumbs_bucket,
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
    print("Storage Backend: " + self.storage_type)

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
    new_img = new_img.convert('RGB')
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
    new_img = new_img.convert('RGB')

    blo = io.BytesIO()
    new_img.save(blo, format=IMAGE_FORMAT)
    blo.seek(0)
    thumb_payload = blo.read()
    
    return image_payload, thumb_payload

#---------------------------------------------------------