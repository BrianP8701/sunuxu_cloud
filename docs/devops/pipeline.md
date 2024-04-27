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


okay update heres what its like now

develop backend core locally. test locally
develop backend routes locally. test locally
deploy backend routes to sunuxu-test-functions function app. test by calling the cloud functions locally with mocks

develop frontend locally
run frontend locally with vercel dev. run azure function app locally with func start. test frontend locally.
run frontend locally with vercel dev. test frontend locally calling deployed test azure function routes
deploy frontend to azure static web apps sunuxu-test-frontend. test with sunuxu-test-functions

deploy backend to sunuxu-functions for prod
deploy fronend to sunuxu-frontend for prod