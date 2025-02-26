import os
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Use DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dbname")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    buying_price = Column(Float)
    selling_price = Column(Float)

class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str
    type: str
    buying_price: float
    selling_price: float

class ServiceCreate(BaseModel):
    name: str
    description: str
    price: float

@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/services/")
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    db_service = Service(**service.dict())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

@app.get("/services/")
def read_services(db: Session = Depends(get_db)):
    return db.query(Service).all()
