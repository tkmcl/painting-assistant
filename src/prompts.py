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
        "name": "Notan",
        "focus": "2-value light/dark pattern",
        "learning": "Seeing the big shape of light vs dark",
        "prompt": """Create a 2-VALUE NOTAN study of this photo.

{style_foundation}

VERSION 1 - NOTAN (2 VALUES ONLY):
This is NOT a painting - it's a value map.

RULES:
- ONLY 2 VALUES: Black and White. Nothing else.
- Every area must be either BLACK or WHITE
- Squint at the photo - what reads as "light"? That's white.
- Everything else is black.
- The SHAPE of the light pattern is what matters

The silhouette and gesture must be recognizable.
The face is just shapes - light shape for the lit side, dark for shadow.
No features, no gradients, no in-between values.

This helps you see: Where is the light? Where is the shadow?
""",
        "version_notes": "v2.0 - True 2-value notan for learning light patterns"
    },

    2: {
        "name": "3-Value",
        "focus": "Adding a mid-tone",
        "learning": "Seeing the halftone zone",
        "prompt": """Create a 3-VALUE study of this photo.

{style_foundation}

VERSION 2 - THREE VALUES:
- BLACK (darkest darks, core shadows)
- GRAY (halftones, turning forms)
- WHITE (direct light, highlights)

Now you can show FORM - where light turns to shadow.
The gray is the transition zone.

Still NO features - eyes are dark shapes, not drawn.
The face is sculpted with these 3 values like a simple clay model.
Keep it blocky and simple.

This helps you see: How does the form turn from light to shadow?
""",
        "version_notes": "v2.0 - 3-value study for understanding form"
    },

    3: {
        "name": "5-Value",
        "focus": "Full value range",
        "learning": "Seeing subtle value shifts",
        "prompt": """Create a 5-VALUE study of this photo.

{style_foundation}

VERSION 3 - FIVE VALUES:
1. White (brightest lights)
2. Light gray (lighter halftones)
3. Mid gray (middle values)
4. Dark gray (darker halftones)
5. Black (darkest accents)

Now you have a full value range to work with.
The face starts to have dimension and presence.
Features are still SHAPES made of value - not drawn lines.

Eyes: dark shape + light accent = presence (no iris detail)
Mouth: value change suggests expression (no teeth)

This helps you see: The full range of values that create dimension.
""",
        "version_notes": "v2.0 - 5-value for full tonal range"
    },

    4: {
        "name": "Edges",
        "focus": "Lost and found edges",
        "learning": "Where to blur, where to sharpen",
        "prompt": """Add EDGE VARIATION to the value study.

{style_foundation}

VERSION 4 - EDGES:
Using the same values, now vary the EDGES:
- LOST edges: where form dissolves into background (hair edges, shadow sides)
- SOFT edges: where forms turn gradually
- FIRM edges: most edges, clear but not sharp
- SHARP edges: only at focal point (usually near the eyes)

Only 10-20% of edges should be sharp.
50% or more can be lost or very soft.

The figure should feel like it's emerging from atmosphere.
Hair and shoulders dissolve. Eyes stay defined.

This helps you see: Edge hierarchy creates focus and atmosphere.
""",
        "version_notes": "v2.0 - Edge control for atmosphere"
    },

    5: {
        "name": "Temperature",
        "focus": "Warm lights, cool shadows",
        "learning": "Color temperature in grays",
        "prompt": """Add subtle COLOR TEMPERATURE to the study.

{style_foundation}

VERSION 5 - TEMPERATURE:
Still essentially monochromatic, but with temperature shifts:
- WARM (slightly yellow/orange) in the lights
- COOL (slightly blue/purple) in the shadows

This is very subtle - you should barely notice the color.
It's still a "gray" painting but with life.

Keep all the value work and edge work from before.
Just add this subtle temperature variation.

The person must be recognizable with their exact expression.

This helps you see: How temperature adds life to values.
""",
        "version_notes": "v2.0 - Temperature for final study"
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
