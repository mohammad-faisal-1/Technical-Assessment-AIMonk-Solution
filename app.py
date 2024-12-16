from fastapi import FastAPI, File, UploadFile, HTTPException
import httpx

app = FastAPI()

AI_BACKEND_URL = "http://127.0.0.1:5001/detect"

@app.post("/upload")
async def upload_image(image: UploadFile = File(...)):
    if not image:
        raise HTTPException(status_code=400, detail="No image uploaded")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(AI_BACKEND_URL, files={"image": (image.filename, image.file, image.content_type)})
            return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to AI backend: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)