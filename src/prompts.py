"""
Gemini (Nano Banana Pro) prompt templates for painting milestones.

THIS IS THE MOST IMPORTANT FILE FOR TUNING OUTPUT QUALITY.

5 versions: Block-in → Form → Development → Atmosphere → Final

Each prompt has been tested and refined. When modifying:
1. Test the change on multiple reference images
2. Compare against previous outputs
3. Document what changed and why in the version notes
"""

# =============================================================================
# CONFIGURATION
# =============================================================================

NUM_VERSIONS = 5

# =============================================================================
# STYLE FOUNDATION - Used in all prompts
# =============================================================================

STYLE_FOUNDATION = """
TWO REQUIREMENTS - BOTH MUST BE MET:

1. LIKENESS (non-negotiable):
- This must be recognizable as THIS EXACT PERSON
- Same face shape, same expression, same pose
- If mouth is open, it stays open. If hands are up, hands stay up.
- Someone who knows them would recognize them instantly

2. ROUGH PAINTING STYLE (non-negotiable):
- Like a quick alla prima oil sketch - bold and unfinished
- Big chunky strokes - think palette knife, not small brush
- MONOCHROMATIC - grays only, maybe slight warm/cool temperature
- Eyes are DARK SHAPES with a light accent - NO irises, NO pupils
- Mouth is a VALUE SHAPE - no teeth, no lip definition
- 50% of the image should look UNFINISHED
- Visible canvas/paper texture through the paint

DO NOT render details. Suggest everything with VALUE and SHAPE.
The rougher and sketchier, the better - while keeping the likeness.
"""

# =============================================================================
# VERSION-SPECIFIC PROMPTS (5 VERSIONS)
# =============================================================================

PROMPTS = {
    1: {
        "name": "Block-in",
        "focus": "Composition and big value masses",
        "learning": "Seeing shapes, not features",
        "prompt": """Convert this photo into a rough block-in painting study.

{style_foundation}

VERSION 1 - BLOCK-IN:
- Simplify to 3-4 main values: darks, mid-tones, lights
- Big, bold brushstrokes - not blended
- Capture the GESTURE and EXPRESSION even if simplified
- The specific face shape and pose must be preserved
- Features are simplified shapes, but the likeness must be clear

The person must be RECOGNIZABLE even in this simplified state.
If they have a playful expression, it should read as playful.
If hands are up near the face, show hands up near the face.

Keep rough and painterly - visible strokes, no smooth gradients.
But prioritize LIKENESS over abstraction.
""",
        "version_notes": "v1.3 - Balance between rough style and likeness preservation"
    },

    2: {
        "name": "Form & Edges",
        "focus": "3D structure and edge hierarchy",
        "learning": "Seeing form, creating focal point",
        "prompt": """Build on the block-in, adding form while staying bold and rough.

{style_foundation}

VERSION 2 - FORM & EDGES:
- Add 1-2 more gray values (now 4-5 total)
- Show basic planes of the face (forehead, cheek, jaw)
- ONE area can have slightly sharper edges (focal point)
- Keep the bold, chunky brushwork from v1
- Still very rough - this is NOT a finished painting

Keep same pose and composition as the reference.
Features still abstract - eyes as shapes, not detailed.

ABSOLUTELY NO:
- Smooth blending or gradients
- Eye details (irises, pupils, catchlights)
- Teeth, defined lips
- Polished or finished look
""",
        "version_notes": "v1.1 - Simplified, maintains bold style"
    },

    3: {
        "name": "Development",
        "focus": "Feature suggestion and subtle color",
        "learning": "Power of suggestion",
        "prompt": """Develop the painting - more presence, still rough.

{style_foundation}

VERSION 3 - DEVELOPMENT:
- The person is clearly recognizable now
- But features are still SUGGESTED, not RENDERED
- Eyes: dark socket shape + light shape = presence. NO IRIS.
- Mouth: value shape that captures expression. NO TEETH.
- Subtle temperature: warm highlights, cool shadows
- STAY MONOCHROMATIC - grays with temperature, not color

RESIST THE URGE TO ADD DETAIL.
The likeness comes from SHAPE and VALUE, not from rendering.
Keep it looking like a 10-minute oil sketch.
""",
        "version_notes": "v1.4 - Balance likeness and roughness"
    },

    4: {
        "name": "Atmosphere",
        "focus": "Figure/ground integration",
        "learning": "Lost edges",
        "prompt": """Integrate figure and background while maintaining bold style.

{style_foundation}

VERSION 4 - ATMOSPHERE:
- Edges of hair/shoulders dissolve into background
- Figure emerges from the gray atmosphere
- Some facial edges can also dissolve
- Only the focal area (eyes region) stays defined
- Keep the rough, bold brushwork throughout

The painting should feel unified - figure and ground are one.
But still recognizable as the same person.

ABSOLUTELY NO:
- Hard outline around the head
- Figure that looks "pasted on" the background
- Loss of the bold, rough quality
- Photorealistic detail anywhere
""",
        "version_notes": "v1.1 - Simplified, maintains bold integration"
    },

    5: {
        "name": "Final",
        "focus": "Emotional presence, completion",
        "learning": "Knowing when to stop",
        "prompt": """Final version - the person must be unmistakably recognizable.

{style_foundation}

VERSION 5 - FINAL:
- Someone who knows this person should instantly recognize them
- The specific expression and emotion from the photo must be captured
- The unique characteristics of their face must be clear
- Keep the bold, painterly quality but ensure likeness

This is the painting reference you will work from.
It must capture:
1. The exact person (likeness)
2. The exact moment (expression, pose)
3. The painterly style (rough, bold strokes)

Priority order: LIKENESS > EXPRESSION > STYLE
If you have to choose, preserve the person's identity above all.
""",
        "version_notes": "v1.3 - Likeness as top priority"
    },
}


