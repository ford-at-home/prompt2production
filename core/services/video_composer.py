"""Video composition service that generates individual clips and composes final video."""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import List, Dict, Any
import json

try:
    import replicate
except ModuleNotFoundError:
    replicate = None


class VideoComposer:
    """Handles video generation and composition."""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.output_dir = Path(config.get("output_dir", "output"))
        self.clips_dir = self.output_dir / "clips"
        self.clips_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_clips(self, video_prompts: List[Dict[str, Any]]) -> List[str]:
        """Generate individual video clips for each scene."""
        if replicate is None:
            return self._generate_placeholder_clips(len(video_prompts))
            
        clip_paths = []
        
        for i, prompt_data in enumerate(video_prompts):
            print(f"Generating clip {i+1}/{len(video_prompts)}: {prompt_data['prompt'][:50]}...")
            
            try:
                # Use a more suitable model for short clips
                model_name = self.config.get("video_model", "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438")
                
                # Generate video with specific parameters for short clips
                output = replicate.run(
                    model_name,
                    input={
                        "prompt": prompt_data["prompt"],
                        "video_length": "14_frames_with_svd",
                        "fps": 6,
                        "motion_bucket_id": 127,
                        "cond_aug": 0.02,
                        "decoding_t": 7,
                        "seed": 42
                    }
                )
                
                # Download the video file
                clip_path = self.clips_dir / f"clip_{i:03d}.mp4"
                self._download_video(output, clip_path)
                clip_paths.append(str(clip_path))
                
                print(f"✓ Generated clip {i+1}: {clip_path}")
                
            except Exception as e:
                print(f"✗ Failed to generate clip {i+1}: {e}")
                # Create placeholder clip
                clip_path = self.clips_dir / f"clip_{i:03d}.mp4"
                self._create_placeholder_clip(clip_path)
                clip_paths.append(str(clip_path))
                
        return clip_paths
    
    def _download_video(self, video_url: str, output_path: Path) -> None:
        """Download video from URL to local path."""
        import requests
        
        response = requests.get(video_url)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            f.write(response.content)
    
    def _create_placeholder_clip(self, clip_path: Path) -> None:
        """Create a placeholder video clip."""
        # Create a simple colored video using ffmpeg
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", "color=c=blue:s=640x480:d=5",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(clip_path)
        ]
        
        try:
            subprocess.run(cmd, check=True, capture_output=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            # If ffmpeg fails, create an empty file
            clip_path.write_text("placeholder video")
    
    def _generate_placeholder_clips(self, num_clips: int) -> List[str]:
        """Generate placeholder clips when Replicate is not available."""
        clip_paths = []
        for i in range(num_clips):
            clip_path = self.clips_dir / f"clip_{i:03d}.mp4"
            self._create_placeholder_clip(clip_path)
            clip_paths.append(str(clip_path))
        return clip_paths
    
    def compose_final_video(self, clip_paths: List[str], audio_path: str, timing_data: List[Dict]) -> str:
        """Compose final video by stitching clips and adding audio."""
        final_video_path = self.output_dir / "final_video.mp4"
        
        if not clip_paths:
            self._create_placeholder_clip(final_video_path)
            return str(final_video_path)
        
        try:
            # Create a file list for ffmpeg
            with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                for clip_path in clip_paths:
                    f.write(f"file '{clip_path}'\n")
                file_list_path = f.name
            
            # Concatenate video clips
            temp_video = self.output_dir / "temp_concatenated.mp4"
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", file_list_path,
                "-c", "copy",
                str(temp_video)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Add audio overlay
            cmd = [
                "ffmpeg", "-y",
                "-i", str(temp_video),
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                "-shortest",
                str(final_video_path)
            ]
            
            subprocess.run(cmd, check=True, capture_output=True)
            
            # Clean up temporary files
            os.unlink(file_list_path)
            temp_video.unlink(missing_ok=True)
            
            print(f"✓ Composed final video: {final_video_path}")
            return str(final_video_path)
            
        except Exception as e:
            print(f"✗ Failed to compose video: {e}")
            self._create_placeholder_clip(final_video_path)
            return str(final_video_path)


def compose_video(video_prompts: List[Dict], audio_path: str, timing_data: List[Dict], config: Dict) -> str:
    """Main function to generate and compose video."""
    composer = VideoComposer(config)
    
    # Generate individual clips
    clip_paths = composer.generate_clips(video_prompts)
    
    # Compose final video
    final_video_path = composer.compose_final_video(clip_paths, audio_path, timing_data)
    
    return final_video_path 