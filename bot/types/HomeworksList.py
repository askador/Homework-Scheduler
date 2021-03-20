
from pymongo import MongoClient

from datetime import datetime, timedelta
from bot.data import config
from bot.utils.html_photo.html_wrap import top_block, bottom_block, TRElement, TDElement
from bot.utils.html_photo.pyppeteer.pyppeteer import launch


class HomeworksList:
    """
    Create image of homeworks list
    """

    def __init__(self, chat_id, page):
        """

        :param int chat_id: chat id
        :param int page: week page
        """
        self.chat_id = chat_id
        self.page = page
        self.hws = {}
        self.week = []

    async def set_fields(self):
        """
        Get chat homeworks
        """
        self.week = await self._get_week_dates()

        client = MongoClient(config.mongodb_url)
        db = client["hw_bot_db"]
        col = db["chat"]

        homeworks = []

        for x in col.find({"_id": self.chat_id}):
            homeworks = x["homeworks"]

        self.hws = await self._filter_hws(homeworks)

    async def _get_week_dates(self):
        """
        Generating week

        :return list dates: list of week dates
        """
        week_day = datetime.now().isocalendar()[2]
        start_date = datetime.now() - timedelta(days=week_day)
        dates = [(start_date + timedelta(days=i)) for i in range(1 + 7*self.page, 8 + 7*self.page)]
        return dates

    async def _filter_hws(self, hws):
        """
        Filter homeworks by priority and dates

        :param list hws: list of homeworks
        :return list filtered homeworks by date
        """

        filtered_hws = {'important': [],
                        'common': []}

        for hw in hws:
            if self.week[0] <= hw['deadline'] <= self.week[-1] or hw['priority'] == 1:
                """
                Add both filtered by deadline common hw and important hw
                """
                if hw['priority'] != 0:
                    filtered_hws['important'].append(hw)
                else:
                    filtered_hws['common'].append(hw)

        return filtered_hws

    @staticmethod
    async def _date_row(date):
        from datetime import datetime
        tr_day = TRElement(class_name="week-day")

        td_day_name = TDElement(colspan=2)
        td_day_name.insert_data(datetime.strftime(date, "%A"))

        td_date = TDElement(colspan=2)
        td_date.insert_data(datetime.strftime(date, "%d.%m.%y"))

        tr_day.add_element(td_day_name)
        # tr_day.add_element(datetime.strftime(date, "%d.%m.%y"))
        tr_day.add_element(td_date)

        return str(tr_day)

    @staticmethod
    async def _generate_hw_block(class_name, hw):
        tr = TRElement(class_name)

        del hw['deadline']
        del hw['subgroup']
        del hw['priority']
        for field, val in hw.items():
            td = TDElement()
            td.insert_data(val)
            tr.add_element(td)

        return tr

    async def _sort_hws(self, hws, is_important=False):
        sorted_hws = {}
        prefix = ''
        dates = self.week

        if is_important:
            dates = []
            for hw in hws:
                dates.append(hw["deadline"])

            dates = list(set(dates))
            dates.sort()
            prefix = '*'

        for date in dates:
            hws_list = []
            i = 1
            for hw in hws:
                if datetime.isocalendar(hw['deadline']) == datetime.isocalendar(date):
                    hw['_id'] = prefix + str(i)
                    i += 1
                    hws_list.append(hw)
            sorted_hws[date] = hws_list

        return sorted_hws

    async def _generate_body(self):
        body = top_block()

        important_hws = await self._sort_hws(self.hws['important'], True)
        common_hws = await self._sort_hws(self.hws['common'])

        # Generate important elements
        for date, hws in important_hws.items():
            body += await self._date_row(date)
            for hw in hws:
                body += str(await self._generate_hw_block("important__row", hw))

        # Generate important elements
        for date, hws in common_hws.items():
            body += await self._date_row(date)
            for hw in hws:
                body += str(await self._generate_hw_block("common__row", hw))

        body += bottom_block()

        return body

    async def generate_photo(self, html_file, photo_file):

        file = open(html_file, "w")
        file.write(await self._generate_body())
        file.close()

        sourcepath = 'file://' + html_file
        browser = await launch({"args": ['--no-sandbox']})
        page = await browser.newPage()
        await page.goto(sourcepath)
        await page.screenshot({'path': photo_file, 'fullPage': True})
        await browser.close()

        photo = open(photo_file, 'rb')
        # os.remove(_html)
        # os.remove(_photo)
        return photo

        # hw_photo = await generate_png(html_file=html_file, output=photo_file)


