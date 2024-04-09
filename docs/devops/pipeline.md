# Development Pipeline

## Development Phase
- For `sunuxu_cloud`: Use the development branch. Test functionality by executing `func start` locally. Utilize the Azure SQL test database.
- For `sunuxu_frontend`: Work within the development branch. Test the Next.js application by running it locally.

## Testing Phase
- Deploy `sunuxu_cloud` to the Azure test function app and execute all tests.

## Production Preparation
- Merge `sunuxu_cloud` from the development branch to the main branch.

## Integration Testing
- Conduct integration tests for `sunuxu_frontend` against `sunuxu_cloud` deployed on the Azure test function app.

## Deployment to Production
- Deploy `sunuxu_frontend` to Azure web hosting services.
