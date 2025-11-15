import time
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from app.config import settings


class FacebookGraphAPIClient:
    """Client for interacting with Facebook Graph API."""

    BASE_URL = settings.FB_GRAPH_BASE_URL

    def __init__(self):
        self.app_id = settings.FB_APP_ID
        self.app_secret = settings.FB_APP_SECRET

    def _request_with_retry(
        self, method: str, url: str, max_retries: int = 3, backoff_factor: float = 2.0, **kwargs
    ) -> requests.Response:
        """Make HTTP request with retry logic for transient errors."""
        for attempt in range(max_retries):
            try:
                response = requests.request(method, url, timeout=30, **kwargs)

                # Check for rate limit (429) or server errors (5xx)
                if response.status_code == 429 or response.status_code >= 500:
                    if attempt < max_retries - 1:
                        wait_time = backoff_factor ** attempt
                        time.sleep(wait_time)
                        continue
                    else:
                        response.raise_for_status()

                response.raise_for_status()
                return response

            except requests.exceptions.RequestException as e:
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    time.sleep(wait_time)
                else:
                    raise e

        raise Exception("Max retries exceeded")

    def exchange_code_for_token(self, code: str, redirect_uri: str) -> Dict[str, Any]:
        """Exchange authorization code for short-lived access token."""
        url = f"{self.BASE_URL}/oauth/access_token"
        params = {
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "redirect_uri": redirect_uri,
            "code": code,
        }

        response = self._request_with_retry("GET", url, params=params)
        return response.json()

    def extend_token(self, short_lived_token: str) -> Dict[str, Any]:
        """Exchange short-lived token for long-lived token (60 days)."""
        url = f"{self.BASE_URL}/oauth/access_token"
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": self.app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": short_lived_token,
        }

        response = self._request_with_retry("GET", url, params=params)
        data = response.json()

        # Calculate expires_at (default 60 days for long-lived tokens)
        expires_in = data.get("expires_in", 60 * 24 * 60 * 60)  # Default 60 days
        expires_at = datetime.utcnow() + timedelta(seconds=expires_in)
        data["expires_at"] = expires_at

        return data

    def get_insights(
        self,
        ad_account_id: str,
        since: str,
        until: str,
        level: str,
        fields: List[str],
        access_token: str,
        after_cursor: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetch insights from Facebook Marketing API.

        Args:
            ad_account_id: Ad account ID (e.g., act_123456789)
            since: Start date (YYYY-MM-DD)
            until: End date (YYYY-MM-DD)
            level: account, campaign, adset, or ad
            fields: List of fields to retrieve
            access_token: User or system user access token
            after_cursor: Pagination cursor

        Returns:
            Dict containing 'data' list and 'paging' info
        """
        url = f"{self.BASE_URL}/{ad_account_id}/insights"
        params = {
            "access_token": access_token,
            "level": level,
            "time_range": f'{{"since":"{since}","until":"{until}"}}',
            "fields": ",".join(fields),
            "limit": 100,  # Max per page
        }

        if after_cursor:
            params["after"] = after_cursor

        response = self._request_with_retry("GET", url, params=params)
        return response.json()

    def get_all_insights_pages(
        self,
        ad_account_id: str,
        since: str,
        until: str,
        level: str,
        fields: List[str],
        access_token: str,
    ) -> List[Dict[str, Any]]:
        """
        Fetch all pages of insights data.

        Returns:
            List of all insight records across all pages
        """
        all_data = []
        after_cursor = None

        while True:
            result = self.get_insights(
                ad_account_id=ad_account_id,
                since=since,
                until=until,
                level=level,
                fields=fields,
                access_token=access_token,
                after_cursor=after_cursor,
            )

            data = result.get("data", [])
            all_data.extend(data)

            # Check for next page
            paging = result.get("paging", {})
            cursors = paging.get("cursors", {})
            after_cursor = cursors.get("after")

            if not after_cursor:
                break  # No more pages

        return all_data