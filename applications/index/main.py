from fastapi import APIRouter

router = APIRouter()

@router.get('/start')
async def start(name:str='Reviy'):
    return f'Hello, {name}'


    