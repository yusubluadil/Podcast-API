# 🎧 Spotify Podcast API Wrapper (Django + DRF)

Bu layihə Spotify Web API üzərindən **podcast (show və episode)** məlumatlarını çəkmək üçün hazırlanmış sadə Django REST Framework tətbiqidir.  

Layihədə 3 əsas endpoint mövcuddur:

1. `GET /podcasts/search?q={query}` → axtarış əsasında podcast siyahısı  
2. `GET /podcasts/{showId}` → seçilmiş podcast haqqında detallı məlumat  
3. `GET /podcasts/{showId}/episodes` → podcast-ın epizod siyahısı  

---

## 🚀 Texnologiyalar

- Python 3.10  
- Django 5.2  
- Django REST Framework  
- Gunicorn (production server)  
- Docker & Docker Compose  
- Spotify Web API  

---

## ⚙️ Quraşdırma (Docker ilə)

### 1. Ətraf mühit dəyişənləri (`.env` faylı)

Layihənin kökünə `.env` faylı əlavə edin:

```env
SECRET_KEY=supersecretkey
DJANGO_SETTINGS_MODULE=core.settings.production or core.settings.development
DJANGO_PORT=8000
ALLOWED_HOSTS=* (127.0.0.1,localhost)
CSRF_TRUSTED_ORIGINS=* (http://127.0.0.1:8000)
CORS_ALLOWED_ORIGINS=* (http://127.0.0.1:8000,http://localhost:5173)

SPOTIFY_CLIENT_ID=your_client_id_here (660b1fe647c14dcca3cccb9550c36451)
SPOTIFY_CLIENT_SECRET=your_client_secret_here (85b825811a2844b2a7b63e02fddaabb0)
```

### 2. Docker build və run

```env
docker-compose up --build -d
```

API default olaraq ```http://127.0.0.1:8000``` üzərində işləyəcək.


## 📡 API Endpoint-lər

### 1. Podcast axtarışı
```env
GET /podcasts/search?q={query}&limit=10&offset=0&market={market}
```
Nümunə:
```env
curl "http://127.0.0.1:8000/api/v1/podcasts/search?q=technology&limit=5&market=AZ"
```

### 2. Podcast detalları
```env
GET /podcasts/{showId}
```
Nümunə:
```env
curl "http://127.0.0.1:8000/api/v1/podcasts/38bS44xjbVVZ3No3ByF1dJ"
```

### 3. Podcast epizodları
```env
GET /podcasts/{showId}/episodes?limit=10&offset=0
```
Nümunə:
```env
curl "http://127.0.0.1:8000/api/v1/podcasts/38bS44xjbVVZ3No3ByF1dJ/episodes?limit=3"
```

## 📌 Qeydlər

- Spotify access token cache-də saxlanılır (1 saat etibarlıdır).

- Token avtomatik yenilənir, əlavə müdaxiləyə ehtiyac yoxdur.

- CORS üçün ```CORS_ALLOWED_ORIGINS``` dəyişəni ```.env``` faylında konfiqurasiya edilməlidir.


## 🛠️ Dokumentasiya

[Dokumentasiya üçün klik et](https://documenter.getpostman.com/view/26221248/2sB3BKF8Yf)