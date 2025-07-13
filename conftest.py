import pytest, os, requests
from faker import Faker
from pymongo import MongoClient
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

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

###### LIMPIEZA BACK ######
# Lista global para rastrear correos de usuarios de prueba
created_test_users = []

# Fixture para registrar usuarios creados durante un test
@pytest.fixture
def track_created_user():
    def _track(email):
        created_test_users.append(email)
    return _track

# Limpieza después de la sesión de tests
@pytest.fixture(scope="session", autouse=True)
def cleanup_created_users():
    yield  # Esperar a que terminen los tests

    mongo_uri = os.getenv("MONGO_URI")
    db_name = os.getenv("DB_NAME")  # Usamos la base de datos real, no DB_NAME_TEST
    client = MongoClient(mongo_uri)
    db = client[db_name]
    for email in created_test_users:
        db["users"].delete_many({"email": email})

###### LIMPIEZA FRONT ######
@pytest.fixture(scope="session")
def tracked_users_frontend():
    return []

@pytest.fixture
def track_created_user_frontend(tracked_users_frontend):
    def tracker(email):
        tracked_users_frontend.append(email)
    return tracker

@pytest.fixture(scope="session", autouse=True)
def cleanup_frontend_users(request, tracked_users_frontend):
    def finalizer():
        if tracked_users_frontend:
            mongo_uri = os.getenv("MONGO_URI")
            db_name = os.getenv("DB_NAME")
            client = MongoClient(mongo_uri)
            db = client[db_name]
            db["users"].delete_many({"email": {"$in": tracked_users_frontend}})
    request.addfinalizer(finalizer)

@pytest.fixture
def browser():
    options = Options()
    options.add_argument("--start-maximized")
    # Opcional: ejecuta sin ventana
    # options.add_argument("--headless")
    
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()
