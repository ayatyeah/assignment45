from fastapi import FastAPI, HTTPException
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}

PRODUCTS = {
    1: {"name": "Laptop", "price": 1000},
    2: {"name": "Phone", "price": 500}
}

@app.get("/products")
def get_products():
    return PRODUCTS

@app.get("/products/{product_id}")
def get_product(product_id: int):
    if product_id in PRODUCTS:
        return PRODUCTS[product_id]
    raise HTTPException(status_code=404, detail="Product not found")