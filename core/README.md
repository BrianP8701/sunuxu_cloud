## Core Folder Structure

- **database**: Singleton objects for database interactions, abstracting connection pooling for SQL and blob storage.
- **queries**: Helper methods for complex, reusable data queries.
- **models**: Data models representing SQL database tables.
- **types**: Pydantic models and types used throughout the application, abstracting direct database interactions.
- **integrations**: Wrapper classes for external APIs and services.
- **api**: API endpoints as Python functions, separating routes from logic for easy replatforming.
- **enums**, **constants**, **utils**: You should know what these are.

## Recommended Reading Order

To best understand the application, read the READMEs in the following order:

1. **database**
2. **models**
3. **types**

After that, the order doesn't matter.