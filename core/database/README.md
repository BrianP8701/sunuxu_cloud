## Database

This folder contains the `Database()` and `BlobStorage()` classes. Direct interactions with the database are handled exclusively through these classes.

### Details

- **Storage Types**: Our application uses both SQL and blob/object storage.
- **Abstract Classes**: We define abstract classes for SQL and blob storage.
- **Concrete Implementations**: We use Azure PostgreSQL for SQL storage and Azure Blob Storage for object storage.
- **Singleton Pattern**: Both classes are singletons, retrieving connection strings/keys from `.env` upon instantiation.
- **ORM**: We use SQLAlchemy to manage the connection pool.
