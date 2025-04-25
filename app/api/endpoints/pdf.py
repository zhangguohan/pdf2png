from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import FileResponse
import os
import uuid
from typing import List
from app.services.pdf_service import convert_pdf_to_png

router = APIRouter()

@router.post("/convert", summary="将PDF转换为PNG")
async def convert_pdf(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    dpi: int = 200,
    first_page: int = None,
    last_page: int = None
):
    """
    上传PDF文件并将其转换为PNG图像
    
    - **file**: PDF文件
    - **dpi**: 图像DPI (默认: 200)
    - **first_page**: 起始页码 (默认: 1)
    - **last_page**: 结束页码 (默认: 最后一页)
    """
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="只接受PDF文件")
    
    # 创建临时文件名
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    temp_id = str(uuid.uuid4())
    temp_pdf_path = os.path.join(temp_dir, f"{temp_id}.pdf")
    
    # 保存上传的文件
    with open(temp_pdf_path, "wb") as pdf_file:
        content = await file.read()
        pdf_file.write(content)
    
    try:
        # 转换PDF为PNG
        output_files = convert_pdf_to_png(
            pdf_path=temp_pdf_path,
            output_dir=temp_dir,
            file_prefix=temp_id,
            dpi=dpi,
            first_page=first_page,
            last_page=last_page
        )
        
        # 创建ZIP文件以便下载多个图像
        if len(output_files) > 1:
            import zipfile
            zip_path = os.path.join(temp_dir, f"{temp_id}.zip")
            with zipfile.ZipFile(zip_path, 'w') as zipf:
                for png_file in output_files:
                    zipf.write(png_file, os.path.basename(png_file))
            
            # 设置清理任务
            background_tasks.add_task(cleanup_files, [temp_pdf_path] + output_files + [zip_path])
            
            return FileResponse(
                zip_path,
                media_type="application/zip",
                filename=f"{os.path.splitext(file.filename)[0]}.zip"
            )
        else:
            # 只有一个文件时直接返回PNG
            background_tasks.add_task(cleanup_files, [temp_pdf_path] + output_files)
            
            return FileResponse(
                output_files[0],
                media_type="image/png",
                filename=f"{os.path.splitext(file.filename)[0]}.png"
            )
    
    except Exception as e:
        # 清理临时文件
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)
        raise HTTPException(status_code=500, detail=f"转换失败: {str(e)}")

def cleanup_files(files: List[str]):
    """清理临时文件"""
    for file_path in files:
        if os.path.exists(file_path):
            os.unlink(file_path)