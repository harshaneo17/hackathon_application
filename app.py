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
ENDPOINT_URL = "https://z30t4qhxpgvjofag.eu-west-1.aws.endpoints.huggingface.cloud"  # Hugging Face model endpoint
HF_TOKEN = "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"  # Replace with your Hugging Face API token

def predict(image_bytes: bytes, question: str, file_name: str):
    """Sends image bytes and question to the Hugging Face Inference API and returns the JSON response."""
    # Dynamically determine the MIME type from the file name
    mime_type, _ = mimetypes.guess_type(file_name)
    
    # Default to 'application/octet-stream' if the mime type can't be guessed
    if mime_type is None:
        mime_type = 'application/octet-stream'

    # Prepare the headers and payload for the Hugging Face inference API
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": mime_type  # Dynamic mime type based on file
    }

    data = {"image" : image_bytes, "question" : question}

    # Send the POST request to the Hugging Face inference endpoint
    response = requests.post(ENDPOINT_URL, headers=headers, data=data)
    
    try:
        response.raise_for_status()  # Raise an error for bad status codes
        # Print the model's response for debugging
        return response.json()  # Return the response as JSON
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        return {"error": str(err)}
    except Exception as err:
        print(f"Other error occurred: {err}")
        return {"error": str(err)}

@app.post("/uploadfile/", response_class=HTMLResponse)
async def main(request: Request, file: UploadFile = File(...), question: str = Form(...)):
    """
    Handles file uploads, processes the question, and sends the image and question to the Hugging Face API.
    """
    # Read the uploaded file as bytes
    image_bytes = await file.read()

    # Send the image and question to the Hugging Face API
    response = predict(image_bytes, question, file.filename)  # Pass image bytes, question, and filename
    
    
    # Check for errors in the response
    if "error" in response:
        answer = f"Error: {response['error']}"
    else:
        # Handle the prediction response and extract the answer
        answer = response  # Keep the full response for now
        
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
