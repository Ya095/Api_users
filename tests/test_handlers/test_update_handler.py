import json
from uuid import uuid4
from tests.conftest import create_test_auth_headers_for_user


async def test_update_user(client, create_user_in_database, get_user_from_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }

    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@example.com",
    }

    await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data["user_id"])
    users_from_db = await get_user_from_database(user_data["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data["is_active"]
    assert user_from_db["user_id"] == user_data["user_id"]


async def test_update_user_check_only_one_was_updated(client, create_user_in_database, get_user_from_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }
    user_data_3 = {
        "user_id": uuid4(),
        "name": "Petr",
        "surname": "Petr",
        "email": "petr@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }
    user_data_updated = {
        "name": "Nikifor",
        "surname": "Nikiforov",
        "email": "nik@example.com",
    }

    for user_data in [user_data_1, user_data_2, user_data_3]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 200
    resp_data = resp.json()
    assert resp_data["updated_user_id"] == str(user_data_1["user_id"])
    users_from_db = await get_user_from_database(user_data_1["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_updated["name"]
    assert user_from_db["surname"] == user_data_updated["surname"]
    assert user_from_db["email"] == user_data_updated["email"]
    assert user_from_db["is_active"] is user_data_1["is_active"]
    assert user_from_db["user_id"] == user_data_1["user_id"]

    # проверка, что другие пользователи не изменились
    users_from_db = await get_user_from_database(user_data_2["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_2["name"]
    assert user_from_db["surname"] == user_data_2["surname"]
    assert user_from_db["email"] == user_data_2["email"]
    assert user_from_db["is_active"] is user_data_2["is_active"]
    assert user_from_db["user_id"] == user_data_2["user_id"]

    users_from_db = await get_user_from_database(user_data_3["user_id"])
    user_from_db = dict(users_from_db[0])
    assert user_from_db["name"] == user_data_3["name"]
    assert user_from_db["surname"] == user_data_3["surname"]
    assert user_from_db["email"] == user_data_3["email"]
    assert user_from_db["is_active"] is user_data_3["is_active"]
    assert user_from_db["user_id"] == user_data_3["user_id"]


async def test_update_user_not_found_error(client, create_user_in_database):
    user_data = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }

    user_data_updated = {
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivanov@example.com",
    }
    await create_user_in_database(**user_data)
    user_id = uuid4()
    resp = client.patch(
        f"/user/?user_id={user_id}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data["email"])
    )
    assert resp.status_code == 404
    resp_data = resp.json()
    assert resp_data == {"detail": f"User with id {user_id} not found."}


async def test_update_user_duplicate_email_error(client, create_user_in_database):
    user_data_1 = {
        "user_id": uuid4(),
        "name": "Egor",
        "surname": "Yakovlev",
        "email": "egor@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }
    user_data_2 = {
        "user_id": uuid4(),
        "name": "Ivan",
        "surname": "Ivanov",
        "email": "ivan@example.com",
        "is_active": True,
        "hashed_password": "SampleHashPass",
        "roles": ["ROLE_PORTAL_USER"]
    }
    user_data_updated = {
        "name": "Egor",
        "surname": "Yakovlev",
        "email": user_data_2["email"],
    }
    for user_data in [user_data_1, user_data_2]:
        await create_user_in_database(**user_data)
    resp = client.patch(
        f"/user/?user_id={user_data_1['user_id']}",
        data=json.dumps(user_data_updated),
        headers=create_test_auth_headers_for_user(user_data_1["email"])
    )
    assert resp.status_code == 503
    assert (
        f'Key (email)=({user_data_2["email"]}) already exists'
        in resp.json()["detail"]
    )