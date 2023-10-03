import openai
import requests

openai.api_key = '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'

response = openai.Image.create(
    prompt="a white siamese cat",
    n=1,
    size="1024x1024"
)
image_url = response['data'][0]['url']
print(image_url)