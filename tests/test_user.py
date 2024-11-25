import pytest
import schemas
import jwt
import os
import auth

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


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
