## Data Models

This folder contains data models, with each file representing a table in our SQL database.

### Optimizations

1. **Main and Details Tables**:
   - Some models are split into main and details tables to improve read performance.
   - Example: In the frontend, we display a table of all people with a few fields for each row, allowing for filtering, sorting, and searching. Clicking on a person retrieves the full person object.
   - By separating tables based on access patterns, we enhance read performance.

2. **Denormalization**:
   - To boost performance, we denormalize and avoid relationships in the main tables.
   - This tradeoff increases complexity, requiring careful updates and data consistency checks, but the performance gains are worth it.