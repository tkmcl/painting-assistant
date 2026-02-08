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
CRITICAL - PRESERVE IDENTITY:
- The subject MUST be immediately recognizable as the same person in the reference photo
- Key proportions: distance between eyes, nose length, face shape, chin - MUST match exactly
- Even when abstract, the ESSENCE and LIKENESS of the person must be unmistakable
- If someone knows this person, they should recognize them instantly

STYLE REFERENCE - Greek street artist INO:
- VERY loose, broad, rough brushstrokes - NOT smooth or polished
- Monochromatic gray palette with subtle temperature shifts
- EXTREMELY atmospheric - figure emerges from/blends with background
- Most edges COMPLETELY LOST - only 5-10% of edges are sharp
- Economy of means - LESS is more, always err on the side of MORE ABSTRACTION
- This should look like a ROUGH PAINTING, not a photograph with a filter
- Think: bold, expressive, unfinished quality

EMOTIONAL DIRECTION:
- Capture life, joy, presence (not INO's melancholy)
- The subject should feel alive despite the abstraction
"""

# =============================================================================
# VERSION-SPECIFIC PROMPTS (5 VERSIONS)
# =============================================================================

PROMPTS = {
    1: {
        "name": "Block-in",
        "focus": "Composition and big value masses",
        "learning": "Seeing shapes, not features",
        "prompt": """Transform this portrait into an extremely simplified block-in painting study.

{style_foundation}

VERSION 1 REQUIREMENTS - BLOCK-IN:
- Use ONLY 3-4 distinct values: dark, mid-dark, mid-light, light
- NO detail whatsoever - just large abstract value shapes
- ALL edges must be soft and undefined
- The face should be barely recognizable - just masses of light and shadow
- Think: what you see when you squint until the photo is almost blurred out
- Background should blend seamlessly into figure - no hard separation
- Painterly texture - visible brushstrokes, not smooth gradients

DO NOT include:
- Any recognizable features (no eyes, nose details, lip definition)
- Sharp edges anywhere
- More than 4 distinct values
- Smooth, airbrushed transitions

OUTPUT: A painterly value study that looks like the first 5 minutes of a portrait painting.
""",
        "version_notes": "v1.0 - Initial prompt"
    },

    2: {
        "name": "Form & Edges",
        "focus": "3D structure and edge hierarchy",
        "learning": "Seeing form, creating focal point",
        "prompt": """Transform this portrait showing 3D form with selective edge control.

{style_foundation}

VERSION 2 REQUIREMENTS - FORM & EDGES:
- Expand to 5-6 distinct values
- Basic planes of the face become visible (forehead, cheek, jaw planes)
- Introduce edge hierarchy: ONE area gets slightly sharper edges (near eye or nose bridge)
- This sharp area = focal point, everything else stays soft or lost
- The face should feel sculptural - forms emerging from atmosphere
- Background edges dissolve - figure bleeds into ground

PROGRESSION FROM V1:
- Same composition and basic masses
- Now adding 3D form through plane changes
- Introducing selective sharpness for focal point

DO NOT include:
- Multiple competing sharp areas
- Detailed eyes/nose/mouth
- Sharp edges at head outline
- Loss of atmospheric quality

OUTPUT: A portrait with emerging 3D form and clear focal point hierarchy.
""",
        "version_notes": "v1.0 - Combined form emergence + edge hierarchy from 10-version system"
    },

    3: {
        "name": "Development",
        "focus": "Feature suggestion and color temperature",
        "learning": "Power of suggestion, emotional color",
        "prompt": """Transform this portrait with suggested features and subtle color temperature.

{style_foundation}

VERSION 3 REQUIREMENTS - DEVELOPMENT:
- Features are SUGGESTED, not explicitly rendered
- Eyes: hint of light/presence, but no iris/pupil detail
- Nose: shadow shapes define it, not lines
- Mouth: subtle value shift, not defined lips
- One side more defined, other side lost in atmosphere
- Introduce subtle color temperature: warm lights, cool shadows
- Color should be FELT more than SEEN - still reads as monochromatic when squinting

PROGRESSION FROM V2:
- Building on established form and edge hierarchy
- Adding feature hints within focal area
- Introducing emotional color temperature

DO NOT include:
- Fully rendered features with detail
- Obvious color that jumps out
- Both sides equally defined
- Loss of atmospheric integration

OUTPUT: A portrait where features are felt more than seen, with subtle color emotion.
""",
        "version_notes": "v1.0 - Combined feature suggestion + color from 10-version system"
    },

    4: {
        "name": "Atmosphere",
        "focus": "Figure/ground integration, refinement",
        "learning": "Lost edges, unified atmosphere",
        "prompt": """Transform this portrait with complete atmospheric integration.

{style_foundation}

VERSION 4 REQUIREMENTS - ATMOSPHERE:
- Edges of hair/shoulders/clothing dissolve COMPLETELY into background
- Figure appears to emerge from or sink into the atmosphere
- Some areas of the face may also dissolve
- Only the focal area maintains clear presence
- Background is not separate - same atmospheric substance as figure
- Focal point gets final refinement - may include subtle catchlights
- Color temperature unifies figure and ground

PROGRESSION FROM V3:
- Pushing lost edges much further
- Creating signature "emerging from mist" quality
- Refining focal point while losing periphery

DO NOT include:
- Clear outline of head/hair against background
- Figure that feels "pasted on" background
- Loss of focal point presence
- Photorealistic detail even in focal area

OUTPUT: A portrait where subject and atmosphere are inseparable.
""",
        "version_notes": "v1.0 - Combined atmospheric integration + focal refinement from 10-version system"
    },

    5: {
        "name": "Final",
        "focus": "Emotional resonance, completion",
        "learning": "Art beyond technique, knowing when to stop",
        "prompt": """Transform this portrait into a finished painting reference with emotional presence.

{style_foundation}

VERSION 5 REQUIREMENTS - FINAL:
- Something in the expression should connect - joy, intensity, presence, LIFE
- The gaze (if visible) should feel present and alive, not vacant
- Check all technical elements: values, edges, atmosphere, color temperature
- The finish should feel inevitable, not overworked
- Economy: nothing extra, nothing missing
- This is the version you will paint from

FINAL CHECKLIST:
- Values reading correctly? (established in V1-2)
- Edge hierarchy clear? (established in V2)
- Features suggested not stated? (established in V3)
- Figure integrated with atmosphere? (established in V4)
- Does it connect emotionally? (this version)
- Is it complete without being overworked?

DO NOT include:
- Empty or vacant expression
- Overworked details that kill the life
- Loss of any atmospheric quality
- Anything that doesn't serve the whole

OUTPUT: A finished painting reference - technically accomplished AND emotionally alive.
""",
        "version_notes": "v1.0 - Combined emotional resonance + final refinement from 10-version system"
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
