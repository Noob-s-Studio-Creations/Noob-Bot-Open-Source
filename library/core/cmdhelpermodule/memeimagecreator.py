import discord
import tempfile
import os

from PIL import Image, ImageDraw, ImageFont

from library.core.helpmodule.randomtextcreator import GetRandomText
from library.core import console

import botconfig as config

def wrap_text(text, font, max_width, draw):
    lines = []

    for paragraph in text.split("\n"):
        words = paragraph.split()
        current_line = ""

        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            bbox = draw.textbbox((0, 0), test_line, font=font)
            text_width = bbox[2] - bbox[0]

            if text_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        lines.append("")

    if lines and lines[-1] == "":
        lines.pop()

    return lines

Temp_Path = os.path.join(
    tempfile.gettempdir(),
    config.BotOwnerTeam,
    config.AppName,
    "temporary",
    "memeeditor"
)

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = os.path.abspath(
    os.path.join(CURRENT_DIR, "..", "..", "..")
)

Fredoka_One = os.path.join(
    PROJECT_ROOT,
    "assets",
    "fonts",
    "fredokaone-regular.ttf"
)

async def AddMemeCaption(attachment: discord.Attachment, caption: str):
    os.makedirs(Temp_Path, exist_ok=True)

    input_path = os.path.join(
        Temp_Path,
        f"tmp_in_{GetRandomText()}.png"
    )

    output_path = os.path.join(
        Temp_Path,
        f"tmp_out_{GetRandomText()}.jpg"
    )

    await attachment.save(input_path)

    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    caption = caption.replace("\\n", "\n")

    caption_height = int(height * 0.2)
    min_caption_height = caption_height
    font_size = caption_height // 3

    try:
        font = ImageFont.truetype(Fredoka_One, font_size)
    except Exception as e:
        console.warn(f"Error While Loading Fonts As: {e}")
        font = ImageFont.load_default()

    dummy_img = Image.new("RGB", (width, caption_height), "white")
    draw_dummy = ImageDraw.Draw(dummy_img)

    max_text_width = int(width * 0.9)
    lines = wrap_text(caption, font, max_text_width, draw_dummy)

    line_spacing = 6
    line_heights = []
    total_text_height = 0

    for line in lines:
        if line == "":
            h = font_size // 2
        else:
            bbox = draw_dummy.textbbox((0, 0), line, font=font)
            h = bbox[3] - bbox[1]

        line_heights.append(h)
        total_text_height += h + line_spacing

    total_text_height -= line_spacing

    caption_height = max(min_caption_height, total_text_height + 25)

    new_img = Image.new(
        "RGB",
        (width, height + caption_height),
        "white"
    )
    new_img.paste(img, (0, caption_height))

    draw = ImageDraw.Draw(new_img)

    y = (caption_height - total_text_height) // 2

    for i, line in enumerate(lines):
        if line:
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            x = (width - text_width) // 2

            draw.text((x, y), line, fill="black", font=font)

        y += line_heights[i] + line_spacing

    new_img.save(output_path, "JPEG", quality=95)
    os.remove(input_path)

    return output_path