# ⚡ QUICK START - Test Everything in 5 Minutes

## 🚀 Start Backend (Terminal 1)

```bash
cd service-booking-platform
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Wait for:** `Application startup complete`

---

## 🌐 Start Frontend (Terminal 2)

```bash
cd servicehub-final-fixed
python3 -m http.server 8080
```

**Wait for:** `Serving HTTP on 0.0.0.0 port 8080`

---

## ✅ Test 1: Backend Health (Terminal 3)

```bash
curl http://127.0.0.1:8000/
```

**Expected:** `{"message":"Service Booking Platform API running"}`

✅ If you see this, backend is working!

---

## ✅ Test 2: Registration

**Open:** http://localhost:8080/pages/register.html

**Fill:**
- Email: `test@example.com`
- Password: `test123456`
- Select: "Book Services" (Customer)

**Click:** "Create Account"

**Expected:** ✅ Green success toast + redirect to login

---

## ✅ Test 3: Login

**On login page:**
- Email: `test@example.com`
- Password: `test123456`

**Click:** "Sign In"

**Expected:** ✅ Redirect to dashboard

---

## ✅ Test 4: Check Browser Console

**Press F12** → Console tab

**Should see:**
```
✅ No errors
✅ "API URL: http://127.0.0.1:8000/api"
✅ Token stored in localStorage
```

---

## ✅ Test 5: Verify Token Stored

In browser console, type:
```javascript
localStorage.getItem('servicehub_token')
```

**Expected:** Long JWT token string

---

## 🎉 SUCCESS!

If all tests passed, your application is **fully working**!

---

## 🐛 If Something Failed

### Registration Shows "Not Found"
```bash
# Check backend logs for errors
# Verify backend is running on port 8000
curl http://127.0.0.1:8000/api/auth/register
```

### Login Shows "Not Found"
**Check:**
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try login
4. Check the request URL - should be: `http://127.0.0.1:8000/api/auth/token`

### CORS Error
**Verify CORS in backend:**
```bash
curl -H "Origin: http://localhost:8080" \
  -H "Access-Control-Request-Method: POST" \
  -X OPTIONS \
  http://127.0.0.1:8000/api/auth/register -v
```

Should see: `access-control-allow-origin: *`

---

## 📊 Verify API Endpoints

```bash
# Health
curl http://127.0.0.1:8000/

# Services (should work without auth)
curl http://127.0.0.1:8000/services

# Auth endpoints
curl http://127.0.0.1:8000/api/auth/register
curl http://127.0.0.1:8000/api/auth/token
```

---

## 💡 Pro Tip: Browser Console Testing

```javascript
// Test registration
fetch('http://127.0.0.1:8000/api/auth/register', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        email: 'console@test.com',
        name: 'Console Test',
        password: 'console123'
    })
})
.then(r => r.json())
.then(d => console.log('✅ Registration:', d))
.catch(e => console.error('❌ Error:', e));

// Test login
const formData = new URLSearchParams();
formData.append('username', 'test@example.com');
formData.append('password', 'test123456');

fetch('http://127.0.0.1:8000/api/auth/token', {
    method: 'POST',
    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
    body: formData
})
.then(r => r.json())
.then(d => console.log('✅ Token:', d.access_token))
.catch(e => console.error('❌ Error:', e));
```

---

## 🎯 Final Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 8080
- [ ] Registration works
- [ ] Login works
- [ ] Dashboard loads
- [ ] No console errors
- [ ] Token in localStorage

**All checked?** You're ready for your presentation! 🎉
