import base64
import os
from tkinter import filedialog
from openai import OpenAI
from load_dotenv import load_dotenv
import pyperclip

load_dotenv()

def encode_image_to_base64(file_path):
    with open(file_path, "rb") as image_file:
        image_data = image_file.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')
        return f"data:image/jpeg;base64,{base64_image}"

# Replace with your OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)


# Ask the user to select images
file_paths = filedialog.askopenfilenames(title="Select Image Files", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

if not file_paths:
    print("No files selected. Exiting.")
else:
    image_urls = [encode_image_to_base64(file_path) for file_path in file_paths]

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "You are a real estate property description generator AI. You generate a comprehensive description of a property based on multiple images we will provide. Generate a markdown for a property listing. It should contain all features of the property written in markdown syntax.",
                    },
                    *[
                        {"type": "image_url", "image_url": {"url": url}} for url in image_urls
                    ],
                ],
            }
        ],
        max_tokens=1300,
    )

    

    generated_markdown = response.choices[0].message.content
    # Copy the text to the clipboard
    pyperclip.copy(generated_markdown)
    print("-----------------------------------------------------")
    print(generated_markdown)

    