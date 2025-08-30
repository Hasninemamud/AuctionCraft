<div align="center">
  
# AuctionCraft - Django REST API 
  
</div>

This is a ready-to-run Django REST Framework backend skeleton for AuctionCraft.  
It exposes API endpoints for products, bids, categories, user registration & JWT auth, and Stripe payment intent creation + webhook handling.

## Features implemented
- Django + DRF API (ViewSets + routers)
- JWT authentication (Simple JWT)
- Basic auction models: Category, Product, Bid
- Stripe payment intent creation endpoint and webhook handler
- Separation of payment logic into a service module (SOLID: Single Responsibility)
- Clear comments and straightforward structure for integration with a React frontend

## How to run locally (Linux / macOS / Windows WSL)
1. Copy `.env` and update secrets:
   ```bash
   cp .env .env.local
   # edit .env.local and provide REAL STRIPE keys and DJANGO_SECRET_KEY
   ```
2. Create and activate virtualenv
   ```bash
   python -m venv venv
   source venv/bin/activate  # on Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Apply migrations and create superuser
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```
4. Run development server
   ```bash
   python manage.py runserver
   ```
5. Open http://127.0.0.1:8000/api/ for the API router.

## API Endpoints

### Authentication
- **Request OTP**:  
  `POST /api/auth/otp/request/`  
  Request an OTP for email-based authentication.  
  **Payload**: `{ "email": "user@example.com" }`

- **Verify OTP**:  
  `POST /api/auth/otp/verify/`  
  Verify the OTP and receive JWT tokens.  
  **Payload**: `{ "email": "user@example.com", "code": "123456" }`

- **Refresh Token**:  
  `POST /api/auth/token/refresh/`  
  Refresh the JWT access token using the refresh token.  
  **Payload**: `{ "refresh": "your_refresh_token" }`

- **Obtain Token (if applicable)**:  
  `POST /api/auth/token/`  
  Obtain JWT tokens using username and password (if enabled).  
  **Payload**: `{ "username": "user", "password": "password" }`

---

### Users
- **User Registration**:  
  `POST /api/users/register/`  
  Register a new user.  
  **Payload**: `{ "email": "user@example.com", "password": "password123" }`

- **User Profile**:  
  `GET /api/users/me/`  
  Retrieve the authenticated user's profile.  
  **Requires**: JWT token.

---

### Auctions
- **List Categories**:  
  `GET /api/categories/`  
  Retrieve a list of all auction categories.

- **List Products**:  
  `GET /api/products/`  
  Retrieve a list of all products available for auction.

- **Retrieve Product**:  
  `GET /api/products/{id}/`  
  Retrieve details of a specific product.

- **Create Product**:  
  `POST /api/products/`  
  Create a new product for auction.  
  **Payload**: `{ "name": "Product Name", "category": 1, "starting_bid": 100.0 }`

- **Place Bid**:  
  `POST /api/products/{id}/bids/`  
  Place a bid on a product.  
  **Payload**: `{ "amount": 150.0 }`

- **Close Auction**:  
  `POST /api/products/{id}/close_auction/`  
  Close an auction manually (staff or seller only).

---

### Notifications
- **List Notifications**:  
  `GET /api/auth/notifications/`  
  Retrieve a list of notifications for the authenticated user.  
  **Requires**: JWT token.

---

### Payments (Stripe Integration)
- **Create Payment Intent**:  
  `POST /api/payments/create-payment-intent/`  
  Create a Stripe PaymentIntent for a product.  
  **Payload**: `{ "product_id": 1 }`

- **Stripe Webhook**:  
  `POST /api/stripe/webhook/`  
  Handle Stripe webhook events (e.g., payment success, failure).

---

### Admin (if applicable)
- **Django Admin Panel**:  
  `/admin/`  
  Access the Django admin interface for managing models and data.

---

### Pagination
- Most list endpoints support pagination. Use query parameters:  
  - `?page=1` for the first page.  
  - `?page_size=12` to specify the number of items per page.

---

### Notes
- All endpoints requiring authentication must include the `Authorization: Bearer <access_token>` header.
- Replace `{id}` with the actual ID of the resource you want to interact with.
- Ensure your `.env` file is configured correctly for Stripe, email, and database settings.
