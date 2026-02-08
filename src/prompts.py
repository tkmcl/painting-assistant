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
CRITICAL - PRESERVE THE REFERENCE EXACTLY:
- Keep the EXACT pose, head angle, and composition from the reference photo
- PRESERVE THE EXPRESSION - if mouth is open, keep it open. If eyes are wide, keep them wide.
- The person must be RECOGNIZABLE - same face shape, same age, same expression, same emotion
- This is a transformation of THIS SPECIFIC MOMENT, not a generic portrait

STYLE - BOLD, ROUGH, UNFINISHED:
- Like a 3-minute charcoal sketch, not a finished painting
- HUGE, CHUNKY brushstrokes - think house painter, not portrait artist
- HIGH CONTRAST - push toward pure black and pure white
- Features are SUGGESTED with single marks, never rendered
- Leave areas UNFINISHED - raw canvas showing through
- Every stroke should look urgent and confident, not careful
- More like a woodcut or linocut than a painting

TEXTURE:
- Visible brush drag marks
- Dry brush texture
- Strokes that don't quite connect
- Rough edges where paint was applied quickly

THIS IS NOT:
- A polished portrait
- Smooth or blended anywhere
- Carefully rendered
- A photo filter effect
"""

# =============================================================================
# VERSION-SPECIFIC PROMPTS (5 VERSIONS)
# =============================================================================

PROMPTS = {
    1: {
        "name": "Block-in",
        "focus": "Composition and big value masses",
        "learning": "Seeing shapes, not features",
        "prompt": """Convert this photo into an extremely rough, bold block-in study.

{style_foundation}

VERSION 1 - BLOCK-IN:
- ONLY 3 values: BLACK, WHITE, and ONE gray
- Massive, chunky brushstrokes
- NO facial features - just big shapes of light and dark
- Eyes are just dark shapes, no detail
- Think: what you see if you blur the photo completely
- Background and figure should merge - no clean edges anywhere

Keep the same pose and head angle as the photo.
The person should be barely recognizable - just abstract masses that hint at a face.

ABSOLUTELY NO:
- Eye details, pupils, irises
- Teeth or lip definition
- Hair strands
- More than 3 values
- Smooth blending
- Anything that looks "finished"
""",
        "version_notes": "v1.2 - Pushed for extreme simplification, 3 values only"
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
        "prompt": """Develop the painting with suggested features while staying ROUGH.

{style_foundation}

VERSION 3 - DEVELOPMENT:
- Features are SHAPES, not details
- Eyes: just dark sockets with a hint of light - NO eyeballs, NO irises
- Mouth: if open in reference, keep it as a DARK SHAPE - no teeth detail
- Nose: ONE stroke for shadow, that's it
- Add subtle warm/cool temperature shift
- KEEP IT ROUGH - resist the urge to refine

The expression must match the reference - playful stays playful, serious stays serious.
Still looks like a quick study, not a finished painting.

ABSOLUTELY NO:
- Drawing the eyeballs
- Rendering the mouth
- Defining individual features
- Smoothing or blending
- Making it "prettier"
""",
        "version_notes": "v1.2 - Stronger emphasis on keeping rough, preserving expression"
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
        "prompt": """Final pass - capture the life while STAYING ROUGH.

{style_foundation}

VERSION 5 - FINAL:
- The expression must MATCH THE REFERENCE - same emotion, same energy
- If they looked playful/surprised in the photo, they look playful/surprised now
- Eyes: presence through VALUE, not detail - dark socket, light shape, DONE
- This is STILL a rough study - it just has more presence

DO NOT:
- Add detail to make it "finished"
- Smooth anything out
- Make the eyes more realistic
- Close an open mouth or change the expression

The magic is in what you DON'T paint.
Keep 50% of this looking unfinished.
This is a bold sketch that captures a moment, not a polished portrait.

STOP BEFORE YOU THINK YOU'RE DONE.
""",
        "version_notes": "v1.2 - Stronger emphasis on staying rough and preserving expression"
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
