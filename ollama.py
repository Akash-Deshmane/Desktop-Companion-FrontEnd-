import requests

url = "http://localhost:11434/api/generate"

prompt = input("ask question")

data={
    "model":"llama3",
    "prompt":prompt,
    "stream":False
}

response = requests.post(url, json=data)

print(response.json()["response"])