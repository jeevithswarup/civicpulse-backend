<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:6366f1,100:8b5cf6&height=200&section=header&text=CivicPulse%20Backend&fontSize=48&fontColor=ffffff&fontAlignY=38&desc=Empowering%20Citizens%20%7C%20Built%20with%20Django%20REST%20Framework&descAlignY=58&descSize=16" width="100%"/>

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![DRF](https://img.shields.io/badge/Django_REST_Framework-3.14-ff1709?style=for-the-badge&logo=django&logoColor=white)](https://www.django-rest-framework.org)
[![JWT](https://img.shields.io/badge/SimpleJWT-5.3-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)](https://django-rest-framework-simplejwt.readthedocs.io)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

<br/>

> **CivicPulse** is a full-stack civic complaint management platform that connects citizens with government departments. Citizens report issues, officers manage resolution pipelines, workers close tasks in the field — all tracked in real time.

<br/>

</div>

---

## ✨ Features at a Glance

```
🔐  JWT Auth with refresh token rotation + blacklisting
👥  4 Roles: Citizen · Officer · Worker · Admin
📍  Haversine duplicate detection (100m radius)
🎫  Auto-generated complaint IDs (CMP-XXXXXXXX)
📊  Role-specific dashboards with aggregated stats
🏢  Department-scoped worker assignment
👍  Community support / upvote system
📸  Cloudinary media upload for resolution proof
🌐  CORS-ready for React frontend integration
```

---

## 🏗️ Architecture

```
civicpulse-backend/
│
├── config/                  # Project settings, URLs, WSGI/ASGI
│   ├── settings.py          # JWT, CORS, DB, media config
│   └── urls.py              # Root URL router
│
├── users/                   # Custom user model + auth
│   ├── models.py            # AbstractUser + role, phone, department
│   ├── serializers.py       # Register, Login, Profile serializers
│   ├── views.py             # Auth views (register, login, profile)
│   └── urls.py              # /api/auth/* endpoints
│
├── complaints/              # Core complaint lifecycle
│   ├── models.py            # Complaint + ComplaintSupport models
│   ├── serializers.py       # Role-specific serializers
│   ├── views.py             # 20+ API views across all roles
│   └── urls.py              # /api/complaints/* endpoints
│
├── departments/             # Department model
├── notifications/           # Notification app (in progress)
├── analytics/               # Analytics app (in progress)
└── mediafiles/              # Media file handling
```

---

## 👤 User Roles

| Role | Can Do |
|------|--------|
| 🟦 **Citizen** | Register, file complaints, track status, upvote issues |
| 🟧 **Officer** | Manage complaint queue, assign workers, update statuses |
| 🟩 **Worker** | View assigned tasks, mark in-progress, upload resolution proof |
| 🟥 **Admin** | Platform overview, create officers, full visibility |

---

## 🔑 API Reference

### Auth — `/api/auth/`

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `POST` | `/register/` | ❌ | Register a new citizen |
| `POST` | `/login/` | ❌ | Login → returns JWT tokens + role |
| `GET` | `/profile/` | ✅ | Get logged-in user details |
| `POST` | `/token/refresh/` | ❌ | Refresh access token |
| `POST` | `/create-officer/` | 🔑 Admin | Create an officer account |

### Complaints — `/api/complaints/`

#### 🟦 Citizen
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/createcomplaint/` | File a new complaint |
| `GET` | `/my/` | List my complaints |
| `PATCH` | `/updatecomplaint/<id>/` | Edit my complaint |
| `DELETE` | `/deletecomplaint/<id>/` | Delete my complaint |
| `GET` | `/citizen-dashboard/` | My stats (total, resolved, pending) |
| `POST` | `/complaints/<id>/support/` | Upvote a complaint |
| `GET` | `/popular-complaints/` | Top supported complaints |
| `GET` | `/nearby-complaints/` | Complaints in area |

#### 🟧 Officer
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/officer/dashboard/` | Officer stats dashboard |
| `GET` | `/officers-complaints/` | Complaints assigned to me |
| `PATCH` | `/assign-officer/<id>/` | Assign officer to complaint |
| `PATCH` | `/status-update/` | Update complaint status |
| `GET` | `/officer/workers/` | List department workers |

#### 🟩 Worker
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/worker-dashboard/` | Worker stats |
| `GET` | `/worker-complaints/` | My assigned tasks |
| `PATCH` | `/assign-worker/<id>/` | Assign worker to complaint |
| `PATCH` | `/complaint-update/<id>/` | Update progress + notes |
| `GET` | `/worker/complaints/<id>/` | Task detail |

#### 🟥 Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/admin-dashboard/` | Platform-wide overview |

---

## 🧠 Key Technical Implementations

### Haversine Duplicate Detection
```python
# Prevents duplicate complaints within 100 metres
def haversine(lat1, lon1, lat2, lon2):
    R = 6_371_000  # Earth's radius in metres
    dlat = radians(float(lat2) - float(lat1))
    dlon = radians(float(lon2) - float(lon1))
    a = sin(dlat/2)**2 + cos(radians(float(lat1))) \
        * cos(radians(float(lat2))) * sin(dlon/2)**2
    return R * 2 * atan2(sqrt(a), sqrt(1 - a))
```

### Auto Complaint ID Generation
```python
def save(self, *args, **kwargs):
    if not self.complaintID:
        import uuid
        self.complaintID = f"CMP-{uuid.uuid4().hex[:8].upper()}"
    super().save(*args, **kwargs)
```

### JWT Token Flow
```
POST /api/auth/login/
  → validates credentials
  → returns { access (15min), refresh (7d), username, role }

POST /api/auth/token/refresh/
  → rotates refresh token (blacklists old one)
  → returns new access token
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- pip

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/jeevithswarup/civicpulse-backend.git
cd civicpulse-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create an admin user
python manage.py createsuperuser

# 6. Start the server
python manage.py runserver
```

Server runs at **`http://localhost:8000`**

### Test the API
```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test@1234","phone":"9876543210"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"Test@1234"}'
```

---

## 🔗 Frontend

The React + TypeScript frontend lives at:
**[github.com/jeevithswarup/civicpulse-spark](https://github.com/jeevithswarup/civicpulse-spark)**

Built with TanStack Router, Tailwind CSS, and shadcn/ui — fully wired to this backend with JWT auth, automatic token refresh, and role-based routing.

---

## 📦 Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | Django 4.2 |
| API | Django REST Framework 3.14 |
| Auth | SimpleJWT 5.3 (access + refresh + blacklist) |
| Database | SQLite (dev) / PostgreSQL-ready |
| Media | Cloudinary + django-cloudinary-storage |
| CORS | django-cors-headers |
| AI/ML | sentence-transformers, scikit-learn, NLTK |
| Server | Gunicorn + Whitenoise |

---

## 🛡️ Security

- ✅ Passwords hashed with Django's PBKDF2
- ✅ JWT tokens expire in 15 minutes
- ✅ Refresh token blacklisting on rotation
- ✅ Role registration locked to `citizen` (officers created by admin only)
- ✅ Department-scoped resource access enforced at API layer
- ✅ CORS restricted to known origins

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:8b5cf6,100:6366f1&height=100&section=footer" width="100%"/>

**Built by [Jeevith Swarup](https://github.com/jeevithswarup)**

</div>
