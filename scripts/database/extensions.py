import asyncio

from core.database import Database


async def main():
    db = Database()
    await db._enable_extensions()


if __name__ == "__main__":
    asyncio.run(main())
