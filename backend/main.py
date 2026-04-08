from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from routers import wallets, transactions, sync
from routers.auth import router as auth_router
from auth import get_current_user

app = FastAPI(
    title       = "Blockchain Analytics API",
    description = "Track and analyze Polygon wallet transactions",
    version     = "1.0.0"
)

# ─── CORS ─────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins       = ["*"],  # We'll restrict this after deploy
    allow_credentials   = True,
    allow_methods       = ["*"],
    allow_headers       = ["*"],
)

# ─── Public Routes (no auth needed) ───────────────────
app.include_router(auth_router)

# ─── Protected Routes (auth required) ─────────────────
app.include_router(
    wallets.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    transactions.router,
    dependencies=[Depends(get_current_user)]
)
app.include_router(
    sync.router,
    dependencies=[Depends(get_current_user)]
)


@app.get("/", tags=["Health"])
def root():
    return {
        "app"       : "Blockchain Analytics API",
        "version"   : "1.0.0",
        "status"    : "running",
        "docs"      : "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
    