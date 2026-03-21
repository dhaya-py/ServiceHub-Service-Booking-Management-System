import requests
try:
    print("Testing /admin/bookings...")
    r = requests.get("http://127.0.0.1:8000/admin/bookings")
    print("Admin bookings:", r.status_code)

    print("Testing slots...")
    # hardcode a provider and service that exists
    r2 = requests.get("http://127.0.0.1:8000/availability/provider/1/slots?service_id=1&date_str=2026-03-24")
    print("Slots 200?:", r2.status_code)
    slots = r2.json()
    print("Slots returned:", len(slots))
    for s in slots[:5]:
        print("-", s)
except Exception as e:
    print("Error:", e)
