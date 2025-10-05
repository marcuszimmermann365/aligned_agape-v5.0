
from fastapi import APIRouter, Response
import pathlib

router = APIRouter()
CAT_PATHS = [
    pathlib.Path(__file__).resolve().parents[1] / "world_data" / "catalog.yaml",
]

@router.get("/world/catalog", response_class=Response, responses={200: {"content": {"text/plain": {}}}})
async def world_catalog():
    for p in CAT_PATHS:
        if p.exists():
            return Response(p.read_text(encoding="utf-8"), media_type="text/plain")
    return Response("catalog: not found", status_code=404, media_type="text/plain")
