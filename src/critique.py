"""
Self-critique system for evaluating generated images against
milestone requirements.
"""

from typing import Optional
from .gemini_client import GeminiImageClient
from .prompts import get_critique_prompt


class ImageCritic:
    """Evaluates generated images for quality and style adherence."""

    def __init__(self, client: GeminiImageClient):
        self.client = client

    def critique_image(
        self,
        image_path: str,
        version: int,
        previous_image_path: Optional[str] = None,
    ) -> dict:
        """
        Critique an image against milestone requirements.

        Returns:
            dict with keys: success, passed, overall_score, critique, issues, suggestions
        """
        prompt = get_critique_prompt(version)

        if previous_image_path and version > 1:
            prompt += f"""
IMPORTANT: This should feel like a natural progression from version {version-1}.
Does it build coherently on what came before?
"""

        result = self.client.analyze_image(image_path, prompt)

        if not result["success"]:
            return {
                "success": False,
                "passed": False,
                "overall_score": 0,
                "critique": None,
                "issues": ["Failed to analyze image"],
                "suggestions": [],
                "error": result["error"],
            }

        # Parse the critique response
        analysis = result["analysis"]

        # Simple heuristic parsing - look for PASS/FAIL and scores
        passed = "PASS" in analysis.upper() and "FAIL" not in analysis.upper().split("PASS")[0]

        # Try to extract overall score
        overall_score = 5  # default
        if "OVERALL SCORE" in analysis.upper():
            try:
                import re
                score_match = re.search(r'overall\s*score[:\s]*(\d+)', analysis, re.IGNORECASE)
                if score_match:
                    overall_score = int(score_match.group(1))
            except:
                pass

        # Extract critical issues
        issues = []
        if "CRITICAL ISSUES" in analysis.upper():
            try:
                start = analysis.upper().find("CRITICAL ISSUES")
                end = analysis.upper().find("VERDICT", start)
                if end == -1:
                    end = len(analysis)
                issues_text = analysis[start:end]
                import re
                issue_items = re.findall(r'[-•*]\s*(.+?)(?=[-•*]|\n\n|$)', issues_text, re.DOTALL)
                issues = [item.strip() for item in issue_items if item.strip()]
            except:
                pass

        return {
            "success": True,
            "passed": passed,
            "overall_score": overall_score,
            "critique": analysis,
            "issues": issues,
            "suggestions": [],
            "error": None,
        }
