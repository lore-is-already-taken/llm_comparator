import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = "protoai"


class MongoHandler:
    """docstring for MongoHandler."""

    def __init__(self, username, password):
        uri = f"mongodb://{username}:{password}@{MONGO_HOST}:{MONGO_PORT}"
        self.client = MongoClient(uri)
        self.db = self.client[MONGO_DB]

    def save_doc(self, doc):
        collection = self.db["images"]

        try:
            result = collection.insert_one(doc)
            print(f"Document inserted with ID: {result.inserted_id}")
            return str(result.inserted_id)

        except Exception as e:
            raise e

    def check_if_exist(self, hash):
        collection = self.db["images"]
        # exists = collection.count_documents({"hash": hash}) > 0
        exists = collection.find_one({"hash": hash}) is not None
        if exists:
            print("Document exists")
            return exists
        else:
            print("Document does not exist")
            return False

    def list_collections(self):
        try:
            collection_names = self.db.list_collection_names()
            print(
                f"Colecciones en la base de datos '{self.db.name}': {collection_names}"
            )
            return collection_names
        except Exception as e:
            print(f"Error al listar colecciones: {e}")
            return []

    def get_all_data_from_collection(self, collection_name: str):
        """
        Recupera todos los documentos de una colección específica.

        :param collection_name: El nombre de la colección de la cual obtener los datos.
        :return: Una lista de diccionarios, donde cada diccionario es un documento.
                 Retorna una lista vacía si la colección no existe, está vacía o hay un error.
        """
        try:
            # Opcional: Verificar si la colección existe antes de intentar leerla
            if collection_name not in self.db.list_collection_names():
                print(
                    f"Advertencia: La colección '{collection_name}' no existe en la base de datos '{self.db.name}'."
                )
                return []

            collection = self.db[collection_name]
            # El filtro vacío {} significa "seleccionar todos los documentos"
            cursor = collection.find({})
            # Convertir el cursor a una lista de documentos
            documents = list(cursor)

            print(
                f"Se encontraron {len(documents)} documentos en la colección '{collection_name}'."
            )
            return documents
        except Exception as e:
            print(f"Error al obtener datos de la colección '{collection_name}': {e}")
            return []
