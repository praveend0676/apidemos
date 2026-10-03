import os
import secrets

from dotenv import load_dotenv
from fastapi import Header, HTTPException, status


load_dotenv()


DEFAULT_API_KEY = "super30-secret-key"

API_KEY: str = os.getenv("API_KEY") or DEFAULT_API_KEY


def verify_api_key(
    x_api_key: str | None = Header(default=None)
) -> str:
    if x_api_key is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key is missing",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    if not secrets.compare_digest(x_api_key, API_KEY):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )

    return x_api_key