import json
import requests
import mimetypes
from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from database import save_question_answer
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")  # Render Jinja templates

# Replace these with your actual endpoint URL and Hugging Face token
ENDPOINT_URL = "https://oc0nzyfkjvdnnt14.us-east-1.aws.endpoints.huggingface.cloud"
HF_TOKEN = "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"  # Replace with your Hugging Face API token

def predict(image_bytes: bytes, file_name: str):
    """Sends image bytes to the Hugging Face Inference API and returns the JSON response."""
    # Dynamically determine the mime type from the file name
    mime_type, _ = mimetypes.guess_type(file_name)
    
    # Default to 'application/octet-stream' if the mime type can't be guessed
    if mime_type is None:
        mime_type = 'application/octet-stream'

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": mime_type  # Dynamic mime type based on file
    }
    
    response = requests.post(ENDPOINT_URL, headers=headers, data=image_bytes)
    
    try:
        response.raise_for_status()  # Raise an error for bad status codes
        # Print the model's response for debugging
        return response.json()
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return {"error": str(err)}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"error": str(err)}

@app.post("/uploadfile/", response_class=HTMLResponse)
async def main(request: Request, file: UploadFile = File(...), question: str = Form(...)):
    """
    Uploaded file is read and a question is passed as a prompt.
    The image is sent to the Hugging Face Inference API, and the response is processed.
    """
    # Read the uploaded file as bytes
    image_bytes = await file.read()
    
    # Send the image to the Hugging Face API
    response = predict(image_bytes, file.filename)  # Pass the actual filename
    
    print(response)
    # Check for errors in the response
    if "error" in response:
        answer = f"Error: {response['error']}"
    else:
        # Return the entire response without extracting specific fields
        answer = response
        
        # Save the question and full answer in the database
        save_question_answer(question, json.dumps(answer))
    
    # Render the result in the template
    return templates.TemplateResponse("result.html", {"request": request, "answer": answer})

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Route to home page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """Route to about page."""
    return templates.TemplateResponse("about.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
