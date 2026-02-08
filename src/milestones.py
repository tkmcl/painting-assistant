"""
Progressive painting milestone definitions.

Each milestone builds on the previous, creating a coherent painting journey.

TECHNICAL INSPIRATION from Greek street artist INO:
- Atmospheric values with subtle color undertones
- Faces emerging from atmosphere
- Balance between photorealism and abstraction
- Masterful edge control (lost and found edges)
- Economy of means

EMOTIONAL DIRECTION:
- Capturing life, joy, presence (not melancholy)
- Personal subjects that matter to you
- Paintings that live, touch, and inspire
- The quiet intensity of childhood
- Monochromatic palette YES, somber mood NO
"""

MILESTONES = [
    {
        "version": 1,
        "name": "Block-in",
        "focus": "3-4 value masses only",
        "learning": "Composition and big shapes",
        "prompt_guidance": """
Transform this portrait into an extremely simplified block-in study in the style of INO.
- Use only 3-4 values: dark, mid-dark, mid-light, light
- NO detail whatsoever - just large abstract shapes
- Monochromatic gray tones
- Soft, undefined edges everywhere
- The face should be barely recognizable - just masses of light and shadow
- Think: squinting at the photo until you only see shapes
- Atmospheric, misty background bleeding into the figure
""",
        "self_critique_checklist": [
            "Are there truly only 3-4 distinct values?",
            "Is all detail eliminated?",
            "Does the composition read as abstract shapes?",
            "Is the mood atmospheric and mysterious?",
        ]
    },
    {
        "version": 2,
        "name": "Value Refinement",
        "focus": "5-7 values, soft transitions",
        "learning": "Value relationships and gradation",
        "prompt_guidance": """
Building on the block-in, refine to 5-7 values while maintaining INO's atmospheric style.
- Expand value range slightly: add subtle half-tones
- Keep ALL edges soft and lost
- Still no recognizable features - just more nuanced value masses
- Introduce very subtle temperature shifts in the grays (slightly warm lights, cool shadows)
- The figure should feel like it's emerging from fog
- Maintain the abstract quality from v1
""",
        "self_critique_checklist": [
            "Does this logically progress from v1?",
            "Are there now 5-7 distinct values?",
            "Are edges still soft throughout?",
            "Is there subtle temperature variation in the grays?",
        ]
    },
    {
        "version": 3,
        "name": "Form Emergence",
        "focus": "Basic anatomical forms appear",
        "learning": "Seeing the head as 3D form",
        "prompt_guidance": """
The face begins to emerge from the atmosphere, but remains largely abstract.
- Basic planes of the face become visible (forehead, cheek, jaw)
- Still soft edges, but some areas slightly more defined
- NO sharp details yet
- The eyes may be suggested as dark shapes, not detailed
- Maintain INO's signature atmospheric gray palette
- The figure should feel sculptural, like stone emerging from mist
""",
        "self_critique_checklist": [
            "Are basic facial planes now visible?",
            "Does this feel like a natural progression from v2?",
            "Are details still suppressed?",
            "Does it maintain the atmospheric quality?",
        ]
    },
    {
        "version": 4,
        "name": "Edge Hierarchy",
        "focus": "Sharp vs lost edges",
        "learning": "Where to guide the viewer's eye",
        "prompt_guidance": """
Introduce selective edge control - INO's key technique.
- ONE area gets slightly sharper edges (typically around one eye or bridge of nose)
- Everything else remains soft or completely lost
- This creates the focal point
- The sharp area should be small - maybe 10% of the image
- Background should lose edges entirely, bleeding into the figure
- Maintain monochromatic gray palette with subtle temperature
""",
        "self_critique_checklist": [
            "Is there a clear focal point with sharper edges?",
            "Do most edges remain soft/lost?",
            "Does the background integrate with the figure?",
            "Is the edge hierarchy creating visual flow?",
        ]
    },
    {
        "version": 5,
        "name": "Feature Suggestion",
        "focus": "Eyes and key features hint at existence",
        "learning": "The power of suggestion over statement",
        "prompt_guidance": """
Features begin to be suggested, not stated - INO's restraint.
- Eyes may have a glint of light, but no iris detail
- Nose exists as shadow shapes, not lines
- Mouth is a subtle value shift, not defined lips
- One side of the face can be more defined, other lost in shadow
- Maintain the atmospheric gray palette
- The viewer's mind should complete what isn't painted
""",
        "self_critique_checklist": [
            "Are features suggested rather than explicitly rendered?",
            "Is there asymmetry in definition (one side more lost)?",
            "Does the image invite the viewer to complete it mentally?",
            "Does this progress naturally from v4?",
        ]
    },
    {
        "version": 6,
        "name": "Subtle Color Introduction",
        "focus": "INO's signature color undertones",
        "learning": "Color temperature as emotion",
        "prompt_guidance": """
Introduce INO's subtle color - still predominantly gray but with emotional undertones.
- Very subtle blue or purple in shadow areas
- Slight warmth in light areas (muted peach/ochre)
- Color should be felt more than seen
- If you squint, it should still read as monochromatic
- The color adds emotional depth without being decorative
- Maintain all previous edge hierarchy and atmospheric quality
""",
        "self_critique_checklist": [
            "Is color subtle enough to almost miss?",
            "Does color appear in shadows vs lights appropriately?",
            "Does the image still read as predominantly gray?",
            "Does color add emotion without decoration?",
        ]
    },
    {
        "version": 7,
        "name": "Focal Refinement",
        "focus": "One area gets real attention",
        "learning": "Selective finish in classical painting",
        "prompt_guidance": """
The focal area (usually eyes) gets more attention while periphery stays loose.
- Eyes can now have more definition - catchlights, subtle iris suggestion
- But still not photorealistic - maintain painterly abstraction
- Surrounding areas (hair, shoulders, background) should be even MORE lost
- The contrast between finished and unfinished creates INO's power
- Gray palette with those subtle color undertones established in v6
""",
        "self_critique_checklist": [
            "Is there a clear contrast between focal and peripheral areas?",
            "Does the focal area have more detail while remaining painterly?",
            "Are peripheral areas appropriately lost?",
            "Does this build coherently on v6?",
        ]
    },
    {
        "version": 8,
        "name": "Atmospheric Integration",
        "focus": "Figure and ground become one",
        "learning": "INO's signature 'emerging from mist' quality",
        "prompt_guidance": """
The figure integrates with the background - INO's most distinctive quality.
- Edges of hair/shoulders/clothing dissolve completely into background
- The figure appears to emerge from or sink into the atmosphere
- Some areas of the face may also dissolve
- Only the focal area maintains separation from the ground
- The background is not separate - it's part of the same atmosphere
- Subtle color undertones should unify figure and ground
""",
        "self_critique_checklist": [
            "Does the figure truly integrate with the background?",
            "Are there areas where figure and ground are indistinguishable?",
            "Does the focal area still maintain presence?",
            "Is there that 'emerging from mist' quality?",
        ]
    },
    {
        "version": 9,
        "name": "Emotional Resonance",
        "focus": "The intangible quality that makes a portrait come alive",
        "learning": "Art beyond technique",
        "prompt_guidance": """
Add the emotional weight that elevates technique to art.
- There should be something in the expression - joy, intensity, presence, life
- The gaze (if visible) should feel present, not vacant
- Subtle adjustments to value can add weight and gravity
- The image should provoke feeling, not just technical appreciation
- Consider: what is this portrait saying? What does it make you feel?
- Maintain all technical achievements from previous versions
""",
        "self_critique_checklist": [
            "Does the image provoke an emotional response?",
            "Is there something 'alive' in the expression?",
            "Does it transcend technical exercise?",
            "Would INO recognize this as aligned with his sensibility?",
        ]
    },
    {
        "version": 10,
        "name": "Final Refinement",
        "focus": "Polish without overworking",
        "learning": "Knowing when to stop",
        "prompt_guidance": """
Final adjustments - the hardest part: knowing when NOT to add more.
- Check value structure one more time - adjust if needed
- Ensure focal area has enough presence
- Ensure lost edges are truly lost
- The finish should feel inevitable, not overworked
- INO's work has economy - nothing extra, nothing missing
- This is the version you will paint from
""",
        "self_critique_checklist": [
            "Is every element serving the whole?",
            "Is there anything that could be removed?",
            "Does it feel complete without being overworked?",
            "Would this translate well to an actual painting?",
            "Does the full v1-v10 journey make sense as a painting progression?",
        ]
    },
]


def get_milestone(version: int) -> dict:
    """Get milestone definition by version number (1-10)."""
    return MILESTONES[version - 1]


def get_cumulative_context(up_to_version: int) -> str:
    """Get context from all previous milestones for coherence."""
    context_parts = []
    for i in range(up_to_version):
        m = MILESTONES[i]
        context_parts.append(f"v{m['version']} ({m['name']}): {m['focus']}")
    return "\n".join(context_parts)
