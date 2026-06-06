from fastapi import FastAPI, HTTPException, Query
from service.products import get_all_products

app = FastAPI()  # Used to create multiple routes


@app.get("/")  # Static route
def root():
    return {"message": "Welcome to FastAPI"}


# @app.get('/products')
# def get_products():
#     return get_all_products()


@app.get("/products")
def list_products(
    name: str = Query(
        default=None,
        min_length=1,
        max_length=50,
        description="Search by product name (case insensitive)",
    )
):

    products = get_all_products()
    if name:
        needle = name.strip().lower()  # Case-insensitive search for products by name
        products = [p for p in products if needle in p.get("name", "").lower()]

        if not products:  # Exception handling for no products found
            raise HTTPException(
                status_code=404, detail=f"No product found matching name={name}"
            )
    total = len(products)  # Total number of products found after filtering
    return {"total": total, "items": products}
