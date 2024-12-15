from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from pathlib import Path
import openai
from backend.database import get_db_connection, initialize_database  # Use absolute import

# Explicitly load the .env file
load_dotenv(dotenv_path=Path(__file__).parent / '.env')

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise RuntimeError("OPENAI_API_KEY is not set in the environment variables.")

# Initialize FastAPI app
app = FastAPI()

# Call this at the start of the app
initialize_database()

# Models
class Product(BaseModel):
    name: str
    category: str

class AnalyzeRequest(BaseModel):
    product_name: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Environmental Impact Analyzer!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/products")
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, category FROM products")
    products = [{"id": row["id"], "name": row["name"], "category": row["category"]} for row in cursor.fetchall()]
    conn.close()
    return {"products": products}

@app.post("/add-product")
def add_product(product: Product):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, category) VALUES (?, ?)",
        (product.name, product.category),
    )
    conn.commit()
    conn.close()
    return JSONResponse(
        content={"message": "Product added successfully!", "product": product.dict()},
        status_code=201,
    )

@app.post("/analyze")
async def analyze_product(request: AnalyzeRequest):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant providing environmental impact analysis."},
                {"role": "user", "content": f"Analyze the environmental impact of the product: {request.product_name}"}
            ],
        )
        return {"analysis": response.choices[0].message.content.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error communicating with OpenAI API: {e}")
