from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import os
import psycopg2
import requests
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()
Instrumentator().instrument(app).expose(app)

DB_URL = os.getenv("DATABASE_URL")
PRODUCT_SERVICE_URL = os.getenv("PRODUCT_SERVICE_URL", "http://product_service:8000")

def validate_config() -> None:
    missing = []
    if not DB_URL:
        missing.append("DATABASE_URL")
    if not PRODUCT_SERVICE_URL:
        missing.append("PRODUCT_SERVICE_URL")
    if missing:
        raise RuntimeError(f"Missing required environment variables: {', '.join(missing)}")

@app.on_event("startup")
def startup_event():
    validate_config()
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id SERIAL PRIMARY KEY,
                product_id INT,
                status VARCHAR(50)
            )
        """)
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        raise RuntimeError(f"Database initialization failed: {e}")

@app.get("/health")
def health_check():
    try:
        conn = psycopg2.connect(DB_URL)
        conn.close()
        return {"status": "ok"}
    except Exception as exc:
        return JSONResponse(status_code=503, content={"status": "degraded", "error": str(exc)})

@app.post("/orders/{product_id}")
def create_order(product_id: int):
    try:
        resp = requests.get(f"{PRODUCT_SERVICE_URL}/products/{product_id}")
        if resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Product not found")
        
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO orders (product_id, status) VALUES (%s, %s) RETURNING id", 
            (product_id, "created")
        )
        order_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return {"order_id": order_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/orders")
def get_orders():
    try:
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("SELECT id, product_id, status FROM orders")
        orders = [{"id": row[0], "product_id": row[1], "status": row[2]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        return orders
    except Exception:
        raise HTTPException(status_code=500, detail="Database Error")