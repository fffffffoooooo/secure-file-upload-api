import io
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
import uuid

def register_and_login():
    email = f"testuser_{uuid.uuid4()}@example.com"
    password = "Password123!"

    client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    return response.json()["access_token"]




def test_upload_without_token():
    """Upload sans authentification → doit échouer"""
    file_content = b"fake pdf content"
    files = {
        "file": ("test.pdf", io.BytesIO(file_content), "application/pdf")
    }

    response = client.post("/files/upload", files=files)

    assert response.status_code == 401


def test_upload_with_valid_token():
    """Upload avec token valide → doit réussir"""
    token = register_and_login()

    file_content = b"fake pdf content"
    files = {
        "file": ("test.pdf", io.BytesIO(file_content), "application/pdf")
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/files/upload", files=files, headers=headers)

    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.pdf"
    assert data["content_type"] == "application/pdf"


def test_upload_invalid_file_type():
    """Upload d’un type interdit → doit échouer"""
    token = register_and_login()

    file_content = b"fake exe content"
    files = {
        "file": ("virus.exe", io.BytesIO(file_content), "application/octet-stream")
    }

    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/files/upload", files=files, headers=headers)

    assert response.status_code == 400
