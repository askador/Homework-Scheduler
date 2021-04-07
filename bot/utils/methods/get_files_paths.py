from datetime import datetime
import os


def get_files_paths(chat_id):
    html_file = f"{datetime.timestamp(datetime.now())}_{chat_id}.html"
    photo_file = f"{datetime.timestamp(datetime.now())}_{str(chat_id)}.png"

    script_dir = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'HTML_photo', 'temp_photo'))

    html_path = os.path.join(script_dir, html_file)
    photo_path = os.path.join(script_dir, photo_file)

    return html_path, photo_path

