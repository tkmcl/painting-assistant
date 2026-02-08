"""
Main pipeline for generating progressive painting studies.

This is the core orchestration that:
1. Takes an input photo
2. Generates v1-v5 progressively (each building on previous)
3. Self-critiques each version
4. Iterates until quality threshold is met
5. Ensures coherence across the full series
"""

import os
import json
from pathlib import Path
from datetime import datetime
from typing import Optional
import shutil

from .gemini_client import GeminiImageClient
from .prompts import get_prompt, get_prompt_for_retry, NUM_VERSIONS, PROMPTS
from .critique import ImageCritic


class PaintingPipeline:
    """Orchestrates the full v1-v5 painting study generation."""

    MAX_ITERATIONS_PER_VERSION = 3  # Max retries before moving on
    MIN_SCORE_TO_PASS = 7

    def __init__(
        self,
        output_dir: str = "output",
        api_key: Optional[str] = None,
    ):
        self.client = GeminiImageClient(api_key)
        self.critic = ImageCritic(self.client)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_version(
        self,
        input_image_path: str,
        version: int,
        session_dir: Path,
        previous_image_path: Optional[str] = None,
        thought_signature: Optional[str] = None,
    ) -> dict:
        """
        Generate a single version with self-critique loop.

        Returns:
            dict with: success, image_path, thought_signature, attempts, final_score
        """
        version_info = PROMPTS[version]
        print(f"\n{'='*60}")
        print(f"GENERATING VERSION {version}/{NUM_VERSIONS}: {version_info['name']}")
        print(f"Focus: {version_info['focus']}")
        print(f"{'='*60}")

        attempts = []
        best_result = None
        best_score = 0

        for iteration in range(self.MAX_ITERATIONS_PER_VERSION):
            print(f"\n--- Attempt {iteration + 1}/{self.MAX_ITERATIONS_PER_VERSION} ---")

            # Build prompt
            is_retry = iteration > 0
            previous_issues = attempts[-1]["issues"] if is_retry and attempts else []

            if is_retry and previous_issues:
                prompt = get_prompt_for_retry(version, previous_issues)
            else:
                prompt = get_prompt(version)

            # Generate image
            output_path = session_dir / f"v{version:02d}_attempt{iteration + 1}.png"

            # Use previous version's output as reference for continuity (if available)
            # Otherwise fall back to original input
            reference_path = previous_image_path if previous_image_path else input_image_path

            gen_result = self.client.generate_image(
                prompt=prompt,
                reference_image_path=reference_path,
                output_path=str(output_path),
                aspect_ratio="4:5",  # 80x100cm canvas
                image_size="2K",
                previous_thought_signature=thought_signature,
            )

            if not gen_result["success"]:
                print(f"Generation failed: {gen_result['error']}")
                attempts.append({
                    "iteration": iteration + 1,
                    "success": False,
                    "error": gen_result["error"],
                    "issues": ["Generation failed"],
                    "score": 0,
                })
                continue

            print(f"Image generated: {output_path}")

            # Self-critique
            print("Running self-critique...")
            critique_result = self.critic.critique_image(
                image_path=str(output_path),
                version=version,
                previous_image_path=previous_image_path,
            )

            score = critique_result.get("overall_score", 0)
            passed = critique_result.get("passed", False)

            print(f"Score: {score}/10 - {'PASS' if passed else 'FAIL'}")

            attempt_record = {
                "iteration": iteration + 1,
                "success": True,
                "image_path": str(output_path),
                "score": score,
                "passed": passed,
                "issues": critique_result.get("issues", []),
                "critique": critique_result.get("critique", ""),
                "thought_signature": gen_result.get("thought_signature"),
            }
            attempts.append(attempt_record)

            # Track best result
            if score > best_score:
                best_score = score
                best_result = attempt_record

            # Check if passed
            if passed and score >= self.MIN_SCORE_TO_PASS:
                print(f"Version {version} PASSED with score {score}")
                break
            else:
                if critique_result.get("issues"):
                    print("Issues to address:")
                    for issue in critique_result["issues"][:3]:
                        print(f"  - {issue}")

        # Use best result even if not perfect
        if best_result:
            # Rename best attempt to final version
            final_path = session_dir / f"v{version:02d}_final.png"
            best_path = Path(best_result["image_path"])
            if best_path.exists():
                best_path.rename(final_path)
                best_result["image_path"] = str(final_path)

            return {
                "success": True,
                "image_path": str(final_path),
                "thought_signature": best_result.get("thought_signature"),
                "attempts": len(attempts),
                "final_score": best_score,
                "passed": best_result.get("passed", False),
            }

        return {
            "success": False,
            "image_path": None,
            "thought_signature": None,
            "attempts": len(attempts),
            "final_score": 0,
            "passed": False,
        }

    def run_full_pipeline(
        self,
        input_image_path: str,
        session_name: Optional[str] = None,
    ) -> dict:
        """
        Run the complete v1-v5 generation pipeline.

        Args:
            input_image_path: Path to the source photo
            session_name: Optional name for this session

        Returns:
            dict with: success, session_dir, versions (list of results), summary
        """
        # Create session directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_name = session_name or Path(input_image_path).stem
        session_dir = self.output_dir / f"{session_name}_{timestamp}"
        session_dir.mkdir(parents=True, exist_ok=True)

        print(f"\n{'#'*60}")
        print(f"PAINTING PIPELINE - {session_name}")
        print(f"Versions: {NUM_VERSIONS}")
        print(f"Output: {session_dir}")
        print(f"{'#'*60}")

        # Copy input image to session
        input_copy = session_dir / f"00_original{Path(input_image_path).suffix}"
        shutil.copy(input_image_path, input_copy)

        results = {
            "success": True,
            "session_dir": str(session_dir),
            "input_image": str(input_copy),
            "versions": [],
            "summary": {},
        }

        previous_image_path = None
        thought_signature = None

        # Generate each version sequentially
        for version in range(1, NUM_VERSIONS + 1):
            version_result = self.generate_version(
                input_image_path=input_image_path,
                version=version,
                session_dir=session_dir,
                previous_image_path=previous_image_path,
                thought_signature=thought_signature,
            )

            results["versions"].append({
                "version": version,
                "name": PROMPTS[version]["name"],
                **version_result,
            })

            if version_result["success"]:
                previous_image_path = version_result["image_path"]
                thought_signature = version_result.get("thought_signature")
            else:
                print(f"\nWARNING: Version {version} failed, continuing with previous...")

        # Generate summary
        passed_count = sum(1 for v in results["versions"] if v.get("passed", False))
        avg_score = sum(v.get("final_score", 0) for v in results["versions"]) / NUM_VERSIONS

        results["summary"] = {
            "versions_passed": passed_count,
            "versions_total": NUM_VERSIONS,
            "average_score": round(avg_score, 1),
            "total_attempts": sum(v.get("attempts", 0) for v in results["versions"]),
        }

        # Save results to JSON
        results_path = session_dir / "results.json"
        with open(results_path, "w") as f:
            json.dump(results, f, indent=2)

        print(f"\n{'#'*60}")
        print("PIPELINE COMPLETE")
        print(f"Versions passed: {passed_count}/{NUM_VERSIONS}")
        print(f"Average score: {avg_score:.1f}/10")
        print(f"Results saved to: {results_path}")
        print(f"{'#'*60}")

        return results


def main():
    """CLI entry point."""
    import argparse
    from dotenv import load_dotenv

    load_dotenv(override=True)

    parser = argparse.ArgumentParser(
        description="Generate progressive painting studies"
    )
    parser.add_argument(
        "input_image",
        help="Path to the source photo"
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "--name",
        help="Session name (default: input filename)"
    )

    args = parser.parse_args()

    pipeline = PaintingPipeline(output_dir=args.output_dir)
    results = pipeline.run_full_pipeline(
        input_image_path=args.input_image,
        session_name=args.name,
    )

    return 0 if results["success"] else 1


if __name__ == "__main__":
    exit(main())
