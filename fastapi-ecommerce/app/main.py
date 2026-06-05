from fastapi import FastAPI
from service.products import get_all_products

app = FastAPI() #Used to create multiple routes

@app.get('/')#Static route 
def root():
    return {"message": "Welcome to FastAPI"}

@app.get('/products')
def get_products():
    return get_all_products()
