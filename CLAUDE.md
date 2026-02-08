# Painting Assistant

A tool to generate progressive painting studies from photos, helping you learn to paint step-by-step.

## Project Goal

Transform photos (primarily of your kids) into 5-stage painting references in a monochromatic, atmospheric style inspired by Greek street artist INO's technique - but with YOUR emotional direction: joy, life, presence (not INO's typical melancholy).

**Key requirements:**
- Subject must remain RECOGNIZABLE - likeness is critical
- Style should be ROUGH and PAINTERLY, not smooth/polished
- More abstraction, fewer details than typical AI output

## How It Works

1. **Input**: A photo (portrait of your kids)
2. **Process**: Generate v1 → v5 progressively, each building on the previous
3. **Output**: 5 images representing painting milestones
4. **Your job**: Paint along with these references on your 80x100cm canvas

## The 5 Versions

| Version | Name | Focus | What You Learn |
|---------|------|-------|----------------|
| v1 | Block-in | 3-4 values, composition | Seeing shapes, not features |
| v2 | Form & Edges | 3D structure, edge hierarchy | Seeing form, creating focal point |
| v3 | Development | Feature suggestion, color temp | Power of suggestion, emotional color |
| v4 | Atmosphere | Figure/ground integration | Lost edges, unified atmosphere |
| v5 | Final | Emotional resonance, completion | Art beyond technique, when to stop |

## Technical Details

### Canvas
- **Size**: 80x100cm
- **Aspect ratio**: 4:5 (can be portrait or landscape depending on photo)

### Style Direction
- **Technical model**: INO (atmospheric grays, lost edges, economy)
- **Emotional direction**: Life, joy, presence - NOT melancholy
- **Palette**: Monochromatic grays with subtle color temperature
- **Brushwork**: ROUGH, painterly, visible strokes - NOT smooth or airbrushed

### Image Generation
- **Model**: Gemini 3 Pro Image Preview (`gemini-3-pro-image-preview`)
- **Resolution**: 2K
- **Aspect ratio**: 4:5

## Key Files

- `src/prompts.py` - **THE MOST IMPORTANT FILE** - All Gemini prompts live here. Tune these to improve output quality.
- `src/pipeline.py` - Orchestrates the v1→v5 generation with self-critique loop
- `src/gemini_client.py` - API client for Gemini image generation
- `src/critique.py` - Self-critique system for quality control

## Usage

```bash
# Generate a full v1-v5 series
python run.py input/photo.jpg my_painting_name

# Output goes to output/my_painting_name_TIMESTAMP/
```

## Prompt Tuning

The prompts in `src/prompts.py` are the key to quality output. When tuning:

1. **Test one version at a time** - Don't change multiple prompts at once
2. **Test on multiple reference images** - What works for one photo may not work for another
3. **Check coherence** - Each version must logically follow from the previous
4. **Document changes** - Use the `version_notes` field in each prompt

### Current issues to address:
- Likeness preservation - outputs don't always look like the original person
- Too much detail - need MORE abstraction, rougher brushwork
- Too smooth/polished - should look like actual rough paintings

### What to tune:
- Identity preservation instructions
- Explicit value counts ("3-4 values" not "limited values")
- Edge descriptions ("soft", "lost", "sharp")
- Negative instructions ("DO NOT include...")
- Abstraction level

## Self-Critique Loop

Each version goes through:
1. Generate image with prompt
2. Analyze with critique prompt (using Gemini 2.0 Flash)
3. If score < 7 or issues found, regenerate with issues addressed
4. Max 3 attempts per version
5. Keep best result, move to next version

## Your Reference Painting

Your existing painting (`examples/IMG_3381.jpeg`) shows the target style:
- Bold value structure (good dark/light separation)
- Loose, rough brushwork (expressive)
- Monochromatic palette
- Subject immediately recognizable

The AI outputs should look MORE like your painting, not less.

## Environment

Requires `GEMINI_API_KEY` in `.env` file.
