from fastapi import APIRouter,Query,HTTPException
from reviutils.common import get_passrate
from reviutils.noisepollution.splhelper import calc_Leq, calc_LA,calc_Lt,calc_Ldn
import pandas as pd
from typing import List
from .schemas import FuncArea
from .spl import NoiseLevel

router = APIRouter()

@router.get('/Leq')
async def Calc_Leq(LData:List[float]=Query(description='声级数据列表')):
    '''计算等效声级'''
    data = pd.Series(LData)
    Leq = calc_Leq(data)
    return {'Leq':Leq,"data":LData}

@router.get('/Lt')
async def Calc_Lt(LData:List[float]=Query(description='声级数据列表')):
    '''计算叠加声级'''
    data = pd.Series(LData)
    Lt = calc_Lt(data)
    return {'Lt':Lt,"data":LData}

@router.get('/LA')
async def Calc_LA(LData:List[float]=Query(description='声级数据列表')):
    '''计算监测声强时所需的各类声级数据，包括：L10、L50、L90、Leq、Lmax、Lmin、标准差(std)'''
    data = pd.Series(LData)
    result = calc_LA(data)
    return {'result':result,"data":LData}

@router.get('/Ldn')
async def Calc_Ldn(HourData:List[int]=Query(description='小时数据列表'),LData:List[float]=Query(description='声级数据列表'),):
    '''计算小时数据的Ld，Ln，Ldn'''
    try:
        result = calc_Ldn(hour_data=HourData, leq_data=LData)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get('/limit')
async def Get_Limit(area:FuncArea=Query(description='功能区类别')):
    '''获取环境噪声限值'''
    nl = NoiseLevel(area.value)
    return {
        'Area':area.value+'类',
        'Day':nl.day_level,
        'Night':nl.night_level,
    }

@router.get('/passrate')
async def Get_Passrate(area:FuncArea=Query(description='功能区类别'),is_day:bool=Query(description='昼夜间'),LData:List[float]=Query(description='声级数据列表')):
    '''获取噪声达标率'''
    data = pd.Series(LData)
    if is_day:
        limit = NoiseLevel(area.value).day_level
    else:
        limit = NoiseLevel(area.value).night_level
    passdata = data[data<=limit]
    return {
        'Area':area.value+'类',
        'LData':LData,
        'Limit': limit,
        "is_day":is_day,
        'Passrate':get_passrate(pass_num=len(passdata), total=len(data))
    }