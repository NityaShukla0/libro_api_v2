from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api import users, books, loans
from app.config.settings import settings

app = FastAPI(
    title="Libro API v2",
    description="Library Management API with caching, rate limiting & feature flags",
    version="2.0",
    debug=settings.DEBUG
)

# -------------------------------
# Rate Limiter Setup
# -------------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# -------------------------------
# CORS Middleware
# -------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Include Routers
# -------------------------------
app.include_router(users.router)   # prefix already set in router
app.include_router(books.router)   # prefix already set in router
app.include_router(loans.router)   # prefix already set in router

# -------------------------------
# Startup Event
# -------------------------------
@app.on_event("startup")
async def startup():
    if settings.ENABLE_CACHE:
        FastAPICache.init(InMemoryBackend(), prefix="fastapi-cache")

# -------------------------------
# Root Endpoint
# -------------------------------
@app.get("/")
async def root():
    return {"message": "Welcome to Libro API v2"}