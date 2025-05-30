import json
import pathlib

import requests
import os
from datetime import datetime, timedelta


class TCGPlayerSession:
    def __init__(self, public_key, private_key, environment="production"):
        self.public_key = public_key
        self.private_key = private_key
        self.environment = environment  # "production" or "sandbox"
        self.access_token = None
        self.refresh_token = None
        self.token_expiry = None
        self.base_url = self._get_base_url()

    def _get_base_url(self):
        if self.environment == "production":
            return "https://api.tcgplayer.com"
        elif self.environment == "sandbox":
            return "https://api.sandbox.tcgplayer.com"  # Sandbox URL
        else:
            raise ValueError("Invalid environment. Must be 'production' or 'sandbox'.")

    def _get_auth_headers(self):
        return {"Accept": "application/json", "Content-Type": "application/json"}

    def _authenticate(self):
        url = f"{self.base_url}/token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.public_key,
            "client_secret": self.private_key,
        }
        try:
            response = requests.post(
                url, data=payload, headers=self._get_auth_headers()
            )
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

            auth_data = response.json()
            self.access_token = auth_data["access_token"]
            self.refresh_token = auth_data.get(
                "refresh_token"
            )  # Refresh token is not always provided
            expires_in = auth_data["expires_in"]
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            return True

        except requests.exceptions.RequestException as e:
            print(f"Authentication failed: {e}")
            return False  # Or raise the exception if you prefer

    def _refresh_token(self):
        if not self.refresh_token:
            print("Refresh token is not available. Re-authentication is required.")
            return False

        url = f"{self.base_url}/token"
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": self.public_key,
            "client_secret": self.private_key,
        }

        try:
            response = requests.post(
                url, data=payload, headers=self._get_auth_headers()
            )
            response.raise_for_status()

            auth_data = response.json()
            self.access_token = auth_data["access_token"]
            expires_in = auth_data["expires_in"]
            self.token_expiry = datetime.now() + timedelta(seconds=expires_in)
            self.refresh_token = auth_data.get(
                "refresh_token"
            )  # Refresh token might be updated.
            return True

        except requests.exceptions.RequestException as e:
            print(f"Token refresh failed: {e}")
            return False

    def _ensure_token(self):
        if self.access_token and self.token_expiry > datetime.now() + timedelta(
            minutes=5
        ):  # Check token validity with a 5-minute buffer
            return  # Token is valid, no need to do anything

        if self.refresh_token and self._refresh_token():
            return  # Token refreshed successfully

        if self._authenticate():
            return  # Authenticated successfully

        raise Exception(
            "Failed to obtain a valid access token."
        )  # Raise exception if both auth and refresh fail.

    def get(self, endpoint, params=None):  # Example method for making GET requests
        self._ensure_token()
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    # Add other API interaction methods (POST, PUT, DELETE, etc.) as needed.


# Example Usage (replace with your actual keys):
print(pathlib.Path("credentials.json").resolve().exists())
with open("credentials.json", mode="r") as credentials_file:
    credentials_dict = json.load(credentials_file)

public_key = credentials_dict.get(
    "public_key"
)  # os.environ.get("TCGPLAYER_PUBLIC_KEY")
private_key = credentials_dict.get(
    "private_key"
)  # os.environ.get("TCGPLAYER_PRIVATE_KEY")

if not public_key or not private_key:
    raise ValueError(
        "TCGPLAYER_PUBLIC_KEY and TCGPLAYER_PRIVATE_KEY environment variables must be set."
    )

try:
    tcgplayer = TCGPlayerSession(
        public_key, private_key, environment="production"
    )  # Or "sandbox"

    # Example: Get categories (replace with the actual endpoint you need)
    categories = tcgplayer.get("/catalog/categories")
    if categories:
        print(categories)

    # Example: Get products (replace with the actual endpoint and parameters)
    products = tcgplayer.get(
        "/catalog/products", params={"categoryId": 3}
    )  # Example category ID
    if products:
        print(products)

except Exception as e:
    print(f"An error occurred: {e}")
