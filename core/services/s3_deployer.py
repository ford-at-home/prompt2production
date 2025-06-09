"""Deployment helper for uploading assets to S3."""


def deploy(path: str, config: dict) -> None:
    """Pretend to deploy an artifact to S3."""

    bucket = config.get("deployment", {}).get("s3_bucket", "demo")
    print(f"Uploading {path} to s3://{bucket}/")

