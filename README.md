# Shukuji

## Prototype in python for a basic microservice

- Created using Flask
- Currently uses SQLite as the database


### App Dev Steps (After creation of respective tests, for TDD manner)
1. Handler for index: (Create test and corresponding logic function)
2. Database functions (steps)
  2.1. Create the DB
    2.1.1. Connect to the DB (create connection)
    2.1.2. Initialize the DB (create desired tables)
    2.1.3. Save the DB connection for re-use by the application
  2.3. Close the DB (connection) - when app needs to close.
3. Create handlers for desired operations.
