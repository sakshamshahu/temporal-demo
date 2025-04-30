from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import aiofiles
from temporalio.client import Client, WorkflowFailureError
from temporalio.worker import Worker
from workflow import AadharWorkflow
import traceback

from temporal_demo.src.activities import Aadhar_Verification

app = FastAPI()

UPLOAD_DIR = os.path.abspath(os.path.join(os.getcwd(), "uploads"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/uploadpdf")
async def upload_pdf(file: UploadFile = File(...), doc_type: str = Form(...)):
    """Upload a PDF file.

    Args:
        file (UploadFile, optional): The PDF file to upload. Defaults to File(...).
        doc_type (str, optional): The type of document. Defaults to Form(...).
    """
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Please upload a PDF file."})
    

    file_location = os.path.join(UPLOAD_DIR, file.filename)
    
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    data = {
        'filename': file.filename,
        'doc_type': doc_type,
        'file_location': file_location
    }
    
    #establish connection to temporal server (local)
    temporal_client = await Client.connect("localhost:7233", namespace='default')
    
    try:
        result = await temporal_client.execute_workflow(
            AadharWorkflow.run,
            data,
            id=file.filename,
            task_queue="aadhar_queue"
        )
        print(f"Workflow result: {result}")
        
        # worker: Worker = Worker(
        #     temporal_client,
        #     task_queue="aadhar_queue",
        #     workflows=[AadharWorkflow],
        #     activities=[Aadhar_Verification().unpackPdf()],
        # )
        # await worker.run()
    
    except Exception as WorkflowFailureError:
        print("Got expected exception: ", traceback.format_exc())
    
    
    return {
        'filename': file.filename,
        'doc_type': doc_type,
        'message': 'File uploaded successfully',
        'file_location': file_location
    }
