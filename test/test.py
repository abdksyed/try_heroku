import requests

resp = requests.post("http://192.168.207.35:5000/predict/", files={"file": open("sample2.jpg", "rb")})

print(resp.text)
