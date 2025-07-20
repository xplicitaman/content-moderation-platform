# content-moderation-platform
Content Moderation pipeline backend

# Tech Used:
- Docker -> To host PostgreSQL instance
- PostgreSQL -> SQL database to store incoming data
- RabbitMQ -> Message broker to handle async tasks, creates a queue of task for the AI model to handle
- DBeaver -> To view and edit the PostgreSQL db

# Liraries Used:
- FastAPI[all] -> Fast, high-performing web framework to make APIs with uvicorn (runs ASGI servers) and pydantic (for data validation)
- SQLAlchemy[asyncio] -> Most popular **O**bject-**R**elational **M**apper (ORM), allows interaction with db tables using Python classes instead of raw SQL queries
- asyncpg -> High-performance db driver that allows Python's asyncio to communicate with PostgreSQL asynchronously
- pika -> Most widely used Python client for RabbitMQ, allows to publish messages (from the API) and consume them (in our worker)

# Files in the project:
- main.py -> Main server and utility functions
- database.py -> Database connections and sessions
- models.py -> Database models which is basically the ORM models that define the schema of the db tables
- worker.py -> Worker that listens and consumes messages from RabbitMQ