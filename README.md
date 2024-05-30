# MoonXu Backend

This is the backend for MoonXu, the all-in-one app for real estate agents.

## Tech Stack
- **Azure Functions**: Serverless compute service.
- **Azure PostgreSQL**: Managed database service.

## Folder Structure
- **core**: Contains application logic.
- **api**: Exposes API endpoints. Minimal logic here; most logic resides in the core folder for easy replatforming.
- **playground**, **my_stuff**, **tools**: Can be ignored.
- **tests**: Contains test cases.

## Getting Started
1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Run Locally**: Use `func start` from Azure CLI to simulate the Azure Function app locally.
3. **Testing**: Tests run against the deployed test Azure Function app.

For more details, refer to the README files in each folder.