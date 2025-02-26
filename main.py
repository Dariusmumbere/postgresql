from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from fastapi.middleware.cors import CORSMiddleware

# Database URL (replace with your actual database URL)
DATABASE_URL = "postgresql://itech_l1q2_user:AoqQkrtzrQW7WEDOJdh0C6hhlY5Xe3sv@dpg-cuvnsbggph6c73ev87g0-a/itech_l1q2"

# Create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
Base = declarative_base()

# Product model
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    buying_price = Column(Float)
    selling_price = Column(Float)

# Service model
class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)

# Create tables if they do not exist
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (replace with your frontend URL in production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models for request validation
class ProductCreate(BaseModel):
    name: str
    type: str
    buying_price: float
    selling_price: float

class ServiceCreate(BaseModel):
    name: str
    description: str
    price: float

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "ok", "message": "ITECH Management System is running"}

# Create a new product
@app.post("/products/")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    try:
        db_product = Product(**product.dict())
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all products
@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    try:
        products = db.query(Product).all()
        return products
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Create a new service
@app.post("/services/")
def create_service(service: ServiceCreate, db: Session = Depends(get_db)):
    try:
        db_service = Service(**service.dict())
        db.add(db_service)
        db.commit()
        db.refresh(db_service)
        return db_service
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Get all services
@app.get("/services/")
def read_services(db: Session = Depends(get_db)):
    try:
        services = db.query(Service).all()
        return services
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
