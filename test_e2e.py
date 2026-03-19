import requests

BASE_URL = "http://127.0.0.1:8000"

def test_flow():
    # 1. Login as Provider
    print("Testing Provider Login...")
    resp = requests.post(f"{BASE_URL}/api/auth/token", data={
        "username": "provider1@test.com",
        "password": "password123"
    })
    
    if resp.status_code != 200:
        print("Provider login failed:", resp.text)
        return
    prov_token = resp.json()["access_token"]
    prov_headers = {"Authorization": f"Bearer {prov_token}"}
    print("Provider logged in successfully.")

    # 2. Get Provider Dashboard
    print("Testing Provider Dashboard...")
    resp = requests.get(f"{BASE_URL}/provider/dashboard/summary", headers=prov_headers)
    print("Provider Dashboard status:", resp.status_code)
    if resp.status_code != 200:
        print("Error details:", resp.text)
        
    # 3. Get Provider Bookings
    print("Testing Provider Bookings...")
    resp = requests.get(f"{BASE_URL}/bookings/provider/me", headers=prov_headers)
    print("Provider Bookings status:", resp.status_code)
    if resp.status_code == 200:
        bookings = resp.json()
        print(f"Found {len(bookings)} bookings for provider.")
        for b in bookings:
            print(f"Booking ID: {b.get('id')} - Status: {b.get('status')}")
    else:
        print("Error details:", resp.text)

    # 4. Login as Admin
    print("\nTesting Admin Login...")
    resp = requests.post(f"{BASE_URL}/api/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    if resp.status_code == 200:
        admin_token = resp.json()["access_token"]
        admin_headers = {"Authorization": f"Bearer {admin_token}"}
        
        # Test Admin Dashboard
        resp = requests.get(f"{BASE_URL}/admin/dashboard", headers=admin_headers)
        print("Admin Dashboard status:", resp.status_code)
        if resp.status_code != 200:
            print("Error details:", resp.text)
            
        # Test Admin Bookings
        resp = requests.get(f"{BASE_URL}/bookings/admin/all", headers=admin_headers)
        print("Admin Bookings status:", resp.status_code)
        if resp.status_code != 200:
            print("Error details:", resp.text)
    else:
        print("Admin login failed:", resp.text)

if __name__ == "__main__":
    test_flow()
