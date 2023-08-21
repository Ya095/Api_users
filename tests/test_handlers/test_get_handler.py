from uuid import uuid4
from tests.conftest import create_test_auth_headers_for_user


async def test_get_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@exemple.com",
        "is_active": True,
        "hashed_password": "SampleHashPass"
    }

    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    user_from_response = resp.json()
    assert user_from_response["user_id"] == str(user_data["user_id"])
    assert user_from_response["name"] == user_data["name"]
    assert user_from_response["surname"] == user_data["surname"]
    assert user_from_response["email"] == user_data["email"]
    assert user_from_response["is_active"] is True


# async def test_get_user_id_validation_error(client, create_user_in_database, get_user_from_database):
#     user_data = {
#         "user_id": uuid4(),
#         "name": "Egor",
#         "surname": "Yakovlev",
#         "email": "egor@exemple.com",
#         "is_active": True,
#         "hashed_password": "SampleHashPass"
#     }
#
#     await create_user_in_database(**user_data)
#     resp = client.get(f"/user/?user_id=123")
#     assert resp.status_code == 422
#     data_from_response = resp.json()
#     assert data_from_response == {
#         "detail": [
#             {
#                 "loc": ["query", "user_id"],
#                 "msg": "value is not a valid uuid",
#                 "type": "type_error.uuid",
#             }
#         ]
#     }


async def test_get_user_not_found(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@exemple.com",
        "is_active": True,
        "hashed_password": "SampleHashPass"
    }

    user_id_for_finding = uuid4()
    await create_user_in_database(**user_data)
    resp = client.get(
        f"/user/?user_id={user_id_for_finding}",
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id_for_finding} not found."}