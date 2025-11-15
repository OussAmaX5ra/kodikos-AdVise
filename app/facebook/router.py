import json
from datetime import datetime, date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import User, FacebookAccount, MetricSnapshot
from app.schemas import (
    FacebookAccountResponse,
    SystemUserTokenRequest,
    FetchInsightsResponse,
    MetricSnapshotListResponse,
    MetricSnapshotResponse,
)
from app.auth.dependencies import get_current_user
from app.facebook.client import FacebookGraphAPIClient
from app.config import settings

router = APIRouter()
fb_client = FacebookGraphAPIClient()


@router.get("/oauth/login")
def facebook_oauth_login(
    redirect_to: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
):
    """
    Generate Facebook OAuth authorization URL.
    User should visit this URL to authorize the app.
    """
    # Build state parameter (optional: encode user_id + redirect_to)
    state = f"user_{current_user.id}"
    if redirect_to:
        state += f"|redirect_{redirect_to}"

    auth_url = (
        f"https://www.facebook.com/{settings.FB_API_VERSION}/dialog/oauth?"
        f"client_id={settings.FB_APP_ID}"
        f"&redirect_uri={settings.FB_REDIRECT_URI}"
        f"&state={state}"
        f"&scope=ads_read,ads_management,business_management"
    )

    return {"authorization_url": auth_url, "message": "Visit this URL to authorize"}


