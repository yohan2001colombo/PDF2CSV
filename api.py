import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from backend.constants import DATA_PATH
from fastapi.responses import FileResponse
from pdf_to_markdown import pdf2markdown
from backend.tableextracter import extract_and_convert_csv
from backend.reformat_item import reformat_items
from backend.reformat_buildings import reformat_buildings

app = FastAPI()
#  uv run uvicorn api:app --reload

@app.post("/upload/")
async def upload(file: UploadFile = File(...)):
    
    path = f"{DATA_PATH}/{file.filename}"
    
    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    base_name = file.filename.replace(".pdf", "")
    csv_path_item = f"{DATA_PATH}/{base_name}_items.csv"   
    csv_path_building = f"{DATA_PATH}/{base_name}_buildings.csv" 
    
    if not os.path.exists(csv_path_item) or not os.path.exists(csv_path_building):
        pdf2markdown()  # Process the PDF to Markdown and extract tables
        extract_and_convert_csv()  # Extract and convert tables to CSV

    return {
        "filename": file.filename,
        "path": path,
        "csv": path.replace(".pdf", ".csv")
    }

@app.get("/download/items/{filename}")
async def download_items(filename: str):

    base_name = filename.replace(".pdf", "")
    csv_path = f"{DATA_PATH}/{base_name}_items.csv"
    
    reformat_items(csv_path)  # Reformat the items CSV before sending
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Items CSV not found")

    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename=f"{base_name}_items.csv"
    )
    
@app.get("/download/buildings/{filename}")
async def download_buildings(filename: str):

    base_name = filename.replace(".pdf", "")
    csv_path = f"{DATA_PATH}/{base_name}_buildings.csv"
    
    reformat_buildings(csv_path)  # Reformat the buildings CSV before sending
    
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="Buildings CSV not found")

    return FileResponse(
        path=csv_path,
        media_type="text/csv",
        filename=f"{base_name}_buildings.csv"
    )
# uv run streamlit run fronted/app.py     
