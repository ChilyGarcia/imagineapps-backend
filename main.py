from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.core import exception_handlers
from app.db.base import Base

from app.routers.auth import router as auth_router
from app.routers.user import router as user_router
from app.routers.events import router as events_router
from app.routers.category import router as category_router

app = FastAPI(
    title="FastAPI App",
    description="API con autenticación OAuth2",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    swagger_ui_oauth2_redirect_url="/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "usePkceWithAuthorizationCodeGrant": True,
        "clientId": "",
        "clientSecret": "",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(HTTPException, exception_handlers.http_exception_handler)
app.add_exception_handler(404, exception_handlers.not_found_exception_handler)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(events_router, prefix="/events", tags=["events"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
