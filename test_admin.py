import requests
resp = requests.post("http://127.0.0.1:8000/api/auth/token", data={"username":"admin@test.com", "password":"password123"})
token = resp.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}
r = requests.get("http://127.0.0.1:8000/admin/users", headers=headers)
print("Users Status:", r.status_code)
if r.status_code == 200:
    print(f"Loaded {len(r.json())} users successfully")
else:
    print("Error:", r.text)
