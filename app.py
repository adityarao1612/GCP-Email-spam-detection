#%%
from PIL import Image, ImageGrab, ImageTk  # Import ImageTk from PIL

from PIL import ImageGrab
import tkinter as tk
from io import BytesIO
import requests
import json
import io
import base64

from PIL import Image, ImageDraw
import numpy as np


global_image = None
label = None  # Define label globally


def outline_rows_and_update_gui(spam):
    global global_image, label

    # Call outline_rows to modify the image
    outline_rows(spam)

    # Load the modified image
    modified_image = Image.open('modified_image.png')

    # Convert PIL Image to Tkinter PhotoImage
    photo = ImageTk.PhotoImage(modified_image)

    # Update the label with the modified image
    label.config(image=photo)
    label.image = photo  # Keep a reference to avoid garbage collection


def outline_rows( spam):
    global global_image

    # Load image and convert to numpy array
    image = global_image
    img_array = np.array(image)

    # Get dimensions of the image
    height, width, channels = img_array.shape

    # Create a PIL ImageDraw object
    draw = ImageDraw.Draw(image)

    # Define outline colors
    spam_color = (255, 0, 0)   # Red
    not_spam_color = (0, 255, 0)   # Blue (you can choose any color)

    # Iterate through each row
    for i in range(len(spam)):
        if spam[i]:  # If it's spam
            outline_color = spam_color
        else:        # If it's not spam
            outline_color = not_spam_color

        # Draw a rectangle to outline the row
        top_left = (0, i * height // len(spam))
        bottom_right = (width, (i + 1) * height // len(spam))
        draw.rectangle([top_left, bottom_right], outline=outline_color, width=5)

    # Save the modified image
    image.save('modified_image.png')
    print("Modified image saved as 'modified_image.png'.")




def import_from_clipboard():
    global global_image, label

    # Grab the image from the clipboard
    image = ImageGrab.grabclipboard()

    # Check if an image was successfully grabbed
    if image is None:
        print("No image found in the clipboard.")
    else:
        # Save the image to a buffer in PNG format
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        buffer.seek(0)

        # Create a PhotoImage object from the buffer
        photo = tk.PhotoImage(data=buffer.read())

        # Create a label to display the image
        label = tk.Label(root, image=photo)
        label.image = photo  # Keep a reference to avoid garbage collection
        label.pack()

    global_image = image

def get_ocr_data():
    global global_image
    image=global_image
    # Define necessary variables
    bearer_token = ""          # fill details of your GCP bearer token
    url = ""                   # endpoint of your Document Ai API

    # Get the image from the clipboard
    image = ImageGrab.grabclipboard()

    # Check if an image was successfully grabbed

    if image is None:
        print("No image found. Please import an image from the clipboard first.")
        return None

    else:
        # Convert image to base64
        buffered = io.BytesIO()
        image.save(buffered, format="PNG")
        image_content = base64.b64encode(buffered.getvalue()).decode('utf-8')

        # Prepare headers for the API request
        headers = {
            "Authorization": f"Bearer {bearer_token}",
            "Content-Type": "application/json; charset=utf-8"
        }

        # Prepare the JSON payload
        json_data = {
            "raw_document": {
                "content": image_content,
                "mimeType": "image/png"  # MIME type should match the image format
            }
        }

        # Send the POST request to the API endpoint
        try:
            response = requests.post(url, headers=headers, json=json_data)
            response.raise_for_status()  # Raise an exception for bad status codes

            # Check if the request was successful
            if response.status_code == 200:
                ocr_data = response.json()
                x=json.dumps(ocr_data)
                data = json.loads(x)

                text = data['document']['text']

                # Split text into a list based on newline characters
                text_list = text.split("\n")

                # Print the resulting list
                print(text_list)
                return text_list

            else:
                print(f"OCR request failed with status code: {response.status_code}")
                print("Response content:")
                print(response.text)
        except requests.exceptions.RequestException as e:
            print(f"Error processing document: {e}")




def scan_spam():

    emails = ["how are you today","nice meeting you!"]
    emails= get_ocr_data()
    # print(emails)

    # Define necessary variables
    bearer_token = ""          #fill details of your bearer token
    url = ""                   #end point of your autoML model trained on spam detection

    headers = {
        "Authorization": f"Bearer {bearer_token}",
        "Content-Type": "application/json; charset=utf-8"
    }


    l=[]
    for i in emails:
        if len(i)>20:

            # Define JSON payload
            payload = {
                "instances": [{
                    "mimeType": "text/plain",
                    "content": i
                }]
            }

            # Prepare headers

            # Make the POST request
            response = requests.post(url, headers=headers, json=payload)
            if response.status_code == 200:
                # Parse JSON response
                json_response = json.loads(response.text)

                # Extract confidence for "spam" class (index 1)
                spam_confidence = json_response["predictions"][0]["confidences"][1]
                ham_confidence = json_response["predictions"][0]["confidences"][0]

                # Check if spam confidence is greater than 50%
                if spam_confidence>0.5:
                    l.append(True)
                    print("SPAM with confidence: ", spam_confidence)
                else:
                    l.append(False)
                    print("NOT SPAM with confidence: ", ham_confidence)
            else:
                print(f"Request failed with status code {response.status_code}")
    print(l)
    outline_rows_and_update_gui(l)



# Create the main Tkinter window
root = tk.Tk()
root.title("Image Viewer")

# Button to import from clipboard
button = tk.Button(root, text="Import from Clipboard", command=import_from_clipboard)
button.pack(pady=10)

# Button to scan for SPAM
button1 = tk.Button(root, text="Scan for SPAM", command=scan_spam)
button1.pack(pady=10)

# Start the main event loop
root.mainloop()


#%%