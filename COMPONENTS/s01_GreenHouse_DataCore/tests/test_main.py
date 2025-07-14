from starlette.testclient import TestClient
from app.main import app  # Ajusta esta ruta si es diferente

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.text == "Hello, its working"
    assert response.headers["content-type"] == "text/plain; charset=utf-8"
