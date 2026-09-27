from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()


# Create an endpoint called /hello
@app.get("/hello")
def hello(name: str):
    # Return the message as a dictionary
    return {"message": f"Hello {name}"}