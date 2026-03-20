import requests

BASE_URL = "http://127.0.0.1:8000"

def test_assign():
    # Login as Admin
    resp = requests.post(f"{BASE_URL}/api/auth/token", data={
        "username": "admin@test.com",
        "password": "password123"
    })
    
    if resp.status_code != 200:
        print("Admin login failed:", resp.text)
        return
        
    admin_token = resp.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    # Get all bookings
    resp = requests.get(f"{BASE_URL}/bookings/admin/all", headers=admin_headers)
    if resp.status_code != 200:
        print("Failed to get bookings:", resp.text)
        return
        
    bookings = resp.json()
    if not bookings:
        print("No bookings found to test assignment.")
        return
        
    booking = bookings[0]
    booking_id = booking["id"]
    current_provider_id = booking.get("provider_id")
    
    print(f"Assigning booking {booking_id} to provider 1...")
    
    # Assign to provider1 (assumed ID 5 based on typical DB sequence, or we can just query users)
    # Let's get providers first
    resp = requests.get(f"{BASE_URL}/providers/", headers=admin_headers)
    providers = resp.json()
    if not providers:
        print("No providers found.")
        return
        
    new_provider_id = providers[0]["id"]
    
    # Call new endpoint
    resp = requests.post(f"{BASE_URL}/bookings/admin/{booking_id}/assign?provider_id={new_provider_id}", headers=admin_headers)
    
    if resp.status_code == 200:
        print(f"Successfully reassigned booking {booking_id} to provider {new_provider_id}.")
        updated_booking = resp.json()
        print("New status:", updated_booking["status"])
    else:
        print("Failed to assign:", resp.status_code, resp.text)

if __name__ == "__main__":
    test_assign()
