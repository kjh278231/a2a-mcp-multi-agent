# image_mcp/server.py
from fastmcp import FastMCP
from . import tools

mcp = FastMCP("image-processor")


@mcp.tool()
def get_image_info(image_path: str) -> dict:
    """Get information about an image file.

    Args:
        image_path: Path to the image file

    Returns:
        Dictionary with image information (width, height, format, mode, size)
    """
    return tools.get_image_info(image_path)


@mcp.tool()
def resize_image(
    image_path: str, width: int, height: int, output_path: str | None = None
) -> dict:
    """Resize an image to specified dimensions.

    Args:
        image_path: Path to the input image
        width: Target width in pixels
        height: Target height in pixels
        output_path: Path to save resized image (optional)
    """
    return tools.resize_image(image_path, width, height, output_path)


@mcp.tool()
def apply_filter(
    image_path: str, filter_type: str, output_path: str | None = None
) -> dict:
    """Apply a filter to an image.

    Args:
        image_path: Path to the input image
        filter_type: Type of filter (blur, sharpen, grayscale)
        output_path: Path to save filtered image (optional)
    """
    return tools.apply_filter(image_path, filter_type, output_path)
