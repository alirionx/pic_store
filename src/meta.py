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
    
    self.data = []

    if os.environ.get("FILESYSTEM_META_DIR"):
      self.meta_dir = os.environ.get("FILESYSTEM_META_DIR")
    self.meta_file_path = os.path.join(self.meta_dir, self.meta_filename)

    #-------------
    self.check_data_dir()
    self.load_pictures_meta()


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
  def load_pictures_meta(self):
    with open(self.meta_file_path, "r") as fl:
      self.data = json.loads(fl.read())
    
  #----------------------
  def save_pictures_meta(self):
    with open(self.meta_file_path, "w") as fl:
      res = json.dumps(self.data, indent=2)
      fl.write(res)

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
    self.load_pictures_meta()


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
  def load_pictures_meta(self):
    db = self.couch_cli[self.couchdb_database]
    for id in db:
      self.data.append(dict(db[id]))
    
  #----------------------
  def save_pictures_meta(self):
    db = self.couch_cli[self.couchdb_database]
    tmp_id_list = []
    for item in self.data:
      id = item["filename"].split(".")[0]
      tmp_id_list.append(id)
      if id in db:
        db[id] = db[id] | item  # UIUIUIUIUIU
      else: db[id] = item
    
    print(tmp_id_list)
    db = self.couch_cli[self.couchdb_database]
    for id in db:
      if id not in tmp_id_list:
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
    print(self.storage_type)
  
  #----------------------
  def list_picture_meta(self):
    return self.data

  #----------------------
  def add_picture_meta(self, data:dict):
    self.data.append(data)
    self.save_pictures_meta()
    
  #----------------------
  def update_picture_meta(self, filename:str, data:dict):
    for item in self.data:
      if item["filename"] == filename:
        self.data[self.data.index(item)] = data
        break
    self.save_pictures_meta()
  
  #----------------------
  def delete_picture_meta(self, filename:str):
    res = [i for i in self.data if not (i['filename'] == filename)] # NICE!!!
    self.data = res
    self.save_pictures_meta()


#---------------------------------------------------------