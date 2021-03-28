from datetime import datetime
import os


def get_files_paths(chat_id):
    html_file = f"{datetime.timestamp(datetime.now())}_{chat_id}.html"
    photo_file = f"{datetime.timestamp(datetime.now())}_{str(chat_id)}.png"

    script_dir = os.path.dirname(__file__)
    script_dir = "/".join(script_dir.split('/')[:script_dir.split('\\').index("bot") + 1])

    script_dir = script_dir + "/utils/HTML_photo/temp_photo/"

    html_path = script_dir + html_file
    photo_path = script_dir + f"/utils/HTML_photo/temp_photo/{photo_file}"

    return html_path, photo_path

