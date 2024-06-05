import pytest

from core.objects.base_entities.user import User


@pytest.mark.asyncio
async def test_insert_user():
    user = User(
        email="test@test.com",
        phone="1234567890",
        first_name="Test",
        last_name="Test",
        password="password",
    )

    await user.create()
    assert user.id is not None
