# image_mcp/tools.py
from pathlib import Path
from PIL import Image, ImageFilter
from typing import Optional


def get_image_info(image_path: str) -> dict:
    """이미지 파일 정보를 조회합니다."""
    try:
        with Image.open(image_path) as img:
            return {
                "success": True,
                "path": image_path,
                "width": img.width,
                "height": img.height,
                "format": img.format,
                "mode": img.mode,
                "size_bytes": Path(image_path).stat().st_size,
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def resize_image(
    image_path: str, width: int, height: int, output_path: Optional[str] = None
) -> dict:
    """이미지를 지정한 크기로 리사이즈합니다."""
    try:
        with Image.open(image_path) as img:
            resized = img.resize((width, height), Image.Resampling.LANCZOS)
            if output_path is None:
                path = Path(image_path)
                output_path = str(path.parent / f"{path.stem}_resized{path.suffix}")
            resized.save(output_path)
            return {
                "success": True,
                "input": image_path,
                "output": output_path,
                "original_size": f"{img.width}x{img.height}",
                "new_size": f"{width}x{height}",
            }
    except Exception as e:
        return {"success": False, "error": str(e)}


def apply_filter(
    image_path: str, filter_type: str, output_path: Optional[str] = None
) -> dict:
    """이미지에 필터를 적용합니다."""
    try:
        with Image.open(image_path) as img:
            if filter_type.lower() == "grayscale":
                filtered = img.convert("L")
            elif filter_type.lower() == "blur":
                filtered = img.filter(ImageFilter.BLUR)
            elif filter_type.lower() == "sharpen":
                filtered = img.filter(ImageFilter.SHARPEN)
            else:
                return {"success": False, "error": f"Unknown filter: {filter_type}"}
            if output_path is None:
                path = Path(image_path)
                output_path = str(
                    path.parent / f"{path.stem}_{filter_type}{path.suffix}"
                )
            filtered.save(output_path)
            return {
                "success": True,
                "input": image_path,
                "output": output_path,
                "filter": filter_type,
            }
    except Exception as e:
        return {"success": False, "error": str(e)}
