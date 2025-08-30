# AuctionCraft - Django REST API (Skeleton)

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

## Stripe integration
- Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET` in your `.env` file.
- Use the `api/payments/create-payment-intent/` endpoint to create a PaymentIntent from the frontend.
- Configure Stripe CLI or dashboard to forward webhooks to `/api/stripe/webhook/` and set the webhook secret in `.env`.

## Notes & next steps
- This is a backend skeleton. Replace or extend model fields, add permissions, validation, tests, and admin customizations as needed.
- For production, switch to PostgreSQL, secure secret keys, and configure CORS for your React frontend.

## OTP Authentication
- Request OTP: `POST /api/auth/otp/request/` with `{ "email": "user@example.com" }`.
- Verify OTP: `POST /api/auth/otp/verify/` with `{ "email": "user@example.com", "code": "123456" }`.
- On verify, server returns JWT `access` and `refresh` tokens.
- By default emails are printed to console because `EMAIL_BACKEND` defaults to console backend. Configure SMTP in `.env` to send real emails.

## Auction close notifications
- Sellers (or staff) can manually close an auction:
  - `POST /api/products/{id}/close_auction/`
- When closed the system:
  - Marks the auction inactive and sets `end_time` to now.
  - Determines the highest bid winner.
  - Creates `Notification` records for every bidder and sends an email (best-effort).
  - You can view notifications via `GET /api/auth/notifications/` (JWT required).
