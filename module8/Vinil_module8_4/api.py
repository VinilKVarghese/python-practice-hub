from fastapi import FastAPI
from database import add_user, get_all_users, search_users

# Create FastAPI application
app = FastAPI(title="User Database API")


@app.get("/")
def home():
    """Test whether the API is running."""

    return {
        "message": "User Database API is running"
    }


@app.post("/users")
def create_user(name: str, age: int, city: str):
    """Add a user to the database."""

    return add_user(name, age, city)


@app.get("/users")
def users():
    """Get all users."""

    return get_all_users()


@app.get("/users/search")
def find_users(name: str):
    """Search users by name."""

    return search_users(name)