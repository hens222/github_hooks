import requests
from PIL import Image
from io import BytesIO

def capture_screenshot(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Create an in-memory file-like object
        image_data = BytesIO(response.content)

        # Open the image using Pillow
        image = Image.open(image_data)

        # Save the image to a file or store it in a database
        # Example: Saving the image in the media directory
        image_path = 'media/screenshot.png'
        image.save(image_path)

        # Return the path to the saved image
        return image_path
