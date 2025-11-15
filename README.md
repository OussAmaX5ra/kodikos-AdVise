# Facebook Marketing API Integration - FastAPI

A complete FastAPI backend implementing server-side OAuth integration with Facebook Marketing/Graph API, including insights ingestion and secure token storage.

## Features

- Server-side OAuth 2.0 flow with Facebook
- Long-lived token exchange and storage
- Insights ingestion with pagination and error handling
- JWT-based user authentication
- SQLite database with SQLAlchemy
- Placeholder page routes for frontend integration
- Docker support

## Prerequisites

- Python 3.11+
- Facebook App with Marketing API access
- Docker and Docker Compose (optional)

## Setup

### 1. Clone and Install
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` and set:

- `FB_APP_ID`: Your Facebook App ID
- `FB_APP_SECRET`: Your Facebook App Secret
- `FB_REDIRECT_URI`: Your OAuth callback URL (e.g., http://localhost:8000/facebook/oauth/callback)
- `SECRET_KEY`: Random secret for session security
- `JWT_SECRET_KEY`: Random secret for JWT tokens

### 3. Initialize Database
```bash
python -m app.seed
```

This creates a demo user:
- Email: `demo@example.com`
- Password: `demo123`

### 4. Run Application

**Local:**
```bash
uvicorn app.main:app --reload
```

**Docker:**
```bash
docker-compose -f docker-compose.dev.yml up --build
```

API available at: http://localhost:8000
API docs at: http://localhost:8000/docs
Adminer (DB tool) at: http://localhost:8080

## API Endpoints

### Public Pages (Placeholder Routes)

These routes return JSON structures for frontend integration:
```bash
# Landing page
curl http://localhost:8000/public/landing

# Login page
curl http://localhost:8000/public/login

# Signup page
curl http://localhost:8000/public/signup
```

### Authentication
```bash
# Register
curl -X POST http://localhost:8000/auth/register  -H "Content-Type: application/json" -d '{"email":"user@example.com","password":"securepass123"}'

# Login (get JWT token)
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo@example.com&password=demo123"
```

Save the `access_token` from response.

### Protected Page Routes

All protected routes require the JWT token in the Authorization header:
```bash
# Dashboard
curl -X GET http://localhost:8000/dashboard \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Reports & Analytics
curl -X GET http://localhost:8000/reports \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Upload CSV report (placeholder)
curl -X POST http://localhost:8000/reports/upload \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -F "file=@report.csv"

# Manage Accounts
curl -X GET http://localhost:8000/accounts/manage \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# AI Assistant
curl -X GET http://localhost:8000/ai \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# Ask AI Assistant
curl -X POST http://localhost:8000/ai/ask \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question":"How can I improve my ad campaign performance?"}'

# Campaigns
curl -X GET http://localhost:8000/campaigns \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Facebook OAuth Flow
```bash
# Get Facebook authorization URL
curl -X GET "http://localhost:8000/facebook/oauth/login?redirect_to=/dashboard" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Visit the returned URL in browser, authorize the app. Facebook redirects to callback with `code` parameter.

The callback endpoint automatically:
- Exchanges code for short-lived token
- Exchanges for long-lived token (60 days)
- Stores in database linked to your user

### Alternative: Insert System User Token (Testing)
```bash
curl -X POST http://localhost:8000/facebook/system_user/token \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "ad_account_id": "act_123456789",
    "access_token": "YOUR_SYSTEM_USER_TOKEN"
  }'
```

### Facebook Accounts Management
```bash
# List Connected Facebook Accounts
curl -X GET http://localhost:8000/facebook/accounts \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Fetch Insights from Facebook
```bash
curl -X POST "http://localhost:8000/facebook/act/act_123456789/fetch_insights?since=2024-01-01&until=2024-01-31&level=campaign" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Parameters:
- `since`: Start date (YYYY-MM-DD)
- `until`: End date (YYYY-MM-DD)
- `level`: account, campaign, adset, or ad

Response:
```json
{
  "rows_ingested": 150,
  "rows_skipped": 0,
  "next_cursor": null,
  "status": "success"
}
```

### Query Persisted Insights
```bash
curl -X GET "http://localhost:8000/facebook/act/act_123456789/insights_from_db?limit=10&page=1" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

Response includes computed metrics (CTR, ROAS):
```json
{
  "items": [
    {
      "id": 1,
      "ts": "2024-01-15",
      "level": "campaign",
      "entity_id": "123456",
      "impressions": 10000,
      "clicks": 250,
      "spend": 150.50,
      "conversions": 15,
      "revenue": 500.00,
      "ctr": 2.5,
      "roas": 3.32
    }
  ],
  "total": 150,
  "page": 1,
  "limit": 10
}
```

