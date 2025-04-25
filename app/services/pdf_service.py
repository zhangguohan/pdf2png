import os
from typing import List, Optional
from pdf2image import convert_from_path
from app.core.config import settings

def convert_pdf_to_png(
    pdf_path: str,
    output_dir: str = settings.TEMP_DIR,
    file_prefix: str = "output",
    dpi: int = settings.DEFAULT_DPI,
    first_page: Optional[int] = None,
    last_page: Optional[int] = None
) -> List[str]:
    """
    将PDF文件转换为PNG图像
    
    Args:
        pdf_path: PDF文件路径
        output_dir: 输出目录
        file_prefix: 输出文件前缀
        dpi: 图像DPI
        first_page: 起始页码 (从1开始)
        last_page: 结束页码
        
    Returns:
        生成的PNG文件路径列表
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)
    
    # 转换参数
    convert_params = {
        "dpi": dpi,
        "output_folder": None,  # 不直接输出到文件
        "fmt": "png",
    }
    
    # 添加可选参数
    if first_page is not None:
        convert_params["first_page"] = first_page
    if last_page is not None:
        convert_params["last_page"] = last_page
    
    # 执行转换
    images = convert_from_path(pdf_path, **convert_params)
    
    # 保存图像
    output_files = []
    for i, image in enumerate(images):
        output_path = os.path.join(output_dir, f"{file_prefix}_page_{i+1}.png")
        image.save(output_path, "PNG")
        output_files.append(output_path)
    
    return output_files