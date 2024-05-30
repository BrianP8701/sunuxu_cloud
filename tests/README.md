We test locally, then deployed.

In dev mode (env variable) we run the application with `func start` from azure CLI to simulate the azure function app locally. In dev mode we still use the cloud test database.

In test mode we run tests against the deployed test azure function app.