## Project Structure

```
.
├── app/
│   ├── main.py              # FastAPI app entry
│   ├── config.py            # Environment configuration
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth/
│   │   ├── router.py        # Auth endpoints
│   │   ├── dependencies.py  # JWT verification
│   │   └── utils.py         # Password hashing
│   ├── facebook/
│   │   ├── router.py        # Facebook endpoints
│   │   └── client.py        # Graph API client
│   ├── routes/
│   │   └── pages.py         # Placeholder page routes
│   └── seed.py              # Database seeding
├── tests/
│   ├── test_auth.py         # Authentication tests
│   └── test_facebook.py     # Facebook integration tests
├── data/                    # SQLite database (created on first run)
├── .env                     # Environment variables
├── requirements.txt
├── Dockerfile
├── docker-compose.dev.yml
└── README.md
```
## Page Routes Overview

The following placeholder routes are available for frontend development:

| Route | Method | Description | Auth Required |
|-------|--------|-------------|---------------|
| `/public/landing` | GET | Landing page data | No |
| `/public/login` | GET | Login page data | No |
| `/public/signup` | GET | Signup page data | No |
| `/dashboard` | GET | Dashboard summary | Yes |
| `/reports` | GET | Reports & analytics | Yes |
| `/reports/upload` | POST | Upload CSV report | Yes |
| `/accounts/manage` | GET | Manage accounts | Yes |
| `/ai` | GET | AI assistant status | Yes |
| `/ai/ask` | POST | Ask AI a question | Yes |
| `/campaigns` | GET | Campaigns list | Yes |

Note: These are placeholder routes that return minimal JSON structures. They are designed to be lightweight so frontend development can proceed while backend logic is implemented incrementally.

## Graph API Error Handling

The client implements:
- Automatic retry with exponential backoff for 429 (rate limit) and 5xx errors
- Maximum 3 retry attempts
- Pagination handling for large result sets
- Token expiration detection

## Security Notes

- Tokens stored in database (add encryption in production via `cryptography` library)
- JWT tokens for API authentication
- Password hashing with bcrypt
- Environment-based secrets (never commit `.env`)

## Facebook App Setup

1. Create app at https://developers.facebook.com
2. Add "Facebook Login" product
3. Configure Valid OAuth Redirect URIs: `http://localhost:8000/facebook/oauth/callback`
4. Request permissions: `ads_read`, `ads_management`, `business_management`
5. Note App ID and App Secret

## Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests
pytest

# Run with coverage
pytest --cov=app tests/
```

## Development Workflow

1. **Start the server**
```bash
   make dev
   # or
   uvicorn app.main:app --reload
```

2. **Access API documentation**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

3. **Test endpoints**
   - Use the examples above
   - Use the interactive API docs
   - Use Postman or similar tools

## Troubleshooting

**Token Expired:**
Re-run OAuth flow to get fresh 60-day token.

**Permissions Error:**
Ensure Facebook app has Marketing API access and required permissions granted during OAuth.

**Database Locked:**
Only one writer at a time with SQLite. For production, use PostgreSQL.

**CORS Issues:**
Update `allow_origins` in `app/main.py` to match your frontend URL in production.

## Production Deployment

### Environment Variables

Ensure all environment variables are set properly:
```bash
APP_ENV=production
DATABASE_URL=postgresql://user:pass@host:5432/dbname
SECRET_KEY=<strong-random-secret>
JWT_SECRET_KEY=<strong-random-secret>
FB_APP_ID=<your-facebook-app-id>
FB_APP_SECRET=<your-facebook-app-secret>
FB_REDIRECT_URI=https://yourdomain.com/facebook/oauth/callback
```

### Recommended Production Setup

1. **Use PostgreSQL instead of SQLite**
```bash
   pip install psycopg2-binary
   # Update DATABASE_URL in .env
```

2. **Enable HTTPS**
   - Use a reverse proxy (nginx, Caddy)
   - Configure SSL certificates

3. **Add token encryption**
   - Use `cryptography.fernet` to encrypt access tokens
   - Store encryption key securely

4. **Rate limiting**
   - Implement rate limiting middleware
   - Use Redis for distributed rate limiting

5. **Monitoring and logging**
   - Add logging middleware
   - Use Sentry or similar for error tracking
   - Monitor API usage and performance
