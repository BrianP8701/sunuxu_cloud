import asyncio

from core.objects import User

from scripts.create_fake_data.fake_user import fake_user_data


async def test_create_fake_user():
    user = await User.create(fake_user_data())
    print(user.to_dict())


if __name__ == "__main__":
    asyncio.run(test_create_fake_user())


# import asyncio

# from core.objects import User

# from scripts.create_fake_data.fake_user import fake_user_data


# async def test_create_fake_user():
#     user_data = [fake_user_data() for _ in range(10)]
#     users = await User.batch_create(user_data)
#     print(users)


# if __name__ == "__main__":
#     asyncio.run(test_create_fake_user())

