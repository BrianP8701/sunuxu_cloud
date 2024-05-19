import asyncio

from core.database.azure_postgresql import AzurePostgreSQLDatabase

async def main():
    db = AzurePostgreSQLDatabase()
    await db._enable_extensions()

if __name__ == "__main__":
    asyncio.run(main())

