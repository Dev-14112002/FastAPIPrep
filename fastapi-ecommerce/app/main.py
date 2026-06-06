from fastapi import FastAPI, HTTPException, Query
from service.products import get_all_products

app = FastAPI()  # Used to create multiple routes


@app.get("/")  # Static route
def root():
    return {"message": "Welcome to FastAPI"}


# @app.get('/products')
# def get_products():
#     return get_all_products()


@app.get(
    "/products"
)  # Dynamic route with query parameter for searching products by name
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)",
    ),
    sort_by_price: bool = Query(
        default=False, description="Sort products by price"
    ),  # Query parameter to sort products by price
    order: str = Query(
        # Query parameter to specify sort order (ascending or descending) when sorting by price
        default="asc",
        description="Sort order when sort_by_price=true (asc or desc)",
    ),
    limit: int = Query(
        default=5,
        ge=1,
        le=100,
        description="Limit the number of products returned",
    ),
):

    products = get_all_products()  # Get all products from the service layer
    if name:
        needle = name.strip().lower()  # Case-insensitive search for products by name
        products = [p for p in products if needle in p.get("name", "").lower()]

    if not products:  # Exception handling for no products found
        raise HTTPException(
            status_code=404, detail=f"No product found matching name={name}"
        )

    if sort_by_price:
        reverse = order == "desc"
        products = sorted(products, key=lambda p: p.get("price", 0), reverse=reverse)

    total = len(products)  # Total number of products found after filtering
    products = products[
        :limit
    ]  # Limit the number of products returned based on the query parameter
    return {"total": total, "items": products}
