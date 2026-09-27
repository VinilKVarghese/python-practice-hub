from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI()


# Example list of items
items = [
    "Item 1",
    "Item 2",
    "Item 3",
    "Item 4",
    "Item 5",
    "Item 6",
    "Item 7",
    "Item 8",
    "Item 9",
    "Item 10",
    "Item 11",
    "Item 12",
    "Item 13",
    "Item 14",
    "Item 15",
    "Item 16",
    "Item 17",
    "Item 18",
    "Item 19",
    "Item 20",
]


# Create the /items endpoint
@app.get("/items")
def get_items(page: int = 1, size: int = 5):

    # Calculate the starting position
    start = (page - 1) * size

    # Calculate the ending position
    end = start + size

    # Get only the items for the requested page
    page_items = items[start:end]

    # Calculate total number of items
    total_items = len(items)

    # Calculate total number of pages
    total_pages = (total_items + size - 1) // size

    # Return the items and page metadata
    return {
        "items": page_items,
        "metadata": {
            "page": page,
            "size": size,
            "total_items": total_items,
            "total_pages": total_pages,
            "has_next": page < total_pages,
            "has_previous": page > 1
        }
    }
