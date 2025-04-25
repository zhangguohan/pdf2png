
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import pdf

app = FastAPI(
    title="PDF to PNG Converter",
    description="将PDF文件转换为PNG图像的API服务",
    version="0.1.0",
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含路由
app.include_router(pdf.router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "欢迎使用PDF到PNG转换服务"}