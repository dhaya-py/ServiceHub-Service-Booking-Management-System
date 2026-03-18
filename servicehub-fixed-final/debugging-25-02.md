# 🔧 ServiceHub Frontend - Complete Setup & Debugging Guide

## 🚨 Common Issues & Solutions

### Issue 1: "Not Found" Error on Registration/Login

**Symptoms:**
- Red "Not Found" toast appears
- Network tab shows 404 errors
- Backend not responding

**Root Causes:**
1. Backend not running
2. Wrong API base URL
3. CORS not configured

**Solutions:**

#### Step 1: Verify Backend is Running
```bash
# Check if backend is running
curl http://127.0.0.1:8000/

# Should return: {"message": "ServiceHub API"}
```

If not running:
```bash
cd your-backend-directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### Step 2: Check API Base URL
Open `js/config.js` and verify:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';  // Must match your backend
```

#### Step 3: Enable CORS in Backend
In your FastAPI backend `main.py`:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### Issue 2: Service Detail Page Shows 404

**Symptoms:**
- Clicking service shows "Error response 404"
- URL is correct but page not found

**Root Cause:**
Missing `service-detail.html` file

**Solution:**
✅ File is now created at: `pages/service-detail.html`

Make sure your services.html links to:
```javascript
window.location.href = `service-detail.html?id=${serviceId}`;
```

---

### Issue 3: Login/Registration Not Working

**Symptoms:**
- Form submits but nothing happens
- Console shows errors
- User not redirected

**Debugging Steps:**

1. **Open Browser DevTools** (F12)
2. **Go to Console tab**
3. **Try to register/login**
4. **Look for errors**

Common errors and fixes:

**Error: "Failed to fetch"**
- Backend not running → Start backend
- Wrong URL → Check config.js

**Error: "CORS policy"**
- Add CORS middleware to backend (see above)

**Error: "422 Unprocessable Entity"**
- Check request body format
- Ensure email/password fields match backend expectations

**Testing Registration:**
```javascript
// Open browser console and test manually:
fetch('http://127.0.0.1:8000/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'test@test.com',
        password: 'test123',
        role: 'customer'
    })
})
.then(r => r.json())
.then(console.log)
.catch(console.error);
```

---

### Issue 4: Bookings Not Loading

**Symptoms:**
- Infinite loading spinner
- No bookings display

**Debugging:**

1. Check if user is authenticated:
```javascript
// In browser console:
console.log(localStorage.getItem('servicehub_token'));
// Should show JWT token
```

2. Test API manually:
```javascript
// Get token
const token = localStorage.getItem('servicehub_token');

// Test bookings endpoint
fetch('http://127.0.0.1:8000/customer/bookings', {
    headers: {
        'Authorization': `Bearer ${token}`
    }
})
.then(r => r.json())
.then(console.log);
```

3. Check backend logs for errors

---

### Issue 5: Modules Not Showing Up

**Missing Files Checklist:**

✅ Required files:
```
pages/
├── service-detail.html         ← NOW CREATED
├── customer/
│   ├── dashboard.html         ← EXISTS
│   └── bookings.html          ← NOW CREATED
├── provider/
│   ├── dashboard.html         ← EXISTS
│   ├── bookings.html          ← NEEDS CREATION
│   ├── services.html          ← NEEDS CREATION
│   └── availability.html      ← NEEDS CREATION
└── admin/
    ├── dashboard.html         ← EXISTS
    ├── users.html             ← NEEDS CREATION
    ├── providers.html         ← NEEDS CREATION
    └── categories.html        ← NEEDS CREATION
```

---

## 🎯 Complete Setup Checklist

### Backend Setup (MUST DO FIRST!)

- [ ] Backend code is ready
- [ ] Database is created and migrations run
- [ ] Backend is running on port 8000
- [ ] CORS is enabled
- [ ] Test endpoint works: `curl http://127.0.0.1:8000/`

### Frontend Setup

