from fastapi import FastAPI, Request, HTTPException, APIRouter, Form #type: ignore
from fastapi.middleware.cors import CORSMiddleware #type: ignore
from fastapi.responses import Response, StreamingResponse #type: ignore
from fastapi.staticfiles import StaticFiles #type: ignore
from fastapi.templating import Jinja2Templates #type: ignore
from starlette.responses import HTMLResponse, RedirectResponse #type: ignore
from uvicorn import  run as app_run #type: ignore
from fastapi import File, UploadFile #type: ignore
from io import BytesIO
from typing import List

from b2_service import B2
client = B2()

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


@app.get('/', tags=['authentication'])
async def index(request: Request):
    """Renders main html page"""
    return templates.TemplateResponse('index.html', {'request': request, 'context': "Rendering"})



@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        client.upload_file(file_name=file.filename, object_file=contents)
        print(f'File: {file.filename} uploaded Successfully')
    except Exception as e:
        print(e)


@app.post("/download")
async def download_file(file_name: str = Form(...)):
    try:
        memory_stream = BytesIO()

        # Important: Your client must support writing to a stream
        client.s3_client.download_fileobj(file_name, memory_stream)  # NOT download_file()

        memory_stream.seek(0)  # Reset pointer to start
        
        return StreamingResponse(
            memory_stream,
            media_type="application/octet-stream",
            headers={"Content-Disposition": f"attachment; filename={file_name}"}
        )


    except Exception as e:
        raise HTTPException(status_code=404, detail=f"File not found: {str(e)}")
    
    
@app.get("/viewfiles", response_model=List[str])
async def view_files_s():
    response = client.view_files()
    return response
    
@app.post('/delete')
async def deleteFile(file_name: str = Form(...)):
    client.delete_file(key=file_name)
    
    
if __name__ == "__main__":
    app_run(app, host='0.0.0.0', port='8080')