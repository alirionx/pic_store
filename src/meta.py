import os
import datetime
import json
import couchdb



#-Some Globals--------------------------------------------



#---------------------------------------------------------
class FileSystem:

  #-Init object-----------------------
  def __init__(self):
    self.storage_type = "FileSystem"
    self.meta_dir = "./data/meta"
    self.meta_filename = "meta.json"

    if os.environ.get("FILESYSTEM_META_DIR"):
      self.meta_dir = os.environ.get("FILESYSTEM_META_DIR")
    self.meta_file_path = os.path.join(self.meta_dir, self.meta_filename)

    #-------------
    self.check_data_dir()


  #-The Methods----------------------------
  def check_data_dir(self):
    if not os.path.isdir(self.meta_dir):
      os.makedirs(self.meta_dir)

    json_chk = True
    try: 
      with open(self.meta_file_path, "r") as fl:
        json.loads(fl.read())
    except:
      json_chk = False

    if not os.path.isfile(self.meta_file_path) or not json_chk:
      with open(self.meta_file_path, "w") as fl:
        fl.write("[]")     

  #----------------------
  def write_pictures_data_to_fs(self, data:list):
    with open(self.meta_file_path, "w") as fl:
      res = json.dumps(data, indent=2)
      fl.write(res)

  #----------------------
  def get_pictures_meta(self):
    with open(self.meta_file_path, "r") as fl:
      data = json.loads(fl.read())
    return data

  #----------------------
  def get_picture_meta(self, filename:str):
    with open(self.meta_file_path, "r") as fl:
      data = json.loads(fl.read())
    res = [i for i in data if i["filename"] == filename]
    return res[0]

  #----------------------
  def add_picture_meta(self, data:dict):
    pictures_data = self.get_pictures_meta()
    pictures_data.append(data)
    self.write_pictures_data_to_fs(data=pictures_data)

  #----------------------
  def update_picture_meta(self, filename:str, data:dict):
    pictures_data = self.get_pictures_meta()
    for item in pictures_data:
      if item["filename"] == filename:
        pictures_data[pictures_data.index(item)] = data
        break
    self.write_pictures_data_to_fs(data=pictures_data)
    
  #----------------------
  def delete_picture_meta(self, filename:str):
    pictures_data = self.get_pictures_meta()
    res = [i for i in pictures_data if not (i['filename'] == filename)] # NICE!!!
    if len(res) == len(pictures_data):
      raise Exception("item with filename '%s' not found" %filename)
    self.write_pictures_data_to_fs(data=res)

  #----------------------
  
  #----------------------


#---------------------------------------------------------
class CouchDb:

  #-Init object-----------------------
  def __init__(self):
    self.storage_type = "CouchDB - Doc Database"
    self.couchdb_server = "localhost"
    self.couchdb_port = 5984
    self.couchdb_tls = False    
    self.couchdb_user = "couchdb"    
    self.couchdb_password = "couchdb"    
    self.couchdb_database = "pictures"    
    
    self.couch_connection_str = None
    self.couch_cli = None

    self.data = [] 

    self.check_envs()
    self.create_connection_str()
    self.build_couch_cli()
    self.check_db()


  #-The Methods--------------------
  def check_envs(self):
    env_list = []
    for key,val in self.__dict__.items():
      if key.startswith("couchdb"):
        env_list.append(key.upper())
    
    for env in env_list:
      if os.environ.get(env):
        setattr(self, env.lower(), os.environ.get(env))
    # print(self.__dict__.items())

  #----------------------
  def create_connection_str(self):
    if self.couchdb_tls: 
      proto = "https"
    else: 
      proto = "http"
    if self.couchdb_user and self.couchdb_password: 
      creds = "%s:%s@" %(self.couchdb_user, self.couchdb_password)
    else: 
      creds = ""

    self.couch_connection_str = "%s://%s%s:%s/" %(
      proto, creds, self.couchdb_server, self.couchdb_port
    )

  #----------------------
  def build_couch_cli(self):
    self.couch_cli = couchdb.Server(self.couch_connection_str)

  #----------------------
  def check_db(self):
    if self.couchdb_database not in self.couch_cli:
      db = self.couch_cli.create(self.couchdb_database)

  #----------------------
  def get_pictures_meta(self):
    data = []
    db = self.couch_cli[self.couchdb_database]
    for id in db:
      data.append(dict(db[id]))
    return data
  
  #----------------------
  def get_picture_meta(self, filename:str):
    db = self.couch_cli[self.couchdb_database]
    for id in db:
      id = db[id]["filename"].split(".")[0]
      if db[id]["filename"] == filename:
        return dict(db[id])
    raise Exception("item '%s' not found." %filename)
    
  #----------------------
  def add_picture_meta(self, data:dict):
    id = data["filename"].split(".")[0]
    db = self.couch_cli[self.couchdb_database]
    db[id] = data

  #----------------------
  def update_picture_meta(self, filename:str, data:dict):
    id = data["filename"].split(".")[0]
    db = self.couch_cli[self.couchdb_database]
    db[id] = db[id] | data  # UIUIUIUIUIU

  #----------------------
  def delete_picture_meta(self, filename:str):
    id = filename.split(".")[0]
    db = self.couch_cli[self.couchdb_database]
    if id not in db:
      raise Exception("item '%s' not found." %filename)
    db.delete(db[id])

  #----------------------
  #----------------------
  #----------------------
  

#---------------------------------------------------------
if os.environ.get("META_BACKEND") == "couchdb":
  StorageType = CouchDb
else:
  StorageType = FileSystem
  
#-------------------------------------
class MetaStore(StorageType):

  def __init__(self):
    super().__init__()
    print("Meta Backend: " + self.storage_type)
  
  
  #----------------------
  


#---------------------------------------------------------