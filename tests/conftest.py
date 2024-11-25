import pytest


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
