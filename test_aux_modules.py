import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

def get_token(username, password):
    resp = requests.post(f"{BASE_URL}/api/auth/token", data={"username": username, "password": password})
    return resp.json().get("access_token")

def test_aux_modules():
    print("Testing Auxiliary Modules...")
    
    # Get Tokens
    try:
        admin_token = get_token("admin@test.com", "password123")
        provider_token = get_token("provider1@test.com", "password123")
        customer_token = get_token("customer1@test.com", "password123")
    except Exception as e:
        print(f"Failed to login: {e}")
        return

    auth = {
        "admin": {"Authorization": f"Bearer {admin_token}"},
        "provider": {"Authorization": f"Bearer {provider_token}"},
        "customer": {"Authorization": f"Bearer {customer_token}"}
    }

    # 1. Admin configures a category
    print("\n--- Testing Categories ---")
    resp = requests.post(f"{BASE_URL}/categories/", headers=auth["admin"], json={
        "name": "New Test Category",
        "description": "Created by automated audit test"
    })
    if resp.status_code == 200:
        cat_id = resp.json().get("id")
        print("Category created successfully. ID:", cat_id)
    else:
        print("Category Creation Failed:", resp.status_code, resp.text)
        cat_id = None

    # 2. Search Services
    print("\n--- Testing Search & Services ---")
    resp = requests.get(f"{BASE_URL}/search/services?q=Pipe")
    if resp.status_code == 200:
        print("Search Services OK. Found:", len(resp.json()["items"]), "items")
    else:
        print("Search Services Failed:", resp.status_code, resp.text)

    # 3. Provider Availability
    print("\n--- Testing Provider Availability ---")
    # Provider sets weekly availability (e.g., Monday 9 AM to 5 PM)
    resp = requests.put(f"{BASE_URL}/availability/provider/weekly", headers=auth["provider"], json={
        "schedule": [
            {"weekday": 1, "start_time": "09:00:00", "end_time": "17:00:00", "is_active": True}
        ]
    })
    if resp.status_code == 200:
        print("Provider Weekly Availability OK.")
    else:
        print("Provider Weekly Availability Failed:", resp.status_code, resp.text)

    # 4. User Profiles
    print("\n--- Testing User Profiles ---")
    resp = requests.put(f"{BASE_URL}/api/auth/me", headers=auth["customer"], json={
        "name": "Updated Customer Name",
        "phone": "9998887776",
        "address": "123 Customer St"
    })
    if resp.status_code == 200:
        print("Customer Profile Update OK.")
    else:
        print("Customer Profile Update Failed:", resp.status_code, resp.text)

    # 5. Reviews
    print("\n--- Testing Reviews ---")
    # Need a completed booking to review usually, or a basic review endpoint
    # Find a provider ID first
    prov_req = requests.get(f"{BASE_URL}/api/auth/me", headers=auth["provider"])
    if prov_req.status_code == 200:
        p_id = prov_req.json()["id"]
        # Assuming there is a completed booking from previous tests for customer1...
        # Wait, if not, it might throw a 400. Let's try reviewing the provider directly.
        # But wait, review usually requires a booking ID. I'll just check if the endpoint exists.
        resp = requests.post(f"{BASE_URL}/reviews/", headers=auth["customer"], json={
            "provider_id": p_id,
            "rating": 5,
            "comment": "Excellent service!"
        })
        if resp.status_code == 200:
            print("Create Review OK.")
            rev_id = resp.json()["id"]
        else:
            print("Create Review Failed (often due to missing booking validation, which is fine if it responds 400 instead of 404):", resp.status_code, resp.text)
            rev_id = None
            
        if rev_id:
            # Check Admin delete
            resp = requests.delete(f"{BASE_URL}/admin/reviews/{rev_id}", headers=auth["admin"])
            print("Admin Delete Review Response:", resp.status_code)

if __name__ == "__main__":
    test_aux_modules()
