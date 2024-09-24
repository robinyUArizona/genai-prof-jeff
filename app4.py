
import streamlit as st
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import base64
import httpx
from openai import OpenAI
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import requests

def modify_image(image, prompt):
    # Initialize the GPT model
    model = ChatOpenAI(model="gpt-4o-mini")

    # Convert the uploaded image to base64
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    image_data = base64.b64encode(buffered.getvalue()).decode("utf-8")

    # Create a message with both text and the image
    message = HumanMessage(
        content=[
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_data}"}},
        ],
    )

    # Get response with a modified prompt from GPT
    response = model.invoke([message])
    cartoon_prompt = response.content

    # Initialize the DALL-E model to generate the image
    client = OpenAI()

    # Generate the image based on the GPT-generated cartoon prompt
    response = client.images.generate(
        model="dall-e-3",
        prompt=cartoon_prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )

    # Get the image URL from DALL-E
    image_url = response.data[0].url

    # Fetch the generated image
    response2 = requests.get(image_url)
    img = Image.open(BytesIO(response2.content))

    return img

# Streamlit app
st.title("Cartoonify Image with Multimodal LLM")

# Image upload
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    # Open the image using PIL
    image = Image.open(uploaded_image)

    # Display the original image
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Modify the image to look like a cartoon
    st.write("Generating cartoon version...")
    cartoon_img = modify_image(image, "Output a prompt that would render this image as a cartoon.")

    # Display the cartoonified image
    st.image(cartoon_img, caption='Cartoonified Image', use_column_width=True)

    # Provide an option to download the cartoonified image
    buffered = BytesIO()
    cartoon_img.save(buffered, format="JPEG")
    st.download_button(
        label="Download Cartoon Image",
        data=buffered.getvalue(),
        file_name="cartoon_image.jpg",
        mime="image/jpeg"
    )
