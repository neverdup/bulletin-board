from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board"


engine = create_engine(
    "postgresql://postgres:mysecretpassword@localhost:15432/bulletin-board-test"
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def login_user(client):
    user_data = {
        "name": "neverdup",
        "email": "neverdup@gmail.com",
        "password": "password",
    }

    res = client.post("/user/", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]

    return new_user


@pytest.fixture()
def default_users(client):

    NO_OF_USERS = 20
    users = [
        (f"user{i:02d}", f"user{i:02d}@gmail.com", "password")
        for i in range(NO_OF_USERS)
    ]
    for user in users:
        res = client.post(
            "/user/",
            json={
                "name": user[0],
                "email": user[1],
                "password": user[2],
            },
        )
    return users
    # new_user = schemas.UserOut(**res.json())
    # assert new_user.email == "neverdup@gmail.com"
    # assert res.status_code == 201
