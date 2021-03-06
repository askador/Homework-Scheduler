from datetime import datetime, timedelta
from bot.utils.HTML_photo.HTML_wrap import top_block, bottom_block, TRElement, TDElement
from bot.utils.HTML_photo.pyppeteer.pyppeteer import launch
from bot.types.MongoDB.Collections import Chat


class HomeworksList:
    """
    Create list of homeworks
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

    async def _get_week_dates(self):
        """
        Generating week

        :return list dates: list of week dates
        """
        week_day = datetime.now().isocalendar()[2]
        start_date = datetime.now() - timedelta(days=week_day)
        dates = [(start_date + timedelta(days=i)).replace(hour=0, minute=0, second=0, microsecond=0) for i in
                 range(1 + 7 * self.page, 8 + 7 * self.page)]
        return dates

    async def set_fields(self):
        """
        Get chat homeworks
        """
        self.week = await self._get_week_dates()

        filters = [
            {"$or": [
                {
                    "homeworks.priority": "important"
                },
                {
                    "$and": [
                        {
                            "homeworks.deadline": {
                                "$gte": self.week[0]
                            }
                        },
                        {
                            "homeworks.deadline": {
                                "$lte": self.week[-1]
                            }
                        }
                    ]
                }
            ]}
        ]

        chat = Chat(self.chat_id)

        homeworks = await chat.get_homeworks(filters=filters)

        self.hws = await self._filter_hws(homeworks)

    @staticmethod
    async def _filter_hws(hws):
        """
        Filter homeworks by priority and dates

        :param list hws: list of homeworks
        :return list filtered homeworks by date
        """

        filtered_hws = {'important': [],
                        'common': []}

        if not hws:
            return filtered_hws

        for hw in hws:
            """
            Add both filtered by deadline common hw and important hw
            """
            if hw["_id"]['priority'] != "common":
                filtered_hws['important'].append(hw["_id"])
            else:
                filtered_hws['common'].append(hw["_id"])

        return filtered_hws

    @staticmethod
    async def _date_row(date):
        """
        Generate date table row

        :param datetime.datetime date: date
        :return html table row
        """
        from datetime import datetime

        week_days = {
            "Monday": "??????????????????????",
            "Tuesday": "??????????????",
            "Wednesday": "??????????",
            "Thursday": "??????????????",
            "Friday": "??????????????",
            "Saturday": "??????????????",
            "Sunday": "??????????????????????",
        }

        tr_day = TRElement(class_name="week-day")

        td_day_name = TDElement(colspan=2)
        td_day_name.insert_data(week_days[datetime.strftime(date, "%A")])

        td_date = TDElement(colspan=2)
        td_date.insert_data(datetime.strftime(date, "%d.%m.%y"))

        tr_day.add_element(td_day_name)
        tr_day.add_element(td_date)

        return str(tr_day)

    @staticmethod
    async def _generate_hw_block(class_name, hw):
        """
        Generate homework data table row

        :param str class_name: div class name
        :param dict hw: homework
        :return html table row
        """
        tr = TRElement(class_name)

        hw_copy = hw.copy()
        del hw['deadline']
        del hw['subgroup']
        del hw['priority']
        for field, val in hw.items():
            td = TDElement()
            if field == 'subject' and hw_copy['subgroup'] != 'any':
                val = str(val) + f" {hw_copy['subgroup']}????."
            td.insert_data(val)
            tr.add_element(td)

        return tr

    async def _sort_hws(self, hws, is_important=False):
        """
        Sorting homeworks by date
        """
        sorted_hws = {}
        prefix = ''
        dates = self.week

        if is_important:
            dates = []
            for hw in hws:
                dates.append(hw["deadline"].replace(hour=0, minute=0, second=0, microsecond=0))

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

    @staticmethod
    async def _check_insert_into_common_week(important_list, common_list):

        imp_list_copy = important_list.copy()
        cmn_list_copy = common_list.copy()

        for date in imp_list_copy.keys():
            if date in cmn_list_copy.keys():
                common_list[date] = common_list[date] + important_list[date]
                del important_list[date]

        return [important_list, common_list]

    async def _generate_body(self):
        """
        Generate html body
        """
        body = top_block()

        important_hws = await self._sort_hws(self.hws['important'], True)
        common_hws = await self._sort_hws(self.hws['common'])

        important_hws, common_hws = await self._check_insert_into_common_week(important_hws, common_hws)

        # Generate important elements
        for date, hws in important_hws.items():
            body += await self._date_row(date)
            for hw in hws:
                body += str(await self._generate_hw_block("important__row", hw))

        # Generate important elements
        for date, hws in common_hws.items():
            body += await self._date_row(date)
            for hw in hws:
                if hw['priority'] == 'important':
                    body += str(await self._generate_hw_block("important__row", hw))
                else:
                    body += str(await self._generate_hw_block("common__row", hw))

        body += bottom_block()

        return body

    @staticmethod
    async def _generate_text_body(hws_list):
        importance = {
            "important": '????????????',
            "common": '??????????????'
        }

        days_of_week = {
            "Monday": "??????????????????????",
            "Tuesday": "??????????????",
            "Wednesday": "??????????",
            "Thursday": "??????????????",
            "Friday": "??????????????",
            "Saturday": "??????????????",
            "Sunday": "??????????????????????"
        }

        text = ""

        for date, hws in hws_list.items():
            text += f"""\n????<b>{days_of_week[datetime.strftime(date, "%A")]} {datetime.strftime(date, "%d.%m.%y")}</b>\n"""
            i = 1
            for hw in hws:
                pin_sign = ''
                if hw['priority'] != "common":
                    pin_sign = "????"
                if hw['subgroup'] != 'any':
                    subj = f"{hw['subject']} {hw['subgroup']}????."
                else:
                    subj = hw['subject']
                text += f"     {pin_sign}???? <b>{i}</b>\n" \
                        f"     ??????????????: {subj}\n" \
                        f"     ????????????????: {hw['name']}\n" \
                        f"     ????????????????????????????: {importance[hw['priority']]}\n"
                if hws.index(hw) + 1 != len(hws):
                    text += "\n"

                i += 1

        return text

    async def generate_text(self):
        """
        Generate homeworks text

        Example:

        ???? Tuesday 18.05.21
             ???????? 1
             ??????????????: ??????
             ????????????????: ????????????????

        ???? Monday 22.03.21
             ???? 1
             ??????????????: ??????????
             ????????????????: ????????

             ???? 1
             ??????????????: ????
             ????????????????: ????????

        """

        await self.set_fields()

        text = ''

        important_hws = await self._sort_hws(self.hws['important'], True)
        common_hws = await self._sort_hws(self.hws['common'])

        # check if pinned hw deadline is in the current week
        important_hws, common_hws = await self._check_insert_into_common_week(important_hws, common_hws)

        # Generate important elements
        text += await self._generate_text_body(important_hws)
        # Generate important elements
        text += await self._generate_text_body(common_hws)

        return text

    async def generate_photo(self, html_file, photo_file):
        """
        Generate homeworks table photo
        """

        await self.set_fields()

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
        return photo
