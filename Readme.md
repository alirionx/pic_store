## A K8s example stack
### It can store, convert and manage images/pictures incl. metadate  
### It comes with a swagger api and a simple JSX WebUI/SPA

### Used tools/frameworks:
* python
* minio
* couchdb
* fastapi
* vueJS

<br>

### Docker data volume path:
/app/data

<br>

### App/Docker Environment Vars:
* STORAGE_BACKEND ["filesystem"* | "minio"]
* META_BACKEND ["filesystem"* | "couchdb"]

* FILESYSTEM_PICS_PATH "./data/pics"*
* FILESYSTEM_THUMBS_PATH "./data/thumbs"*
* MINIO_SERVER "localhost"*
* MINIO_PORT 9000*
* MINIO_TLS False*
* MINIO_USER "minio"*
* MINIO_PASSWORD "minio"*
* MINIO_PICS_BUCKET "pictures"*
* MINIO_THIMBS_BUCKET "thumbs"*

* COUCHDB_SERVER "localhost"*
* COUCHDB_PORT 5984*
* COUCHDB_TLS False*
* COUCHDB_USER "couchdb"*
* COUCHDB_PASSWORD "couchdb"*
* COUCHDB_DATABASE "pictures"*



\* default