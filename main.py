from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime
from uuid import uuid4 as uuid
app=FastAPI()

products=[]

# Product Model
class Product(BaseModel):
    id: Optional[str]
    title: str
    description: Text
    category: str
    price: float
    stock: int
    weight: float
    location: str
    content: Text

@app.get("/")
def read_root():
    return {"Welcome": "Welcome to my API"}

@app.get("/inventory")
def get_products():
    return products

@app.get("/inventory/{product_id}")
def get_product(product_id: str):
    for product in products:
        if product["id"] == product_id:
            return product
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/inventory")
def save_product(product: Product):
    product.id = str(uuid())
    products.append(product.dict())
    return products[-1]

@app.delete("/inventory/{product_id}")
def delete_product(product_id:str):
    for index, product in enumerate(products):
        if product["id"] == product_id:
            products.pop(index)
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.put("/inventory/{product_id}")
def update_product(product_id: str, product: Product):
    for index, p in enumerate(products):
        if p["id"] == product_id:
            products[index]["title"] = product.title
            products[index]["price"] = product.price
            products[index]["content"] = product.quantity
            return {"message": "Product updated successfully"}
    raise HTTPException(status_code=404, detail="Product not found")