@router.get("/oauth/callback", response_class=HTMLResponse)
def facebook_oauth_callback(
    code: Optional[str] = Query(None),
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_reason: Optional[str] = Query(None),
    error_description: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """
    OAuth callback endpoint. Facebook redirects here after user authorization.
    Exchanges code for token, then extends to long-lived token, then stores in DB.
    """
    # Handle errors
    if error:
        return f"""
        <html>
            <body>
                <h2>Authorization Failed</h2>
                <p><strong>Error:</strong> {error}</p>
                <p><strong>Reason:</strong> {error_reason}</p>
                <p><strong>Description:</strong> {error_description}</p>
            </body>
        </html>
        """

    # Validate required parameters
    if not code:
        return """
        <html>
            <body>
                <h2>Authorization Failed</h2>
                <p>No authorization code received.</p>
            </body>
        </html>
        """

    try:
        # Parse state to get user_id
        user_id = None
        redirect_path = "/dashboard"
        if state:
            parts = state.split("|")
            for part in parts:
                if part.startswith("user_"):
                    user_id = int(part.replace("user_", ""))
                elif part.startswith("redirect_"):
                    redirect_path = part.replace("redirect_", "")

        if not user_id:
            return """
            <html>
                <body>
                    <h2>Authorization Failed</h2>
                    <p>Invalid state parameter - could not identify user.</p>
                </body>
            </html>
            """

        # Verify user exists
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return """
            <html>
                <body>
                    <h2>Authorization Failed</h2>
                    <p>User not found.</p>
                </body>
            </html>
            """

        # Step 1: Exchange code for short-lived token
        token_data = fb_client.exchange_code_for_token(code, settings.FB_REDIRECT_URI)
        short_lived_token = token_data.get("access_token")

        if not short_lived_token:
            return f"""
            <html>
                <body>
                    <h2>Token Exchange Failed</h2>
                    <p>Could not retrieve access token from Facebook.</p>
                    <p>Response: {json.dumps(token_data)}</p>
                </body>
            </html>
            """

        # Step 2: Exchange for long-lived token
        extended_data = fb_client.extend_token(short_lived_token)
        long_lived_token = extended_data.get("access_token")
        expires_at = extended_data.get("expires_at")

        # Step 3: Get ad accounts for this token
        # Make a Graph API call to get ad accounts
        accounts_url = f"{settings.FB_GRAPH_BASE_URL}/me/adaccounts"
        params = {"access_token": long_lived_token, "fields": "id,name,account_id"}
        response = fb_client._request_with_retry("GET", accounts_url, params=params)
        accounts_data = response.json()

        ad_accounts = accounts_data.get("data", [])

        if not ad_accounts:
            return """
            <html>
                <body>
                    <h2>No Ad Accounts Found</h2>
                    <p>Your Facebook account has no ad accounts associated with it.</p>
                    <p>Please create an ad account in Facebook Business Manager first.</p>
                </body>
            </html>
            """

        # Step 4: Store token for each ad account
        stored_accounts = []
        for account in ad_accounts:
            ad_account_id = account.get("id")  # Format: act_123456789

            # Check if account already exists for this user
            existing = (
                db.query(FacebookAccount)
                .filter(
                    FacebookAccount.user_id == user_id,
                    FacebookAccount.ad_account_id == ad_account_id,
                )
                .first()
            )

            if existing:
                # Update existing token
                existing.access_token = long_lived_token
                existing.expires_at = expires_at
                existing.updated_at = datetime.utcnow()
                stored_accounts.append(ad_account_id)
            else:
                # Create new record
                fb_account = FacebookAccount(
                    user_id=user_id,
                    ad_account_id=ad_account_id,
                    access_token=long_lived_token,
                    token_type="Bearer",
                    expires_at=expires_at,
                    is_system_user=False,
                )
                db.add(fb_account)
                stored_accounts.append(ad_account_id)

        db.commit()

        accounts_html = "<ul>" + "".join([f"<li>{acc}</li>" for acc in stored_accounts]) + "</ul>"

        return f"""
        <html>
            <body>
                <h2>Authorization Successful!</h2>
                <p>Your Facebook ad accounts have been connected:</p>
                {accounts_html}
                <p>Token expires: {expires_at.strftime('%Y-%m-%d %H:%M:%S UTC') if expires_at else 'Never'}</p>
                <p>You can now close this window and return to the application.</p>
            </body>
        </html>
        """

    except Exception as e:
        db.rollback()
        return f"""
        <html>
            <body>
                <h2>Authorization Failed</h2>
                <p>An error occurred during authorization:</p>
                <p><strong>{str(e)}</strong></p>
            </body>
        </html>
        """


@router.post("/system_user/token", response_model=FacebookAccountResponse, status_code=status.HTTP_201_CREATED)
def insert_system_user_token(
    token_data: SystemUserTokenRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Insert a system user token manually (for testing/development).
    System user tokens don't expire.
    """
    # Check if account already exists for this user
    existing = (
        db.query(FacebookAccount)
        .filter(
            FacebookAccount.user_id == current_user.id,
            FacebookAccount.ad_account_id == token_data.ad_account_id,
        )
        .first()
    )

    if existing:
        # Update existing
        existing.access_token = token_data.access_token
        existing.is_system_user = True
        existing.expires_at = None  # System user tokens don't expire
        existing.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        return existing

    # Create new
    fb_account = FacebookAccount(
        user_id=current_user.id,
        ad_account_id=token_data.ad_account_id,
        access_token=token_data.access_token,
        token_type="Bearer",
        expires_at=None,
        is_system_user=True,
    )
    db.add(fb_account)
    db.commit()
    db.refresh(fb_account)
    return fb_account


@router.get("/accounts", response_model=list[FacebookAccountResponse])
def list_facebook_accounts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List all connected Facebook ad accounts for the current user."""
    accounts = db.query(FacebookAccount).filter(FacebookAccount.user_id == current_user.id).all()
    return accounts


@router.post("/act/{ad_account_id}/fetch_insights", response_model=FetchInsightsResponse)
def fetch_insights(
    ad_account_id: str,
    since: str = Query(..., description="Start date (YYYY-MM-DD)"),
    until: str = Query(..., description="End date (YYYY-MM-DD)"),
    level: str = Query("campaign", description="account, campaign, adset, or ad"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Fetch insights from Facebook Graph API and persist to database.
    Handles pagination automatically.
    """
    # Validate level
    if level not in ["account", "campaign", "adset", "ad"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid level parameter")

    # Validate dates
    try:
        since_date = datetime.strptime(since, "%Y-%m-%d").date()
        until_date = datetime.strptime(until, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format. Use YYYY-MM-DD")

    # Get Facebook account
    fb_account = (
        db.query(FacebookAccount)
        .filter(
            FacebookAccount.user_id == current_user.id,
            FacebookAccount.ad_account_id == ad_account_id,
        )
        .first()
    )

    if not fb_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Facebook account {ad_account_id} not found or not connected to your user",
        )

    # Check token expiration
    if fb_account.expires_at and fb_account.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token expired. Please re-authorize the app.",
        )

    # Define fields to fetch
    fields = [
        "date_start",
        "date_stop",
        "impressions",
        "clicks",
        "spend",
        "actions",  # Contains conversions
        "action_values",  # Contains revenue
    ]

    # Add level-specific ID field
    if level == "campaign":
        fields.append("campaign_id")
        fields.append("campaign_name")
    elif level == "adset":
        fields.append("adset_id")
        fields.append("adset_name")
    elif level == "ad":
        fields.append("ad_id")
        fields.append("ad_name")
    elif level == "account":
        fields.append("account_id")

    try:
        # Fetch all pages of insights
        all_insights = fb_client.get_all_insights_pages(
            ad_account_id=ad_account_id,
            since=since,
            until=until,
            level=level,
            fields=fields,
            access_token=fb_account.access_token,
        )

        rows_ingested = 0
        rows_skipped = 0

        for insight in all_insights:
            # Extract data
            date_start = insight.get("date_start")
            if not date_start:
                rows_skipped += 1
                continue

            ts = datetime.strptime(date_start, "%Y-%m-%d").date()

            # Determine entity_id based on level
            if level == "campaign":
                entity_id = insight.get("campaign_id", "unknown")
            elif level == "adset":
                entity_id = insight.get("adset_id", "unknown")
            elif level == "ad":
                entity_id = insight.get("ad_id", "unknown")
            elif level == "account":
                entity_id = insight.get("account_id", ad_account_id)
            else:
                entity_id = "unknown"

            impressions = int(insight.get("impressions", 0))
            clicks = int(insight.get("clicks", 0))
            spend = float(insight.get("spend", 0.0))

            # Extract conversions from actions array
            conversions = 0
            actions = insight.get("actions", [])
            for action in actions:
                if action.get("action_type") in ["purchase", "offsite_conversion.fb_pixel_purchase"]:
                    conversions += int(action.get("value", 0))

            # Extract revenue from action_values array
            revenue = 0.0
            action_values = insight.get("action_values", [])
            for action_value in action_values:
                if action_value.get("action_type") in ["purchase", "offsite_conversion.fb_pixel_purchase"]:
                    revenue += float(action_value.get("value", 0.0))

            # Store raw JSON
            raw_json = json.dumps(insight)

            # Create or update metric snapshot
            try:
                metric = MetricSnapshot(
                    facebook_account_id=fb_account.id,
                    ts=ts,
                    level=level,
                    entity_id=entity_id,
                    impressions=impressions,
                    clicks=clicks,
                    spend=spend,
                    conversions=conversions,
                    revenue=revenue,
                    raw=raw_json,
                )
                db.add(metric)
                db.commit()
                rows_ingested += 1
            except IntegrityError:
                # Duplicate entry - skip
                db.rollback()
                rows_skipped += 1
                continue

        return FetchInsightsResponse(
            rows_ingested=rows_ingested,
            rows_skipped=rows_skipped,
            next_cursor=None,
            status="success",
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch insights: {str(e)}",
        )


@router.get("/act/{ad_account_id}/insights_from_db", response_model=MetricSnapshotListResponse)
def get_insights_from_db(
    ad_account_id: str,
    limit: int = Query(50, ge=1, le=1000),
    page: int = Query(1, ge=1),
    level: Optional[str] = Query(None, description="Filter by level: account, campaign, adset, ad"),
    since: Optional[str] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    until: Optional[str] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Retrieve persisted insights from database with pagination.
    Computed metrics (CTR, ROAS) are calculated in the response.
    """
    # Get Facebook account
    fb_account = (
        db.query(FacebookAccount)
        .filter(
            FacebookAccount.user_id == current_user.id,
            FacebookAccount.ad_account_id == ad_account_id,
        )
        .first()
    )

    if not fb_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Facebook account {ad_account_id} not found or not connected to your user",
        )

    # Build query
    query = db.query(MetricSnapshot).filter(MetricSnapshot.facebook_account_id == fb_account.id)

    # Apply filters
    if level:
        query = query.filter(MetricSnapshot.level == level)

    if since:
        try:
            since_date = datetime.strptime(since, "%Y-%m-%d").date()
            query = query.filter(MetricSnapshot.ts >= since_date)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid since date format")

    if until:
        try:
            until_date = datetime.strptime(until, "%Y-%m-%d").date()
            query = query.filter(MetricSnapshot.ts <= until_date)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid until date format")

    # Get total count
    total = query.count()

    # Paginate
    offset = (page - 1) * limit
    metrics = query.order_by(MetricSnapshot.ts.desc()).offset(offset).limit(limit).all()

    # Convert to response with computed fields
    items = [MetricSnapshotResponse.from_orm_with_computed(metric) for metric in metrics]

    return MetricSnapshotListResponse(items=items, total=total, page=page, limit=limit)