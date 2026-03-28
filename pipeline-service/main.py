from math import ceil

from fastapi import FastAPI, HTTPException

from database import Session, Base, engine
from models.customer import Customer
from services.ingestion import load_customers

Base.metadata.create_all(engine)

app = FastAPI()

@app.get("/api/health")
def read_root():
    return {
		"status": "Server running"
	}

# Ingest customers from mock-server
@app.post("/api/ingest")
async def ingest_customers():
    row_counts = load_customers()
    return {
        "status": "success",
        "records_processed": row_counts
    }

# Paginated customers
@app.get("/api/customers")
def fetch_paginated_customers(page: int = 1, limit: int = 5):
    if page < 1 or limit < 1:
        raise HTTPException(400, "Page and Limit must be positive integers")
    
    with Session() as db:
        total = db.query(Customer).count()
        total_pages = max(1, ceil(total / limit))
        
        # if page > total_pages:
        #     page = total_pages
        
        offset = (page-1) * limit
        customers = (db.query(Customer)
            .order_by(Customer.customer_id)
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
            "data": customers
        }

# Customer by id
@app.get("/api/customers/{customer_id}")
def fetch_customer_by_id(customer_id: str):
    with Session() as db:
        customer = db.query(Customer).filter(Customer.customer_id == customer_id).first()
        if customer is not None:
            return customer
        else:
            raise HTTPException(404, "Customer not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)