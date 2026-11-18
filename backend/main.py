import os
from contextlib import asynccontextmanager
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from backend.database import Base, SessionLocal, engine, get_db
from backend.models import Inquiry, Store
from backend.schemas import InquiryCreate, InquiryOut, StoreCreate, StoreOut

ADMIN_KEY = os.getenv("ADMIN_KEY", "hasan2026")

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
ASSETS_DIR = FRONTEND_DIR / "assets"

INITIAL_STORES = [
    {"name": "مشويات الأكيل", "cat": "r", "phone": "01155235484", "open24": False},
    {"name": "أسماك الأكيل", "cat": "r", "phone": "01092154556", "open24": False},
    {"name": "كشري حكاية", "cat": "r", "phone": None, "open24": False},
    {"name": "مطعم مكة للمأكولات الشعبية", "cat": "r", "phone": None, "open24": False},
    {"name": "بيتزا اللهلوبة", "cat": "r", "phone": None, "open24": False},
    {"name": "مخبز زغوط", "cat": "r", "phone": None, "open24": False},
    {"name": "كافيه ونس - Wanas Café", "cat": "r", "phone": None, "open24": False},
    {"name": "R2 PlayStation", "cat": "f", "phone": None, "open24": False},
    {"name": "سوبر ماركت الصحي", "cat": "m", "phone": None, "open24": False},
    {"name": "جزارة الحسن", "cat": "m", "phone": None, "open24": False},
    {"name": "مجمع دواجن الجوهرة", "cat": "m", "phone": None, "open24": False},
    {"name": "ألبان ماندرين لاند", "cat": "m", "phone": None, "open24": False},
    {"name": "عطارة ألف هنا", "cat": "m", "phone": None, "open24": False},
    {"name": "العمراني للحدائد والبويات - Sipes", "cat": "s", "phone": None, "open24": False},
    {"name": "الزعيم للأدوات الصحية", "cat": "s", "phone": None, "open24": False},
    {"name": "مشارف مصر للأجهزة الكهربائية", "cat": "s", "phone": None, "open24": False},
    {"name": "فايف جي شوب - 5G Shop", "cat": "s", "phone": None, "open24": False},
    {"name": "هيلث هاوس جيم - Health House Gym", "cat": "f", "phone": None, "open24": False},
    {"name": "كوافير بندق", "cat": "f", "phone": None, "open24": False},
    {"name": "مكتبة المكتبة - M&S", "cat": "g", "phone": None, "open24": False},
    {"name": "آخر العنقود للهدايا", "cat": "g", "phone": None, "open24": False},
    {"name": "منظفات الصعيدي", "cat": "g", "phone": None, "open24": False},
    {"name": "العيادات التخصصية والصيدليات", "cat": "h", "phone": None, "open24": True},
]


def seed_initial_stores(db: Session):
    """Seed the database with Al Hasan Mall's 23 verified stores if empty."""
    existing_count = db.query(Store).count()
    if existing_count == 0:
        for store_data in INITIAL_STORES:
            store = Store(**store_data)
            db.add(store)
        db.commit()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables and seed stores
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_initial_stores(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="Al Hasan Mall Digital Hub API",
    description="Backend API for Al Hasan Mall (مبنى الحسن السياحي) in October Gardens, Giza.",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_admin_key(x_admin_key: Optional[str] = Header(None, alias="X-Admin-Key")):
    """Dependency to protect administrative routes with X-Admin-Key."""
    if not x_admin_key or x_admin_key != ADMIN_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-Admin-Key header.",
        )
    return x_admin_key


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/api/stores", response_model=List[StoreOut], tags=["Stores"])
def get_stores(db: Session = Depends(get_db)):
    """Retrieve all stores in Al Hasan Mall."""
    return db.query(Store).order_by(Store.id.asc()).all()


@app.post(
    "/api/stores",
    response_model=StoreOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Stores"],
    dependencies=[Depends(verify_admin_key)],
)
def create_store(store_in: StoreCreate, db: Session = Depends(get_db)):
    """Create a new store (Protected by X-Admin-Key)."""
    store = Store(**store_in.model_dump())
    db.add(store)
    db.commit()
    db.refresh(store)
    return store


@app.delete(
    "/api/stores/{store_id}",
    status_code=status.HTTP_200_OK,
    tags=["Stores"],
    dependencies=[Depends(verify_admin_key)],
)
def delete_store(store_id: int, db: Session = Depends(get_db)):
    """Delete a store by ID (Protected by X-Admin-Key)."""
    store = db.query(Store).filter(Store.id == store_id).first()
    if not store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Store with ID {store_id} not found.",
        )
    db.delete(store)
    db.commit()
    return {"status": "success", "message": f"Store {store_id} deleted successfully."}


@app.post(
    "/api/inquiries",
    response_model=InquiryOut,
    status_code=status.HTTP_201_CREATED,
    tags=["Inquiries"],
)
def create_inquiry(inquiry_in: InquiryCreate, db: Session = Depends(get_db)):
    """Submit a leasing or partnership inquiry for Al Hasan Mall."""
    inquiry = Inquiry(**inquiry_in.model_dump())
    db.add(inquiry)
    db.commit()
    db.refresh(inquiry)
    return inquiry


@app.get(
    "/api/inquiries",
    response_model=List[InquiryOut],
    tags=["Inquiries"],
    dependencies=[Depends(verify_admin_key)],
)
def list_inquiries(db: Session = Depends(get_db)):
    """List all leasing inquiries ordered newest first (Protected by X-Admin-Key)."""
    return db.query(Inquiry).order_by(Inquiry.created_at.desc()).all()


# ============================================================================
# STATIC FRONTEND SERVING
# ============================================================================

if ASSETS_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(ASSETS_DIR)), name="assets")


@app.get("/", include_in_schema=False)
def serve_index():
    """Serve the single-page application frontend."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(str(index_file))
    return {
        "status": "online",
        "service": "Al Hasan Mall Digital Hub API",
        "documentation": "/docs",
    }

