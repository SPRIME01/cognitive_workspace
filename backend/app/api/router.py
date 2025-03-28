"""
Main API router for the Cognitive Workspace backend.
"""

from fastapi import APIRouter

from app.api.endpoints import users, auth, workspaces, documents

api_router = APIRouter()

# Include all API endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(workspaces.router, prefix="/workspaces", tags=["workspaces"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
