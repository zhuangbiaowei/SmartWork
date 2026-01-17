from fastapi import APIRouter, HTTPException, Query, Body
from pydantic import BaseModel
from pathlib import Path
import os
from typing import List, Optional

router = APIRouter()


class FileItem(BaseModel):
    name: str
    is_dir: bool
    size: int
    path: str


@router.get("/list/", response_model=List[FileItem])
async def list_files(path: str = Query(".", description="文件路径")):
    try:
        normalized_path = Path(path).expanduser().absolute()

        if not normalized_path.exists():
            raise HTTPException(status_code=404, detail="路径不存在")

        if not normalized_path.is_dir():
            raise HTTPException(status_code=400, detail="路径不是目录")

        files = []
        for item in normalized_path.iterdir():
            try:
                files.append(
                    {
                        "name": item.name,
                        "is_dir": item.is_dir(),
                        "size": item.stat().st_size if item.is_file() else 0,
                        "path": str(item),
                    }
                )
            except (PermissionError, OSError):
                continue

        return sorted(files, key=lambda x: (not x["is_dir"], x["name"]))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/read/")
async def read_file(path: str = Query(..., description="文件路径")):
    try:
        file_path = Path(path).resolve()

        if not file_path.exists() or file_path.is_dir():
            raise HTTPException(status_code=404, detail="文件不存在")

        if not file_path.is_file():
            raise HTTPException(status_code=400, detail="路径不是文件")

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        return {"path": str(file_path), "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/write/")
async def write_file(
    path: str = Query(..., description="文件路径"), content: str = Body(..., embed=True)
):
    try:
        file_path = Path(path).resolve()

        os.makedirs(file_path.parent, exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        return {"message": "文件写入成功", "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete/")
async def delete_file(path: str = Query(..., description="文件路径")):
    try:
        file_path = Path(path).resolve()

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="路径不存在")

        if file_path.is_dir():
            import shutil

            shutil.rmtree(file_path)
        else:
            file_path.unlink()

        return {"message": "删除成功", "path": str(file_path)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
