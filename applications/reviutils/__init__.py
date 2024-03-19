from typing import List
from enum import Enum

import pandas as pd
from fastapi import APIRouter,Query,HTTPException
from pydantic import BaseModel

from reviutils.common import get_passrate
from reviutils.noisepollution.splhelper import calc_Leq, calc_LA,calc_Lt,calc_Ldn
from reviutils.noisepollution.funcarea import FuncAreaSimple, get_func_area_info

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
    
@router.get('/FuncAreaInfo')
async def Get_func_area_info(area:FuncAreaSimple=Query(description='功能区类别')):
    '''获取环境噪声限值'''
    result = get_func_area_info(area.value)
    return result.model_dump()

@router.get('/passrate')
async def Get_Passrate(area:FuncAreaSimple=Query(description='功能区类别'),is_day:bool=Query(description='昼夜间'),LData:List[float]=Query(description='声级数据列表')):
    '''获取噪声达标率'''
    data = pd.Series(LData)
    funcarea_info:BaseModel = get_func_area_info(area.value)
    limit = funcarea_info.lmtd if is_day else funcarea_info.lmtn # 获取限值
    passdata = data[data<=limit]
    return {
        'Area':area,
        'LData':LData,
        'Limit': limit,
        "is_day":is_day,
        'Passrate':get_passrate(pass_num=len(passdata), total=len(data))
    }