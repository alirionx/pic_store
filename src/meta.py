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
    self.meta_path = "./data/meta"

    if os.environ.get("FILESYSTEM_META_PATH"):
      self.meta_path = os.environ.get("FILESYSTEM_META_PATH")

    self.check_data_dir()

  #-The Methods--------------------
  def check_data_dir(self):
    if not os.path.isdir(self.meta_path):
      os.makedirs(self.meta_path)

  #----------------------
  #----------------------
  #----------------------


#---------------------------------------------------------
class CouchDb:

  #-Init object-----------------------
  def __init__(self):
    self.storage_type = "CouchDB - Doc Database"
    self.couchdb_server = "localhost"
    self.couchdb_port = 9000
    self.couchdb_tls = False    
    self.couchdb_user = "couchdb"    
    self.couchdb_password = "couchdb"    
    self.couchdb_database = "pictures"    
    self.couchdb_cli = None

  #-The Methods--------------------

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


#---------------------------------------------------------