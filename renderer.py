import random
import textwrap

from PIL import Image, ImageDraw, ImageFont

FONT_DIR = "fonts"
PAPER_COLOR = (253, 246, 227)
LINE_COLOR = (167, 195, 215)
INK_COLOR = (25, 25, 60)
MARGIN = 60
LINE_SPACING = 1.35
CHAR_JITTER = 2


def _load_font(size: int, bold: bool) -> ImageFont.FreeTypeFont:
    name = "AmaticSC-Bold.ttf" if bold else "AmaticSC-Regular.ttf"
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


def _paper(width: int, height: int, line_step: int) -> Image.Image:
    img = Image.new("RGB", (width, height), PAPER_COLOR)
    draw = ImageDraw.Draw(img)
    top = MARGIN + line_step
    y = top
    while y < height - MARGIN // 2:
        draw.line([(MARGIN // 2, y), (width - MARGIN // 2, y)], fill=LINE_COLOR, width=1)
        y += line_step
    return img


def render_handwriting(
    text: str,
    font_size: int = 48,
    bold: bool = False,
    max_chars: int = 1500,
) -> Image.Image:
    text = text.strip()
    if not text:
        raise ValueError("Matn bo'sh")
    if len(text) > max_chars:
        raise ValueError(f"Matn juda uzun (maksimal {max_chars} belgi)")

    font = _load_font(font_size, bold)
    probe = Image.new("RGB", (10, 10))
    probe_draw = ImageDraw.Draw(probe)

    line_step = int(font_size * LINE_SPACING)
    max_width = 900
    lines = []
    for raw in text.split("\n"):
        if not raw.strip():
            lines.append("")
            continue
        wrapped = textwrap.wrap(raw, width=48) or [""]
        lines.extend(wrapped)

    width = 1000
    height = MARGIN * 2 + line_step * len(lines)
    img = _paper(width, height, line_step)
    draw = ImageDraw.Draw(img)

    rng = random.Random(text)
    y = MARGIN
    for line in lines:
        x = MARGIN
        for char in line:
            dx = rng.randint(-CHAR_JITTER, CHAR_JITTER)
            dy = rng.randint(-CHAR_JITTER, CHAR_JITTER)
            angle = rng.uniform(-2, 2)
            char_img = Image.new("RGBA", (font_size * 2, font_size * 3), (0, 0, 0, 0))
            char_draw = ImageDraw.Draw(char_img)
            char_draw.text((font_size // 2, font_size), char, font=font, fill=INK_COLOR)
            char_img = char_img.rotate(angle, resample=Image.BICUBIC, expand=False)
            img.paste(char_img, (x + dx, y + dy - font_size), char_img)
            bbox = probe_draw.textbbox((0, 0), char, font=font)
            x += max(bbox[2] - bbox[0], 4)
        y += line_step

    return img
