# PDF to PNG Converter

一个基于FastAPI的服务，用于将PDF文件转换为PNG图像。

## 安装
### 环境：python-3.12

```bash
pip install -r requirements.txt
```

## 启动

```bash

uvicorn app.main:app --host 0.0.0.0 --port 8090 --reload 
```

## Curl测试例子

```bash
(pdf2png) gzgi@dify-test:~/tank$ curl -X POST "http://127.0.0.1:8090/api/convert"   -H "accept: application/json"   -H "x-api-key: ADFeerer2343vdfFIOUKwefoijlsakfj98798"   -H "Content-Type: multipart/form-data"   -F "file=@./dzfp_25442000000216382284_广有限公司_20250418102010.pdf"   -F "dpi=200"   --output 12333.png

  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  269k  100  212k  100 58307   227k  62551 --:--:-- --:--:-- --:--:--  288k
```

