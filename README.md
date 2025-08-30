# AuctionCraft - Django REST API

[![Django](https://img.shields.io/badge/Django-4.2+-green.svg)](https://djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.14+-blue.svg)](https://www.django-rest-framework.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org/)


A robust Django REST Framework backend for an auction platform with JWT authentication, Stripe payments, and real-time bidding capabilities.

## 🚀 Features

- **Authentication & Authorization**
  - JWT-based authentication with Simple JWT
  - OTP (One-Time Password) email verification
  - User registration and profile management
  - Token refresh mechanism

- **Auction System**
  - Product listings with categories
  - Real-time bidding system
  - Auction management (create, close, monitor)
  - Bid history tracking

- **Payment Integration**
  - Stripe payment processing
  - Payment intent creation
  - Webhook handling for payment events
  - Secure payment flow

- **API Architecture**
  - RESTful API design with ViewSets
  - Automatic API documentation
  - Pagination support
  - Clean separation of concerns

## 📋 Prerequisites

- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)
- Stripe account (for payment processing)
- Email service (for OTP delivery)

## 🛠️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/auctioncraft-api.git
cd auctioncraft-api
```

### 2. Environment Configuration
```bash
# Copy the environment template
cp .env .env.local

# Edit .env.local with your configuration
nano .env.local  # or use your preferred editor
```

**Required Environment Variables:**
```env
# Django
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=sqlite:///db.sqlite3

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=7  # days
```

### 3. Virtual Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Database Setup
```bash
# Apply migrations
python manage.py migrate

# Create superuser account
python manage.py createsuperuser

# Load sample data (optional)
python manage.py loaddata fixtures/sample_data.json
```

### 5. Run the Development Server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/api/`

## 📚 API Documentation

### Base URL
```
http://127.0.0.1:8000/api/
```

### Authentication Endpoints

#### Request OTP
```http
POST /api/auth/otp/request/
Content-Type: application/json

{
  "email": "user@example.com"
}
```

#### Verify OTP & Get Tokens
```http
POST /api/auth/otp/verify/
Content-Type: application/json

{
  "email": "user@example.com",
  "code": "123456"
}
```

#### Refresh Access Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### User Management

#### Register New User
```http
POST /api/users/register/
Content-Type: application/json

{
  "email": "newuser@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```

#### Get User Profile
```http
GET /api/users/me/
Authorization: Bearer <access_token>
```

### Auction System

#### List Categories
```http
GET /api/categories/
```

#### List Products
```http
GET /api/products/
# Optional query parameters:
# ?category=1&search=keyword&ordering=-created_at&page=1&page_size=12
```

#### Get Product Details
```http
GET /api/products/{id}/
```

#### Create Product
```http
POST /api/products/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "name": "Vintage Watch",
  "description": "A beautiful vintage timepiece",
  "category": 1,
  "starting_bid": 100.00,
  "reserve_price": 200.00,
  "auction_end_time": "2024-12-31T23:59:59Z"
}
```

#### Place Bid
```http
POST /api/products/{id}/bids/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "amount": 150.00
}
```

#### Close Auction
```http
POST /api/products/{id}/close_auction/
Authorization: Bearer <access_token>
```

### Payment Processing

#### Create Payment Intent
```http
POST /api/payments/create-payment-intent/
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "product_id": 1
}
```

#### Stripe Webhook Handler
```http
POST /api/stripe/webhook/
Stripe-Signature: t=1234567890,v1=...
Content-Type: application/json

# Stripe webhook payload
```

### Notifications

#### Get User Notifications
```http
GET /api/auth/notifications/
Authorization: Bearer <access_token>
```

## 🔧 Configuration Options

### Pagination Settings
```python
# settings.py
REST_FRAMEWORK = {
    'PAGE_SIZE': 12,
    'PAGE_SIZE_QUERY_PARAM': 'page_size',
    'MAX_PAGE_SIZE': 100,
}
```

### JWT Configuration
```python
# Customize JWT settings in settings.py
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
}
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
python manage.py test

# Run specific test module
python manage.py test auctions.tests

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### API Testing with curl
```bash
# Test OTP request
curl -X POST http://127.0.0.1:8000/api/auth/otp/request/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com"}'

# Test product listing
curl -X GET http://127.0.0.1:8000/api/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 🚀 Deployment

### Production Settings
1. Set `DEBUG=False` in production
2. Configure proper database (PostgreSQL recommended)
3. Set up Redis for caching and sessions
4. Configure static file serving
5. Set up proper logging
6. Use environment variables for all secrets

### Docker Deployment (Optional)
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "auctioncraft.wsgi:application"]
```

## 📁 Project Structure

```
auctioncraft/
├── auctioncraft/           # Main project directory
│   ├── settings.py         # Django settings
│   ├── urls.py            # URL configuration
│   └── wsgi.py            # WSGI configuration
├── auctions/              # Auction app
│   ├── models.py          # Data models
│   ├── serializers.py     # DRF serializers
│   ├── views.py           # API views
│   └── urls.py           # App URLs
├── payments/              # Payment handling
│   ├── services.py        # Payment logic
│   └── webhooks.py        # Stripe webhooks
├── users/                 # User management
│   ├── models.py          # User models
│   └── views.py           # User views
├── requirements.txt       # Python dependencies
├── .env                   # Environment template
└── manage.py             # Django management
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request



