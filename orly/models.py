import os
import re
import hashlib

from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont


def generate_image(title, top_text, author, image_code, theme, guide_text_placement='bottom_right',
                   guide_text='The Definitive Guide'):
    unique_id = title + "_" + top_text + "_" + author + "_" + image_code + "_" + theme + "_" + guide_text_placement + "_" + guide_text
    cache_string = hashlib.md5(unique_id.encode('utf-8')).hexdigest()
    final_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "cache", cache_string + ".png"))

    # Note: Cache is going to miss every time due to deleting it
    if os.path.isfile(cache_string):
        print("Cache hit")
        try:
            return final_path
        except Exception as e:
            print(e.message)
    else:
        print("Cache miss")

    theme_colors = {
        "0": (85, 19, 93, 255),
        "1": (113, 112, 110, 255),
        "2": (128, 27, 42, 255),
        "3": (184, 7, 33, 255),
        "4": (101, 22, 28, 255),
        "5": (80, 61, 189, 255),
        "6": (225, 17, 5, 255),
        "7": (6, 123, 176, 255),
        "8": (247, 181, 0, 255),
        "9": (0, 15, 118, 255),
        "10": (168, 0, 155, 255),
        "11": (0, 132, 69, 255),
        "12": (0, 153, 157, 255),
        "13": (1, 66, 132, 255),
        "14": (177, 0, 52, 255),
        "15": (55, 142, 25, 255),
        "16": (133, 152, 0, 255),
    }
    theme_color = theme_colors[theme]

    width = 500
    height = 700
    im = Image.new('RGBA', (width, height), "white")

    font_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Garamond Light.ttf'))
    font_path_helv = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts', 'HelveticaNeue-Medium.otf'))
    font_path_helv_bold = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Helvetica Bold.ttf'))
    font_path_italic = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Garamond LightItalic.ttf'))

    top_font = ImageFont.truetype(font_path_italic, 20)
    subtitle_font = ImageFont.truetype(font_path_italic, 34)
    author_font = ImageFont.truetype(font_path_italic, 24)
    title_font = ImageFont.truetype(font_path, 62)
    orielly_font = ImageFont.truetype(font_path_helv, 28)
    question_mark_font = ImageFont.truetype(font_path_helv_bold, 16)

    dr = ImageDraw.Draw(im)
    dr.rectangle(((20, 0), (width - 20, 10)), fill=theme_color)

    top_text = sanitize_unicode(top_text, font_path_italic)
    text_width, text_height = dr.textsize(top_text, top_font)
    text_position_x = (width / 2) - (text_width / 2)

    dr.text((text_position_x, 10), top_text, fill='black', font=top_font)

    author = sanitize_unicode(author, font_path_italic)
    text_width, text_height = dr.textsize(author, author_font)
    text_position_x = width - text_width - 20
    text_position_y = height - text_height - 20

    dr.text((text_position_x, text_position_y), author, fill='black', font=author_font)

    oreilly_text = "O RLY"

    text_width, text_height = dr.textsize(oreilly_text, orielly_font)
    text_position_x = 20
    text_position_y = height - text_height - 20

    dr.text((text_position_x, text_position_y), oreilly_text, fill='black', font=orielly_font)

    oreilly_text = "?"

    text_position_x = text_position_x + text_width

    dr.text((text_position_x, text_position_y - 1), oreilly_text, fill=theme_color, font=question_mark_font)

    title_font, new_title = clamp_title_text(sanitize_unicode(title, font_path), width - 80)
    if new_title is None:
        raise ValueError('Title too long')

    text_width, text_height = dr.multiline_textsize(new_title, title_font)
    dr.rectangle([(20, 400), (width - 20, 400 + text_height + 40)], fill=theme_color)

    subtitle = sanitize_unicode(guide_text, font_path_italic)

    if guide_text_placement == 'top_left':
        text_width, text_height = dr.textsize(subtitle, subtitle_font)
        text_position_x = 20
        text_position_y = 400 - text_height - 2
    elif guide_text_placement == 'top_right':
        text_width, text_height = dr.textsize(subtitle, subtitle_font)
        text_position_x = width - 20 - text_width
        text_position_y = 400 - text_height - 2
    elif guide_text_placement == 'bottom_left':
        text_position_y = 400 + text_height + 40
        text_width, text_height = dr.textsize(subtitle, subtitle_font)
        text_position_x = 20
    else:  # bottom_right is default
        text_position_y = 400 + text_height + 40
        text_width, text_height = dr.textsize(subtitle, subtitle_font)
        text_position_x = width - 20 - text_width

    dr.text((text_position_x, text_position_y), subtitle, fill='black', font=subtitle_font)

    dr.multiline_text((40, 420), new_title, fill='white', font=title_font)

    cover_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', ('%s.png' % image_code)))
    cover_image = Image.open(cover_image_path).convert('RGBA')

    offset = (80, 40)
    im.paste(cover_image, offset, cover_image)
    im.save(final_path)
    print(final_path)

    return final_path


def clamp_title_text(title, width):
    im = Image.new('RGBA', (500, 500), "white")
    dr = ImageDraw.Draw(im)

    font_path_italic = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fonts', 'Garamond Light.ttf'))
    # try and fit title on one line
    font = None

    start_font_size = 80
    end_font_size = 61

    for fontSize in range(start_font_size, end_font_size, -1):
        font = ImageFont.truetype(font_path_italic, fontSize)
        w, h = dr.textsize(title, font)

        if w < width:
            return font, title

    # try and fit title on two lines
    start_font_size = 80
    end_font_size = 34

    for fontSize in range(start_font_size, end_font_size, -1):
        font = ImageFont.truetype(font_path_italic, fontSize)

        for match in list(re.finditer('\s', title, re.UNICODE)):
            new_title = u''.join((title[:match.start()], u'\n', title[(match.start() + 1):]))
            substring_width, h = dr.multiline_textsize(new_title, font)

            if substring_width < width:
                return font, new_title

    im.close()

    return None, None


def sanitize_unicode(string, font_file_path):
    sanitized_string = u''

    font = TTFont(font_file_path)
    cmap = font['cmap'].getcmap(3, 1).cmap
    for char in string:
        code_point = ord(char)

        if code_point in cmap.keys():
            sanitized_string += char

    return sanitized_string
