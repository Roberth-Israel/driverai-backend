import os
import time
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

router = APIRouter()

APK_DIR = Path(__file__).parent.parent.parent / "apk"
APK_DIR.mkdir(exist_ok=True)

class UpdateCheck(BaseModel):
    current_version: str
    current_build: int


class UpdateResponse(BaseModel):
    has_update: bool
    version: str
    build: int
    download_url: str
    changelog: str
    force: bool = False


@router.post("/update/check", response_model=UpdateResponse, tags=["Update"])
async def check_update(req: UpdateCheck):
    apk_files = list(APK_DIR.glob("*.apk"))
    if not apk_files:
        raise HTTPException(status_code=404, detail="Nenhum APK disponivel no servidor")

    latest_build = 0
    for f in apk_files:
        try:
            build = int(f.stem.split("_")[-1])
            if build > latest_build:
                latest_build = build
        except (ValueError, IndexError):
            continue

    if latest_build == 0:
        latest_build = int(time.time())

    latest_version = f"2.0.{apk_files[0].stat().st_mtime.__round__() % 100}"

    has_update = latest_build > req.current_build

    return UpdateResponse(
        has_update=has_update,
        version=latest_version if has_update else req.current_version,
        build=latest_build if has_update else req.current_build,
        download_url=f"/api/v1/update/download?v={latest_build}",
        changelog="Novas funcionalidades e correcoes" if has_update else "",
        force=False,
    )


@router.get("/update/download", tags=["Update"])
async def download_apk(v: int = 0):
    apk_files = sorted(APK_DIR.glob("*.apk"), key=lambda f: f.stat().st_mtime, reverse=True)
    if not apk_files:
        raise HTTPException(status_code=404, detail="APK nao encontrado")

    apk_path = apk_files[0]
    return FileResponse(
        path=apk_path,
        filename="DriverAI_Pro.apk",
        media_type="application/vnd.android.package-archive",
        headers={
            "Content-Disposition": f'attachment; filename="DriverAI_Pro.apk"',
        },
    )
