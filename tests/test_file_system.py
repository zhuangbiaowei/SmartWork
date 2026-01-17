import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import tempfile
import shutil

import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "src" / "backend"))

from main import app

client = TestClient(app)


@pytest.fixture
def temp_dir():
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)


def test_list_files(temp_dir):
    test_file = temp_dir / "test.txt"
    test_content = "test"
    test_file.write_text(test_content)

    response = client.get(f"/api/files/list/?path={temp_dir}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "test.txt"
    assert data[0]["is_dir"] == False
    assert data[0]["size"] == len(test_content)


def test_read_file(temp_dir):
    test_file = temp_dir / "test_read.txt"
    test_content = "读取测试"
    test_file.write_text(test_content)

    response = client.get(f"/api/files/read/?path={test_file}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == test_content


def test_write_file(temp_dir):
    test_file = temp_dir / "test_write.txt"
    test_content = "写入测试"

    response = client.post(
        f"/api/files/write/?path={test_file}", json={"content": test_content}
    )
    assert response.status_code == 200
    assert test_file.exists()
    assert test_file.read_text() == test_content


def test_delete_file(temp_dir):
    test_file = temp_dir / "test_delete.txt"
    test_file.write_text("删除测试")

    response = client.delete(f"/api/files/delete/?path={test_file}")
    assert response.status_code == 200
    assert not test_file.exists()


def test_nonexistent_path():
    response = client.get("/api/files/list/?path=/nonexistent/path")
    assert response.status_code in [404, 500]


def test_list_root():
    response = client.get("/api/files/list/?path=.")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
