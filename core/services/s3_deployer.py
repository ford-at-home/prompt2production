"""Deployment helper for uploading assets to S3."""

import os
from pathlib import Path
from typing import Optional
from core.utils.config import config as global_config
from core.utils.logger import setup_logger, log_api_call

try:
    import boto3
    from botocore.exceptions import BotoCore3Error, NoCredentialsError
    has_boto3 = True
except ImportError:
    has_boto3 = False
    BotoCore3Error = Exception
    NoCredentialsError = Exception


def deploy(path: str, config: dict) -> Optional[str]:
    """Deploy an artifact to S3.
    
    Args:
        path: Local file path to upload
        config: Project configuration
        
    Returns:
        S3 URL if successful, None otherwise
    """
    logger = setup_logger(__name__)
    
    # Check if we're in development mode or boto3 not available
    if global_config.get('development.use_stubs', True) or not has_boto3:
        bucket = config.get("deployment", {}).get("s3_bucket", global_config.get("api.s3.default_bucket", "demo"))
        print(f"Uploading {path} to s3://{bucket}/")
        log_api_call(logger, "S3", "upload (stub)", 
                    {"path": path, "bucket": bucket}, stub_mode=True)
        return f"s3://{bucket}/{Path(path).name}"
    
    # Get S3 configuration
    bucket = config.get("deployment", {}).get("s3_bucket", global_config.get("api.s3.default_bucket"))
    region = config.get("deployment", {}).get("s3_region", global_config.get("api.s3.region", "us-east-1"))
    profile = global_config.get("api.bedrock.profile", "personal")  # Use same AWS profile
    
    if not bucket:
        logger.error("S3 bucket not configured")
        return None
    
    file_path = Path(path)
    if not file_path.exists():
        logger.error(f"File not found: {path}")
        return None
    
    try:
        # Create S3 client with profile
        session = boto3.Session(profile_name=profile)
        s3_client = session.client('s3', region_name=region)
        
        # Generate S3 key
        project_name = config.get('project_name', 'default')
        s3_key = f"{project_name}/{file_path.name}"
        
        # Log API call
        log_api_call(logger, "S3", "upload", 
                    {"bucket": bucket, "key": s3_key, "size": file_path.stat().st_size}, 
                    stub_mode=False)
        
        # Upload file
        logger.info(f"Uploading {file_path.name} to s3://{bucket}/{s3_key}")
        
        # Determine content type
        content_type = "application/octet-stream"
        if file_path.suffix == ".mp4":
            content_type = "video/mp4"
        elif file_path.suffix == ".mp3":
            content_type = "audio/mpeg"
        elif file_path.suffix == ".html":
            content_type = "text/html"
        elif file_path.suffix == ".json":
            content_type = "application/json"
        elif file_path.suffix in [".txt", ".md"]:
            content_type = "text/plain"
        
        s3_client.upload_file(
            str(file_path),
            bucket,
            s3_key,
            ExtraArgs={
                'ContentType': content_type,
                'ACL': 'public-read'  # Make publicly accessible
            }
        )
        
        # Generate public URL
        s3_url = f"https://{bucket}.s3.{region}.amazonaws.com/{s3_key}"
        logger.info(f"Successfully uploaded to: {s3_url}")
        
        return s3_url
        
    except NoCredentialsError:
        logger.error("AWS credentials not found. Please configure AWS credentials.")
        return None
    except BotoCore3Error as e:
        logger.error(f"S3 upload error: {type(e).__name__}: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during S3 upload: {type(e).__name__}: {str(e)}")
        return None

