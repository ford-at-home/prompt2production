"""Deployment helper for uploading assets to S3."""

from core.utils.config import config as global_config


def deploy(path: str, config: dict) -> None:
    """Pretend to deploy an artifact to S3."""
    bucket = config.get("deployment", {}).get("s3_bucket", global_config.get("api.s3.default_bucket", "demo"))
    print(f"Uploading {path} to s3://{bucket}/")

