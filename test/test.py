import requests

resp = requests.post("http://localhost:5000/predict/", files={"file": open("sample2.jpg", "rb")})

print(resp.text)
