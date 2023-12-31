from uuid import uuid4
from tests.conftest import create_test_auth_headers_for_user


async def test_delete_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }

    await create_user_in_database(**user_data)
    resp = client.delete(
        f"/user/?user_id={user_data['user_id']}",
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    assert resp.json() == {"deleted_user_id": str(user_data["user_id"])}
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data["name"]
    assert user_from_db["surname"] == user_data["surname"]
    assert user_from_db["email"] == user_data["email"]
    assert user_from_db["is_active"] is False
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_delete_user_not_found(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }

    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 404
    assert resp.json() == {"detail": f"User with id {user_id} not found."}


async def test_delete_user_unauth(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }

    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.delete(
        f"/user/?user_id={user_id}",
        headers=create_test_auth_headers_for_user(user_data["email"] + "u")
    )
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


