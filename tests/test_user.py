from fastapi.testclient import TestClient
from main import app
from database import get_db
from tests.database import override_get_db, engine
import models
import schemas


models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def test_create_user():
    res = client.post(
        "/user/",
        json={"name": "yjw", "email": "user@example.com", "password": "password"},
    )

    new_user = schemas.UserResponse(**res.json())
    assert new_user.email == "user@example.com"
    assert res.status_code == 201
