## Data Models

This folder contains data models, with each file representing a table in our SQL database.

### Optimizations

1. **Main and Details Tables**:
   - Some models are split into main and details tables to improve read performance (person, person_details).
   - Example: In the frontend, we display a table of all people with a few fields for each row, allowing for filtering, sorting, and searching. Clicking on a person retrieves the full person object.
   - By separating tables based on access patterns, we enhance read performance.

2. **Denormalization**:
   - To boost performance, we denormalize main tables. These are queried often with combinations of sorting, filtering, searching etc so we want to maximize reads.

