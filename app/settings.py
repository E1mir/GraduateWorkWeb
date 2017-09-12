import urllib

DEBUG = True
USER = "coolproger97@gmail.com"
PASSWORD = "graduatework2017"
DB_PASS = "LXlHIUPxo2r18sBv"
S_KEY = 'ThisIsMyGraduationWork:"WarehouseManagementSystem"'
PERMISSIONS = ["admin", "default"]
SMTP = {"HOST": "smtp.gmail.com", "PORT": 587}
TEMPLATE_FOLDER = "files/templates"
STATIC_FOLDER = "files/static"
DB_CONNECTION_STRING = "mongodb://{}:{}" \
                       "@wms-shard-00-00-nkihn.mongodb.net:27017," \
                       "wms-shard-00-01-nkihn.mongodb.net:27017," \
                       "wms-shard-00-02-nkihn.mongodb.net:27017/" \
                       "test?ssl=true&replicaSet=wms-shard-0&authSource=admin".format("kryternext",
                                                                                      urllib.quote(DB_PASS)
                                                                                      )
