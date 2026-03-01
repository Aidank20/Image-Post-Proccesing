import requests
from PIL import Image, ImageEnhance, ImageFilter
from io import BytesIO
from Config import API_KEY

def generate_image_from_text(prompt):
    API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {"inputs": prompt,}
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code ==200:
        image_bytes=BytesIO(response.content)
        pil_image=Image.open(image_bytes)
        return pil_image
    else:
        raise Exception(f"Error generating image: {response.status_code}:{response.text}")
def post_proccesing(image):
    enhancer=ImageEnhance.Brightness(image)
    bright_image=enhancer.enhance(1.5)
    enhancer=ImageEnhance.Contrast(bright_image)
    contrast_image=enhancer.enhance(1.5)
    soft_image=contrast_image.filter(ImageFilter.GaussianBlur(radius=2))
    return soft_image
def main():
    print("Welcome to our image Workshop\ntype 'exit' to quit")
    while True:
        user_input=input(">>Enter your description")
        if user_input.lower()=='exit':
            break    
        try:
            print("Generating image...(this may take a while) " )
            image=generate_image_from_text(user_input)
            print("Proccesing image...")
            proccesed_image=post_proccesing(image)
            proccesed_image.show()
            save_option=input("Do you want to save the image? (yes/no)")
            if save_option.lower()=='yes':
                file_name=input("Enter a file name to save the image: ")
                proccesed_image.save(f"{file_name}.png")
                print(f"Image saved as {file_name}.png")
        except Exception as e:
            print(f"An error occurred: {e}\n")
            print("Tip: If the error is 401 or 403, check if you accepted the model license on HuggingFace.co")
if __name__=="__main__":
    main()                    