def get_prompt(version: int, include_foundation: bool = True) -> str:
    """Get the prompt for a specific version."""
    if version not in PROMPTS:
        raise ValueError(f"Version {version} not found. Valid versions: 1-{NUM_VERSIONS}")

    prompt_data = PROMPTS[version]
    prompt = prompt_data["prompt"]

    if include_foundation:
        prompt = prompt.replace("{style_foundation}", STYLE_FOUNDATION)
    else:
        prompt = prompt.replace("{style_foundation}", "")

    return prompt


def get_prompt_for_retry(version: int, issues: list[str]) -> str:
    """Get a prompt modified to address specific issues from previous attempt."""
    base_prompt = get_prompt(version)

    issues_text = "\n".join(f"- {issue}" for issue in issues)

    retry_addition = f"""

IMPORTANT - PREVIOUS ATTEMPT HAD THESE ISSUES TO FIX:
{issues_text}

Please specifically address these problems in this generation.
"""

    return base_prompt + retry_addition


def get_all_version_names() -> dict[int, str]:
    """Get a dict of version numbers to names."""
    return {v: data["name"] for v, data in PROMPTS.items()}


# =============================================================================
# CRITIQUE PROMPTS
# =============================================================================

CRITIQUE_PROMPT_TEMPLATE = """You are an art critic evaluating a painting study.

This is VERSION {version} of {total} in a progressive painting series.
Version name: {version_name}
Focus: {version_focus}

STYLE CONTEXT:
- Inspired by INO's technique (atmospheric, lost edges, economy)
- But emotionally: joy/life/presence, NOT melancholy
- Monochromatic grays with subtle color temperature

Please evaluate:

1. TECHNICAL CRITERIA (score 1-10 each):
   - Value structure appropriate for this version?
   - Edge quality appropriate for this version?
   - Atmospheric integration?
   - Painterly quality (not airbrushed)?

2. PROGRESSION CRITERIA:
   - Does this feel like version {version}? (not too advanced, not too basic)
   - Would a painter logically arrive here from version {prev_version}?

3. OVERALL SCORE (1-10)

4. CRITICAL ISSUES (must fix before proceeding)

5. VERDICT: PASS (score >= 7) or FAIL (needs regeneration)

Be strict but constructive.
"""


def get_critique_prompt(version: int) -> str:
    """Get the critique prompt for evaluating a specific version."""
    prompt_data = PROMPTS[version]

    return CRITIQUE_PROMPT_TEMPLATE.format(
        version=version,
        total=NUM_VERSIONS,
        version_name=prompt_data["name"],
        version_focus=prompt_data["focus"],
        prev_version=version - 1 if version > 1 else "N/A"
    )
