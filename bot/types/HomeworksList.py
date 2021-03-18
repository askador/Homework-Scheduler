from datetime import datetime, timedelta
from bot.utils.methods.generate_body import generate_body


class HomeworksList:
    """
    Create image of homeworks list
    """

    def __init__(self, hws):
        self.hws = hws

    @staticmethod
    def _get_current_week():
        week_day = datetime.now().isocalendar()[2]
        start_date = datetime.now() - timedelta(days=week_day)
        dates = [(start_date + timedelta(days=i)) for i in range(1, 8)]

        return dates

    def _filter_hws(self):
        pass

    def generate_photo(self, html_file, photo_file):
        pass

