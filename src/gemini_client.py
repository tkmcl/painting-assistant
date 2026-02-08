"""
Gemini API client for image generation using gemini-3-pro-image-preview.
"""

import os
import base64
import json
import requests
from pathlib import Path
from typing import Optional


class GeminiImageClient:
    """Client for Gemini 3 Pro Image Preview API."""

    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-pro-image-preview:generateContent"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment or provided")
        # Clean up any corrupted env values (e.g., "export" appended)
        self.api_key = self.api_key.replace("export", "").strip()

    def _image_to_base64(self, image_path: str) -> tuple[str, str]:
        """Convert image file to base64 and determine mime type."""
        path = Path(image_path)
        suffix = path.suffix.lower()

        mime_types = {
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".png": "image/png",
            ".webp": "image/webp",
            ".gif": "image/gif",
        }

        mime_type = mime_types.get(suffix, "image/jpeg")

        with open(path, "rb") as f:
            data = base64.standard_b64encode(f.read()).decode("utf-8")

        return data, mime_type

    def _save_response_image(self, response_data: dict, output_path: str) -> Optional[str]:
        """Extract and save image from API response."""
        try:
            candidates = response_data.get("candidates", [])
            if not candidates:
                return None

            parts = candidates[0].get("content", {}).get("parts", [])

            for part in parts:
                # Handle both camelCase (API response) and snake_case formats
                inline_data = part.get("inlineData") or part.get("inline_data")
                if inline_data:
                    image_data = base64.standard_b64decode(inline_data["data"])

                    with open(output_path, "wb") as f:
                        f.write(image_data)

                    return output_path

            return None
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    def _extract_text_response(self, response_data: dict) -> Optional[str]:
        """Extract text from API response."""
        try:
            candidates = response_data.get("candidates", [])
            if not candidates:
                return None

            parts = candidates[0].get("content", {}).get("parts", [])

            text_parts = []
            for part in parts:
                if "text" in part:
                    text_parts.append(part["text"])

            return "\n".join(text_parts) if text_parts else None
        except Exception:
            return None

    def _extract_thought_signature(self, response_data: dict) -> Optional[str]:
        """Extract thought signature for multi-turn editing."""
        try:
            candidates = response_data.get("candidates", [])
            if not candidates:
                return None
            return candidates[0].get("thoughtSignature")
        except Exception:
            return None

    def generate_image(
        self,
        prompt: str,
        reference_image_path: Optional[str] = None,
        output_path: str = "output.png",
        aspect_ratio: str = "4:5",  # Matches 80x100cm canvas (landscape)
        image_size: str = "2K",
        previous_thought_signature: Optional[str] = None,
    ) -> dict:
        """
        Generate an image using Gemini 3 Pro Image Preview.

        Args:
            prompt: Text prompt describing the desired image
            reference_image_path: Optional path to reference image
            output_path: Where to save the generated image
            aspect_ratio: Aspect ratio (e.g., "3:4", "1:1", "16:9")
            image_size: Resolution ("1K", "2K", "4K")
            previous_thought_signature: For multi-turn editing continuity

        Returns:
            dict with keys: success, image_path, text_response, thought_signature, error
        """
        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        # Build parts
        parts = []

        # Add reference image if provided
        if reference_image_path:
            img_data, mime_type = self._image_to_base64(reference_image_path)
            parts.append({
                "inline_data": {
                    "mime_type": mime_type,
                    "data": img_data
                }
            })

        # Add text prompt
        parts.append({"text": prompt})

        # Build request body
        body = {
            "contents": [{
                "role": "user",
                "parts": parts
            }],
            "generationConfig": {
                "responseModalities": ["TEXT", "IMAGE"],
                "imageConfig": {
                    "aspectRatio": aspect_ratio,
                    "imageSize": image_size
                }
            }
        }

        # Add thought signature for multi-turn editing
        if previous_thought_signature:
            body["contents"][0]["thoughtSignature"] = previous_thought_signature

        try:
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=body,
                timeout=120  # Image generation can take a while
            )

            if response.status_code != 200:
                return {
                    "success": False,
                    "error": f"API error {response.status_code}: {response.text}",
                    "image_path": None,
                    "text_response": None,
                    "thought_signature": None,
                }

            response_data = response.json()

            # Save image
            saved_path = self._save_response_image(response_data, output_path)

            # Extract text and thought signature
            text_response = self._extract_text_response(response_data)
            thought_signature = self._extract_thought_signature(response_data)

            return {
                "success": saved_path is not None,
                "image_path": saved_path,
                "text_response": text_response,
                "thought_signature": thought_signature,
                "error": None if saved_path else "No image in response",
            }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out",
                "image_path": None,
                "text_response": None,
                "thought_signature": None,
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": None,
                "text_response": None,
                "thought_signature": None,
            }

    def analyze_image(self, image_path: str, analysis_prompt: str) -> dict:
        """
        Analyze an image without generating a new one.
        Uses the model for critique/analysis only.

        Returns:
            dict with keys: success, analysis, error
        """
        # Use the regular Gemini model for analysis (not image generation)
        analysis_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

        headers = {
            "x-goog-api-key": self.api_key,
            "Content-Type": "application/json",
        }

        img_data, mime_type = self._image_to_base64(image_path)

        body = {
            "contents": [{
                "parts": [
                    {
                        "inlineData": {
                            "mimeType": mime_type,
                            "data": img_data
                        }
                    },
                    {"text": analysis_prompt}
                ]
            }]
        }

        try:
            response = requests.post(
                analysis_url,
                headers=headers,
                json=body,
                timeout=60
            )

            if response.status_code != 200:
                return {
                    "success": False,
                    "analysis": None,
                    "error": f"API error {response.status_code}: {response.text}",
                }

            response_data = response.json()
            text = self._extract_text_response(response_data)

            return {
                "success": True,
                "analysis": text,
                "error": None,
            }

        except Exception as e:
            return {
                "success": False,
                "analysis": None,
                "error": str(e),
            }


if __name__ == "__main__":
    # Quick test
    from dotenv import load_dotenv
    load_dotenv()

    client = GeminiImageClient()
    print("Gemini client initialized successfully")
