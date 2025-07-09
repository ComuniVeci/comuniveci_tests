import pytest, os, requests
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# Generador de datos aleatorios
@pytest.fixture(scope="session")
def faker():
    return Faker()

# Cliente de prueba para hacer http requests
@pytest.fixture
def client():
    class TestClient:
        def __init__(self, base_url):
            self.base_url = base_url

        def post(self, endpoint, json):
            return requests.post(f"{self.base_url}{endpoint}", json=json)
        
        def get(self, endpoint, headers=None):
            return requests.get(f"{self.base_url}{endpoint}", headers=headers)

    return TestClient("http://localhost:8002")  # Cambia puerto si tu auth-service usa otro

# Limpia los usuarios antes de cada test
@pytest.fixture(autouse=True)
def clean_users():
    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME_TEST")
    client = MongoClient(mongo_uri)
    db = client[db_name]
    db["users"].delete_many({})

    yield  # Aquí se ejecuta el test

    # Opcional: limpieza post-test
    db["users"].delete_many({})
