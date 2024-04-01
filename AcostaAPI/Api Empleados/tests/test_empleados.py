from fastapi import FastAPI

from fastapi.testclient import TestClient

app = FastAPI()

client = TestClient(app)

def test_read_index_emp():

    resp = client.get("/empleados")

    assert resp.status_code == 200

    assert resp.json() == {
        "status": "Success",
        "data": []
    }


def test_create_emp():
    resp = client.post(
        "/empleados/",
        headers={"X-Token": "A"},
        json={
            "id": 1,
            "nombre":"Prueba",
            "apellido":"Empleado",
            "edad":"18 años",
            "cargo":"Encargado",
            "salario":"1000bs"
        }
    )

    assert resp.status_code == 200

    assert resp.json() == {
        "id": 1,
        "value": 10
    }

def test_read_emp():
    resp = client.get(
        "/empleado/1/",
        headers={"X-Token": "A"}
    )

    assert resp.status_code == 200

    assert resp.json() == {
        "id": 1,
        "value": 10
    }
