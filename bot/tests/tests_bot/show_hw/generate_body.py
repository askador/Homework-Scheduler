from html_wrap import top_block, bottom_block, TDElement, TRElement

# Сделать функции ассинхронными


def sort_hws(hws):
    dates = []

    for hw in hws:
        dates.append(hw["deadline"])

    dates = list(set(dates))
    dates.sort()

    hws_dict = {}

    for date in dates:
        hws_list = [hw for hw in hws if hw['deadline'] == date]
        hws_dict[date] = hws_list

    return hws_dict


def date_row(date):
    from datetime import datetime
    tr_day = TRElement(class_name="week-day")

    td_day_name = TDElement(colspan=2)
    td_day_name.insert_data(datetime.strftime(date, "%A"))

    td_date = TDElement(colspan=2)
    td_date.insert_data(date)

    tr_day.add_element(td_day_name)
    tr_day.add_element(td_date)

    return str(tr_day)


def generate_hw_block(class_name, hw):
    tr = TRElement(class_name)

    del hw['deadline']
    del hw['subgroup']
    del hw['priority']
    for field, val in hw.items():
        td = TDElement()
        td.insert_data(val)
        tr.add_element(td)

    return tr


def generate_body(data: list):
    body = top_block()

    important_hws = []
    common_hws = []

    for hw in data:
        if hw['priority'] == 0:
            common_hws.append(hw)
        else:
            important_hws.append(hw)

    important_hws = sort_hws(important_hws)
    common_hws = sort_hws(common_hws)

    # Generate important elements
    for date, hws in important_hws.items():
        body += date_row(date)
        for hw in hws:
            body += str(generate_hw_block("important__row", hw))

    # Generate common elements
    for date, hws in common_hws.items():
        body += date_row(date)

        for hw in hws:
            body += str(generate_hw_block("common__row", hw))

    body += bottom_block()
    return body