- [ ] All files extracted to a directory
- [ ] `js/config.js` has correct API_BASE_URL
- [ ] Frontend is served via http-server or similar
- [ ] NOT opening files directly (file://)

### Testing Flow

1. **Test Backend Alone:**
```bash
# Register user
curl -X POST http://127.0.0.1:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123","role":"customer"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test123"}'
```

2. **Test Frontend:**
- Open: http://localhost:8080 (or your server)
- Go to Register page
- Fill form and submit
- Check browser console for errors
- Should redirect to login

3. **Test Services:**
- Create a service via backend/admin
- Go to Browse Services page
- Should see services
- Click a service
- Should show detail page

---

## 🐛 Debugging Tools

### Browser DevTools

**Console Tab:**
- Shows JavaScript errors
- Network requests
- API responses

**Network Tab:**
- See all API calls
- Check request/response
- Verify status codes

**Application Tab:**
- Check localStorage for token
- Clear storage if needed

### Backend Logs

Watch backend terminal for:
- 404 errors → Endpoint doesn't exist
- 422 errors → Validation failed
- 401 errors → Not authenticated
- 500 errors → Server error

---

## 📊 API Testing

### Using Browser Console

```javascript
// Set API base
const API = 'http://127.0.0.1:8000';

// Test registration
fetch(`${API}/auth/register`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'customer@test.com',
        password: 'customer123',
        role: 'customer'
    })
}).then(r => r.json()).then(console.log);

// Test login
fetch(`${API}/auth/login`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'customer@test.com',
        password: 'customer123'
    })
}).then(r => r.json()).then(d => {
    console.log('Token:', d.access_token);
    localStorage.setItem('servicehub_token', d.access_token);
});

// Test authenticated endpoint
const token = localStorage.getItem('servicehub_token');
fetch(`${API}/me`, {
    headers: {'Authorization': `Bearer ${token}`}
}).then(r => r.json()).then(console.log);
```

---

## ✅ Production Checklist

Before considering your app "production-ready":

### Backend
- [ ] All endpoints return proper status codes
- [ ] Error messages are clear and helpful
- [ ] JWT tokens expire properly
- [ ] Passwords are hashed (never plain text)
- [ ] Database has proper indexes
- [ ] API documentation is up to date

### Frontend
- [ ] All pages load without errors
- [ ] Forms validate input
- [ ] Error messages are user-friendly
- [ ] Loading states show properly
- [ ] Success messages confirm actions
- [ ] No console errors
- [ ] Works on mobile/tablet
- [ ] All links work correctly

### Integration
- [ ] Registration creates user in DB
- [ ] Login returns valid JWT token
- [ ] Token is sent with authenticated requests
- [ ] Logout clears token
- [ ] Role-based routing works
- [ ] Booking lifecycle works end-to-end
- [ ] Provider can manage services
- [ ] Admin can see all data

---

## 🔥 Quick Fixes

### Clear Everything and Start Fresh

```javascript
// In browser console:
localStorage.clear();
sessionStorage.clear();
location.reload();
```

### Force Backend Restart

```bash
# Kill existing backend
pkill -f uvicorn

# Start fresh
cd backend-directory
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Verify CORS

```bash
# Test CORS
curl -H "Origin: http://localhost:8080" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type" \
  -X OPTIONS \
  http://127.0.0.1:8000/auth/login -v
```

Should see: `Access-Control-Allow-Origin: *`

---

## 📞 Still Having Issues?

### Diagnostic Script

Run this in browser console:
```javascript
console.log('=== ServiceHub Diagnostics ===');
console.log('Token:', localStorage.getItem('servicehub_token') ? 'Present' : 'Missing');
console.log('User:', localStorage.getItem('servicehub_user'));
console.log('API URL:', API_BASE_URL);

// Test API connectivity
fetch(API_BASE_URL)
  .then(r => r.json())
  .then(d => console.log('Backend Status:', 'OK', d))
  .catch(e => console.log('Backend Status:', 'FAILED', e));
```

### Common Error Codes

- **404**: Endpoint doesn't exist or wrong URL
- **401**: Not authenticated (missing/invalid token)
- **403**: Not authorized (wrong role)
- **422**: Validation error (check request body)
- **500**: Backend error (check backend logs)

---

## 🎓 Understanding the Flow

### Registration Flow:
1. User fills form
2. Frontend sends POST to `/auth/register`
3. Backend creates user in database
4. Backend returns user info
5. Frontend redirects to login

### Login Flow:
1. User enters email/password
2. Frontend sends POST to `/auth/login`
3. Backend verifies credentials
4. Backend returns JWT token
5. Frontend stores token in localStorage
6. Frontend redirects to role-specific dashboard

### Booking Flow:
1. Customer browses services
2. Clicks "Book" on a service
3. Selects date and time
4. Frontend sends POST to `/bookings`
5. Backend creates booking (status: pending)
6. Provider sees booking in their dashboard
7. Provider accepts/rejects
8. Customer is notified

---

## 🚀 Next Steps

Once basic functionality works:

1. **Add remaining pages**
2. **Implement all CRUD operations**
3. **Add real-time notifications**
4. **Improve error handling**
5. **Add loading skeletons**
6. **Implement pagination**
7. **Add search functionality**
8. **Optimize performance**

---

**Remember:** 
- Always check backend logs first
- Use browser DevTools extensively
- Test APIs in isolation before frontend
- Clear cache/localStorage when stuck
- Console.log is your friend!

Good luck! 🌟