from tests.database import client, session
import pytest
import schemas


@pytest.fixture
# @pytest.mark.parametrize(
#     "name, email, password",
#     [
#         ("user1", "user1@gmail.com", "password"),
#         ("user2", "user2@gmail.com", "password"),
#         ("user3", "user3@gmail.com", "password"),
#     ],
# )
# def default_users(client, name, email, password):
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
    # print(pagination)
    assert len(pagination["items"]) == params["size"]
    assert pagination["page"] == params["page"]
    assert res.status_code == 200
