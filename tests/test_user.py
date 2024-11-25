from tests.database import client, session
import pytest
import schemas
import jwt
import os
import auth

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


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


def test_create_user(client):
    res = client.post(
        "/user/",
        json={
            "name": "neverdup",
            "email": "neverdup@gmail.com",
            "password": "password",
        },
    )

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "neverdup@gmail.com"
    assert res.status_code == 201


@pytest.mark.parametrize(
    "page, size",
    [
        (1, 10),
        (2, 5),
        (3, 4),
    ],
)
def test_get_users(client, default_users, page, size):

    params = {"page": page, "size": size}
    res = client.get("/user", params=params)

    pagination = res.json()

    # print(type(pagination))
    assert len(pagination["items"]) == params["size"]
    assert pagination["page"] == params["page"]
    assert res.status_code == 200


def test_token(client, login_user):

    res = client.post(
        "/auth/token",
        data={
            "username": login_user["email"],
            "password": login_user["password"],
        },
    )

    login_res = auth.Token(**res.json())
    payload = jwt.decode(login_res.access_token, SECRET_KEY, algorithms=[ALGORITHM])
    eamil = payload.get("sub")
    assert eamil == login_user["email"]
    assert login_res.token_type == "bearer"
    assert res.status_code == 200
