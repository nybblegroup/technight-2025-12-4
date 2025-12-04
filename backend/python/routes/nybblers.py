"""
Nybblers API endpoints (People Force mock)
"""
from fastapi import APIRouter
from typing import List
from schemas import NybblerDto
from services.mock_apis import people_force_service

router = APIRouter(prefix="/api/nybblers", tags=["Nybblers"])


@router.get("", response_model=List[NybblerDto])
async def get_all_nybblers():
    """Get all Nybblers from People Force (mock)"""
    return await people_force_service.get_all_nybblers()


@router.get("/search", response_model=List[NybblerDto])
async def search_nybblers(query: str):
    """Search Nybblers by name or email"""
    if not query or len(query) < 2:
        return []
    
    return await people_force_service.search_nybblers(query)


@router.get("/{user_id}", response_model=NybblerDto)
async def get_nybbler(user_id: str):
    """Get a specific Nybbler by ID"""
    nybbler = await people_force_service.get_nybbler_by_id(user_id)
    
    if not nybbler:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Nybbler not found")
    
    return nybbler





