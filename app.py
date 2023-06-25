from PIL import Image
from modelpredict import read_image, get_answer, model, processor, show_image
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from io import BytesIO

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.post("/files/")
async def create_file(file: bytes = File(...)):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def main(request: Request, file: bytes = File(...), question: str = Form(...)):
    # Read image
    imagem = read_image(file)
    show_image(imagem)
    answer, score = get_answer(imagem, question, model, processor)
    # Transform and get result
    return templates.TemplateResponse("result.html", {"request": request, "answer": answer["answer"]})


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)