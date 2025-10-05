
from fastapi import APIRouter, HTTPException
import json, pathlib

router = APIRouter()
WD = pathlib.Path(__file__).resolve().parents[1] / "world_data" / "world_state.json"

@router.get("/world/state")
async def world_state():
    if not WD.exists():
        raise HTTPException(status_code=404, detail="world_state.json not found")
    try:
        return {"ok": True, "state": json.loads(WD.read_text(encoding="utf-8"))}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
