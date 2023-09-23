import os

from flask import render_template, request, send_file

from orly import app
from orly.models import generate_image


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/generate", methods=['GET'])
def generate():
    if not request.args:
        message = """
        Bad Request, Try Again
        """

        return message, 401

    try:
        print('generate image')
        body = request.args
        print(body)
        if 'title' in body and 'top_text' in body and 'author' in body and 'image_code' in body and 'theme' in body:
            title = body['title']
            top_text = body['top_text']
            author = body['author']
            image_code = body['image_code']
            theme = body['theme']

            if 'guide_text' in body:
                guide_text = body['guide_text']
            else:
                guide_text = 'The Definitive Guide'

            if 'guide_text_placement' in body:
                guide_text_placement = body['guide_text_placement']
            else:
                guide_text_placement = 'bottom_right'
        else:
            return "Failed: Invalid Params", 401

    except Exception as e:
        print("Unexpected error:", e.message)
        return "Unexpected Error", 500

    try:
        print("generating image")
        final_path = generate_image(title, top_text, author, image_code, theme,
                                    guide_text_placement=guide_text_placement, guide_text=guide_text)
        print("image generated")
        return send_file(final_path, download_name=title + ".png", mimetype='image/png', max_age=604800)  # 604800 is one week in seconds
    except Exception as e:
        print("Unexpected error:", e.message)
        return "Failed", 500
    finally:
        if os.path.isfile(final_path):
            print('removing file')
            os.remove(final_path)


@app.route('/images/<image_code>', methods=['GET'])
def get_image(image_code):
    cover_image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images', ('%s.png' % image_code)))
    return send_file(cover_image_path, mimetype='image/png')
