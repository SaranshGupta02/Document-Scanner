import cv2
import time
import os
from PIL import Image

# Directory to save scanned images
output_dir = "ScannedImages"
os.makedirs(output_dir, exist_ok=True)

# IPWebcam video URL with username and password if required
url = "http://harsh:harsh@172.20.10.11:8080/video"

# Open video stream
cap = cv2.VideoCapture(url)

# Frame counter
frame_count = 0

# Time delay (in seconds)
save_interval = 4  # every 4 seconds
last_saved_time = time.time()

# List to store paths of saved images
image_paths = []

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured
    if not ret:
        print("Failed to grab frame.")
        break

    # Get the current time
    current_time = time.time()

    # Process the frame and save it every 2 seconds
    if current_time - last_saved_time >= save_interval:
        # Convert to grayscale and apply thresholding
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Rotate the image 90 degrees clockwise
        rotated = cv2.rotate(thresh, cv2.ROTATE_90_CLOCKWISE)

        # Save the processed and rotated frame
        filename = f"{output_dir}/page_{frame_count}.jpg"
        cv2.imwrite(filename, rotated)
        print(f"Saved {filename}")
        
        # Append the saved image path to the list
        image_paths.append(filename)

        # Update the last saved time and frame count
        last_saved_time = current_time
        frame_count += 1

        # Display the rotated frame
        cv2.imshow('Processed Stream', rotated)

    # Check if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("Quitting...")
        break

# Release the video capture object and close display window
cap.release()
cv2.destroyAllWindows()

# Convert all saved images to a PDF
if image_paths:
    images = [Image.open(img).convert('RGB') for img in image_paths]
    pdf_path = f"{output_dir}/scanned_document.pdf"
    images[0].save(pdf_path, save_all=True, append_images=images[1:])
    print(f"PDF saved at {pdf_path}")
else:
    print("No images to save as PDF.")
