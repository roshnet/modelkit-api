# ModelKit Server

ModelKit is a public registry to search for and exeucte machine learning models in the cloud.

This is a [FastAPI](https://fastapi.tiangolo.com/) server for ModelKit. It uses PyJWT, SQLAlchemy & Pydantic for the most part.

### Things TBD

  - DRY approach to add JWT validation middleware to specific routes (currently using WET).
  - Safely extract user-provided binaries without running code on the server.

> This README is incomplete & isn't a priority right now. Maybe I'll add it once the project is stable and deployed.
