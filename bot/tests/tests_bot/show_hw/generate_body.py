from html_wrap import top_block, body, bottom_block, TDElement, TRElement


def generate_body(data: dict):
    dict = {
        'hws':
                [
                    {
                        '_id': 1,
                        'deadline': '01/01/01',
                        'descr': 'description',
                        'name': 'lab 1',
                    },
                    {
                        '_id': 2,
                        'deadline': '02/01/01',
                        'descr': 'description',
                        'name': 'pz 1',
                    },
                ],
        }

    body = top_block()

    dict = dict['hws']
    for hw in dict:
        tr = TRElement(class_name="common__row")
        for field, val in hw.items():
            td = TDElement()
            td.insert_data(val)
            tr.add_element(td)

        body += str(tr)

    body += bottom_block()

    return body

