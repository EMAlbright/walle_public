from openai import OpenAI
import base64

client = OpenAI(api_key= API_KEY)

def encodeImage(imagepath):
    with open(imagepath, "rb") as imageFile:
        return base64.b64encode(imageFile.read()).decode('utf-8')


def analyze(encoded_image):
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant",
            
            },
            {
                "role": "user",
                "content": [
                            {
                              "type": "text",
                              "text": "describe the image you see. describe everything in detail, act intrigued and interested."
                                },
                            {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }    
            ],
            max_tokens=300
        )
    return response.choices[0].message.content

