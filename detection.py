from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import torch
from PIL import Image
import os
import json
import shutil

# Initialize FastAPI app
app = FastAPI()

# Load YOLOv3 model (assuming 'yolov5s' is the correct model name)
model = torch.hub.load('ultralytics/yolov3', 'yolov5s', pretrained=True)

# Output directory
OUTPUT_DIR = "./output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/detect")
async def detect(image: UploadFile = File(...)):
    try:
        # Load the uploaded image
        img = Image.open(image.file)
        results = model(img)

        # Define the output image path in the output folder
        output_image_path = os.path.join(OUTPUT_DIR, "output.jpg")

        # Save the result image (with bounding boxes) to the output folder
        results.save(OUTPUT_DIR)  # This saves the image with bounding boxes to the output folder
        detection_image_path = os.path.join(OUTPUT_DIR, "output.jpg")  # Set the specific image name for the detection

        # If results.save() creates a file with a different name, we copy it to output.jpg
        if not os.path.exists(detection_image_path):  # If the image doesn't exist, we copy the first image
            saved_images = os.listdir(OUTPUT_DIR)
            for img_file in saved_images:
                if img_file.endswith(".jpg"):  # Look for the saved image with .jpg extension
                    shutil.copy(os.path.join(OUTPUT_DIR, img_file), detection_image_path)

        # Extract detections
        detections = results.pandas().xyxy[0].to_dict(orient="records")

        # Save the detections as a JSON file
        output_json_path = os.path.join(OUTPUT_DIR, "detections.json")
        with open(output_json_path, 'w') as json_file:
            json.dump({"detections": detections}, json_file, indent=4)

        # Return response as JSON with image and JSON file paths
        return JSONResponse(content={
            "detections": detections,
            "image_path": detection_image_path,
            "json_path": output_json_path
        })
    
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5001)
