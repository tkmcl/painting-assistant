"""
Grid overlay utility for painting reference images.

Adds a proportional grid to help transfer the image to canvas.
"""

from pathlib import Path
from PIL import Image, ImageDraw


def add_grid_overlay(
    input_path: str,
    output_path: str = None,
    grid_size_cm: float = 10.0,  # Size of each grid square in cm on your canvas
    canvas_width_cm: float = 80.0,  # Your canvas width in cm
    canvas_height_cm: float = 100.0,  # Your canvas height in cm
    major_every: int = 2,  # Major line every N squares (2 = 20cm major grid)
    major_color: tuple = (255, 0, 0),  # red
    minor_color: tuple = (255, 100, 100),  # light red
    major_width: int = 3,
    minor_width: int = 1,
    opacity: float = 0.7,
) -> str:
    """
    Add a grid overlay to an image, scaled to match your canvas.

    The grid squares will be proportional - if you draw the same grid
    on your canvas (using grid_size_cm), the proportions will match.

    Args:
        input_path: Path to input image
        output_path: Path for output (default: adds _grid suffix)
        grid_size_cm: Size of minor grid squares on your canvas (cm)
        canvas_width_cm: Your canvas width in cm
        canvas_height_cm: Your canvas height in cm
        major_every: Draw major gridline every N minor squares
        major_color: RGB color for major grid lines
        minor_color: RGB color for minor grid lines
        major_width: Line width for major grid
        minor_width: Line width for minor grid
        opacity: Grid opacity (0-1)

    Returns:
        Path to output image
    """
    if output_path is None:
        p = Path(input_path)
        output_path = str(p.parent / f"{p.stem}_grid{p.suffix}")

    # Open image
    img = Image.open(input_path).convert("RGBA")
    img_width, img_height = img.size

    # Calculate image aspect ratio
    img_aspect = img_width / img_height
    canvas_aspect = canvas_width_cm / canvas_height_cm

    print(f"Image size: {img_width}x{img_height} (aspect: {img_aspect:.3f})")
    print(f"Canvas size: {canvas_width_cm}x{canvas_height_cm}cm (aspect: {canvas_aspect:.3f})")

    # Determine how to fit the image to canvas
    # The image will be scaled to fit within the canvas, maintaining aspect ratio
    if img_aspect > canvas_aspect:
        # Image is wider than canvas - fit to width
        effective_width_cm = canvas_width_cm
        effective_height_cm = canvas_width_cm / img_aspect
    else:
        # Image is taller than canvas - fit to height
        effective_height_cm = canvas_height_cm
        effective_width_cm = canvas_height_cm * img_aspect

    print(f"Effective painting area: {effective_width_cm:.1f}x{effective_height_cm:.1f}cm")

    # Calculate number of grid squares
    cols = int(effective_width_cm / grid_size_cm)
    rows = int(effective_height_cm / grid_size_cm)

    # Ensure at least 1 square
    cols = max(1, cols)
    rows = max(1, rows)

    print(f"Grid: {cols}x{rows} squares ({grid_size_cm}cm each)")
    print(f"Major lines every {major_every} squares ({grid_size_cm * major_every}cm)")

    # Create transparent overlay for grid
    overlay = Image.new("RGBA", (img_width, img_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # Calculate pixel spacing for grid squares
    x_spacing = img_width / cols
    y_spacing = img_height / rows

    # Draw minor grid lines first (so major lines are on top)
    minor_rgba = (*minor_color, int(255 * opacity))

    # All vertical lines
    for i in range(cols + 1):
        x = int(i * x_spacing)
        is_major = (i % major_every == 0)
        if not is_major:
            draw.line([(x, 0), (x, img_height)], fill=minor_rgba, width=minor_width)

    # All horizontal lines
    for i in range(rows + 1):
        y = int(i * y_spacing)
        is_major = (i % major_every == 0)
        if not is_major:
            draw.line([(0, y), (img_width, y)], fill=minor_rgba, width=minor_width)

    # Draw major grid lines
    major_rgba = (*major_color, int(255 * opacity))

    # Vertical major lines
    for i in range(0, cols + 1, major_every):
        x = int(i * x_spacing)
        draw.line([(x, 0), (x, img_height)], fill=major_rgba, width=major_width)

    # Horizontal major lines
    for i in range(0, rows + 1, major_every):
        y = int(i * y_spacing)
        draw.line([(0, y), (img_width, y)], fill=major_rgba, width=major_width)

    # Composite overlay onto original
    result = Image.alpha_composite(img, overlay)

    # Convert back to RGB for saving as PNG/JPG
    result = result.convert("RGB")
    result.save(output_path)

    return output_path


def add_grid_to_session(session_dir: str, **grid_kwargs) -> list[str]:
    """
    Add grid overlay to all final versions in a session directory.

    Args:
        session_dir: Path to session output directory
        **grid_kwargs: Arguments to pass to add_grid_overlay

    Returns:
        List of paths to gridded images
    """
    session_path = Path(session_dir)
    gridded = []

    # Find all final version images
    for img_path in sorted(session_path.glob("v*_final.png")):
        output_path = add_grid_overlay(str(img_path), **grid_kwargs)
        gridded.append(output_path)

    return gridded


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m src.grid <session_dir_or_image> [grid_size_cm] [canvas_width] [canvas_height]")
        print("\nExamples:")
        print("  python -m src.grid output/session/  # Uses defaults: 10cm grid, 80x100cm canvas")
        print("  python -m src.grid output/session/ 10 80 100  # 10cm squares on 80x100cm canvas")
        print("  python -m src.grid output/session/ 5 60 80   # 5cm squares on 60x80cm canvas")
        print("  python -m src.grid image.png 10 80 100")
        sys.exit(1)

    target = sys.argv[1]

    # Parse optional arguments
    grid_size = float(sys.argv[2]) if len(sys.argv) > 2 else 10.0
    canvas_w = float(sys.argv[3]) if len(sys.argv) > 3 else 80.0
    canvas_h = float(sys.argv[4]) if len(sys.argv) > 4 else 100.0

    kwargs = {
        "grid_size_cm": grid_size,
        "canvas_width_cm": canvas_w,
        "canvas_height_cm": canvas_h,
    }

    print(f"Grid settings: {grid_size}cm squares on {canvas_w}x{canvas_h}cm canvas")
    print(f"Major lines every 2 squares ({grid_size * 2}cm)")
    print()

    if Path(target).is_dir():
        add_grid_to_session(target, **kwargs)
    else:
        result = add_grid_overlay(target, **kwargs)
        print(f"Created: {result}")
