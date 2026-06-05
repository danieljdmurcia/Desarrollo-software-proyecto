from fastapi.testclient import TestClient
from Backend.main import app

client = TestClient(app)

def test_home():
    response = client.get("/")
    assert response.status_code == 200

def test_sobre_nosotros():
    response = client.get("/sobre-nosotros")
    assert response.status_code == 200

def test_obtener_productos():
    response = client.get("/api/productos")
    assert response.status_code == 200

def test_crear_producto():
    response = client.post("/api/productos", json={
        "nombre": "Anillo de prueba",
        "precio": 150000.0,
        "disponible": True
    })
    assert response.status_code == 200

def test_producto_no_existe():
    response = client.get("/api/productos/99999")
    assert response.status_code == 404