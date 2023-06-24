from PIL import Image
from modelpredict import read_image,get_answer,model,processor,show_image
from fastapi import FastAPI, File, UploadFile
from io import BytesIO

app = FastAPI() #load fastapi


@app.post("/files/")
async def create_file(file: bytes = File(...)): #type hinting is important https://www.tutorialspoint.com/fastapi/fastapi_type_hints.htm 
    return {"file_size": len(file)}
    
@app.post("/uploadfile/")
async def main(file: bytes = File(...)): #fastAPI uses pythons type hinting
    # read image
    imagem = read_image(file)
    show_image(imagem)
    question = "What is the total or balance?"
    answer, score = get_answer(imagem, question, model, processor)
    # transform and get result 
    return answer,score