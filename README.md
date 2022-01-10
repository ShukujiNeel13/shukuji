# Shukuji

## Prototype in python for a basic microservice

- Created using Flask
- Currently uses SQLite as the database


### App Dev Steps (After creation of respective tests, for TDD manner)
1. Create Route for Index
2. Database functions (steps)
  2.1. Create the DB
    2.1.1. Get the DB connection
      2.1.1.1. Connect to DB
    2.1.2. Save the DB connection for re-use by the application
  2.2. Close the DB (connection) - when app needs to close.
3. Create routes to perform desired operations.
4. Update the index route to more specific version (if desired)
