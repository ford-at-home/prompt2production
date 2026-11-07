"""Bedrock Nova LLM wrapper for text generation."""

from core.utils.config import config as global_config
from core.utils.logger import setup_logger, log_api_call
from pathlib import Path

try:
    import boto3
    has_boto3 = True
except ImportError:
    has_boto3 = False


def run_prompt(prompt: str) -> str:
    """Run a prompt through Bedrock and return the result.
    
    This is a compatibility wrapper for the existing codebase.
    """
    return bedrock_complete(prompt, {})


def bedrock_complete(prompt: str, config: dict) -> str:
    """Complete a prompt using the configured Bedrock model."""
    logger = setup_logger(__name__)
    
    # Check if we're in development mode with stubs
    use_stubs = global_config.get('development.use_stubs', True) or not has_boto3
    
    if use_stubs:
        # Log stub API call
        log_api_call(logger, "Bedrock", "generate (stub)", 
                    {"prompt_length": len(prompt), "model": "stub"}, 
                    stub_mode=True)
        
        # Check for specific development mode handling
        placeholder = global_config.get('placeholders.llm_output', '[LLM output for: {prompt}...]')
        response = placeholder.format(prompt=prompt[:50])
        
        # Save prompt for debugging
        if global_config.get('development.save_prompts', True):
            prompt_dir = Path(global_config.get('development.prompt_directory', 'debug/prompts'))
            prompt_dir.mkdir(parents=True, exist_ok=True)
            
            import time
            timestamp = int(time.time() * 1000)
            prompt_file = prompt_dir / f"bedrock_prompt_{timestamp}.txt"
            prompt_file.write_text(prompt)
            logger.debug(f"Saved prompt to: {prompt_file}")
        
        # Add artificial delay if configured
        import time
        delay = global_config.get('development.stub_delay', 0.5)
        if delay > 0:
            time.sleep(delay)
        
        return response
    
    # Real Bedrock API call
    import boto3
    
    # Get model from config
    model_id = config.get('bedrock_model', global_config.get('api.bedrock.model', 'anthropic.claude-3-haiku-20240307-v1:0'))
    
    # Create Bedrock client with profile
    profile = config.get('aws_profile', global_config.get('api.bedrock.profile', 'personal'))
    region = config.get('aws_region', global_config.get('api.bedrock.region', 'us-east-1'))
    
    # Log API call
    log_api_call(logger, "Bedrock", "generate", 
                {"model": model_id, "profile": profile, "region": region, 
                 "prompt_length": len(prompt)}, 
                stub_mode=False)
    
    try:
        session = boto3.Session(profile_name=profile)
        bedrock = session.client('bedrock-runtime', region_name=region)
        
        # Prepare request based on model type
        if 'anthropic' in model_id and 'claude-3' in model_id:
            # Claude 3 models use Messages API
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
        elif 'anthropic' in model_id:
            # Claude 2 models
            request_body = {
                "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
                "max_tokens_to_sample": 4000,
                "temperature": 0.7,
                "top_p": 0.9,
            }
        else:
            # Generic format
            request_body = {
                "prompt": prompt,
                "max_tokens": 4000,
                "temperature": 0.7,
            }
        
        # Call Bedrock
        import json
        response = bedrock.invoke_model(
            modelId=model_id,
            body=json.dumps(request_body),
            contentType='application/json',
            accept='application/json'
        )
        
        # Extract text from response
        response_body = json.loads(response['body'].read())
        
        # Handle different model response formats
        if 'content' in response_body:
            if isinstance(response_body['content'], list):
                # Claude 3 Messages API format
                result = response_body['content'][0]['text']
            elif isinstance(response_body['content'], str):
                # Alternative format
                result = response_body['content']
            else:
                result = str(response_body['content'])
        elif 'completion' in response_body:
            # Claude 2 format
            result = response_body['completion']
        else:
            # Fallback
            result = str(response_body)
        
        logger.debug(f"Bedrock response length: {len(result)} characters")
        return result
    
    except Exception as e:
        logger.error(f"Error calling Bedrock: {type(e).__name__}: {str(e)}")
        # Fallback to placeholder
        placeholder = global_config.get('placeholders.llm_output', '[LLM output for: {prompt}...]')
        return placeholder.format(prompt=prompt[:50])