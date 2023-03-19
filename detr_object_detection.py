import logging
import os
import random
import string
import threading
import time
from typing import Dict

import torch
from flask import Flask, jsonify, render_template, request, Response
from PIL import Image, ImageDraw
from dotenv import load_dotenv
from pycocotools.coco import COCO
from transformers import DetrForObjectDetection, DetrImageProcessor

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)

# Set port number
PORT = int(os.environ.get("PORT", 5000))

# Set path to COCO annotations file
ANNOTATION_PATH = "annotations/instances_val2017.json"

# Set name of DETR model to be used
MODEL_NAME = "facebook/detr-resnet-101"


def remove_output_file(output_path: str) -> None:
    """Removes the output image file after 30 minutes."""
    time.sleep(1800)
    if os.path.exists(output_path):
        os.remove(output_path)
        logger.info(f"Removed output file {output_path}")


def detect_objects(image: Image, processor: DetrImageProcessor, model: DetrForObjectDetection) -> Dict:
    """
    Performs object detection on an input image using the given DETR model.

    Args:
        image: The input image.
        processor: The DETR image processor.
        model: The DETR object detection model.

    Returns:
        A dictionary containing the object detection results.
    """
    logger.info("Performing object detection...")

    # Check if CUDA is available
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logger.info(f"Using device: {device}")

    # Process input image
    inputs = processor(images=image, return_tensors="pt").to(device)

    # Move model to the same device as the inputs
    model.to(device)

    # Perform object detection using DETR model
    outputs = model(**inputs)

    # Post-process object detection results
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.9)[0]

    # Load COCO annotations file
    coco = COCO(ANNOTATION_PATH)

    # Create mapping from category ID to category name
    label_mapping = {}
    for category in coco.cats.values():
        label_mapping[category["id"]] = category["name"]
    label_mapping[0] = "background"

    logger.info("Object detection completed.")

    # Draw bounding boxes and labels on input image
    draw = ImageDraw.Draw(image)
    for box, score, label in zip(results["boxes"], results["scores"], results["labels"]):
        box = tuple(map(int, box))
        draw.rectangle(box, outline="red")
        label_name = label_mapping[label.item()]
        draw.text((box[0], box[1] - 20), f"{label_name} ({score:.3f})", fill="black")

    # Save output image to file
    output_filename = "".join(random.choices(string.ascii_lowercase + string.digits, k=8)) + ".png"
    if not os.path.exists(app.static_folder):
        os.makedirs(app.static_folder)
    output_path = os.path.join(app.static_folder, output_filename)
    image.save(output_path)
    logger.info(f"Output image saved to {output_path}")

    # Start thread to remove output file after 30 minutes
    threading.Thread(target=remove_output_file, args=(output_path,)).start()

    logger.info("Returning object detection results to the user...")

    # Return object detection results as dictionary
    response_data = {
        "scores": results["scores"].tolist(),
        "labels": [label_mapping[label.item()] for label in results["labels"]],
        "boxes": results["boxes"].tolist(),
        "image_filename": output_filename,
    }
    return response_data


@app.route("/")
def home() -> str:
    """Displays the home page."""
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect() -> Response:
    """
    Handles the object detection request.

    Returns:
        A Flask response containing the object detection results.
    """
    # Get input image from request
    image_file = request.files["image"]
    image = Image.open(image_file).convert("RGB")

    # Perform object detection and return results as Flask response
    response_data = detect_objects(image, DetrImageProcessor.from_pretrained(MODEL_NAME),
                                   DetrForObjectDetection.from_pretrained(MODEL_NAME))
    return jsonify(response_data)


if __name__ == "__main__":
    # Start Flask server
    logger.info(f"Starting server on port {PORT}...")
    app.run(host="0.0.0.0", port=PORT, debug=True)
