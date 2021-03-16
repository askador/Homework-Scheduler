
def top_block():
    top = \
        """
    <!DOCTYPE html>
    <html lang="ru">
        <head>
          <title>img</title>
            <link rel="stylesheet" type="text/css" href="main.css">
        </head>
        <body>
           <div class="wrapper">
             <div class="hw">
                <table>
                      <thead>
                         <tr>
                            <th>id</th>
                            <th>Предмет</th>
                            <th>Название работы</th>
                            <th>Описание</th>
                         </tr>
                      </thead>

                      <tbody>
        """
    return top


def bottom_block():
    bottom = \
        """
                        </tbody>
                    </table>
                 </div>
               </div>
            </body>
        </html>
        """

    return bottom


class TRElement:

    def __init__(self, class_name):
        self.class_name = class_name
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def __str__(self):
        obj = f"""<tr class={str(self.class_name)}>\n"""

        for el in self.elements:
            obj += f"   {el}\n"

        obj += """</tr>\n"""

        return obj

    def __repr__(self):
        obj = f"""<tr class={str(self.class_name)}>\n"""

        for el in self.elements:
            obj += f"   {el}\n"

        obj += """</tr>\n"""

        return obj


class TDElement:

    def __init__(self, colspan=1):
        self.colspan = colspan
        self.data = ""

    def insert_data(self, data):
        self.data = data

    def __str__(self):
        obj = f"""<td colspan={self.colspan}>
                    {self.data}
                  </td>
               """
        return obj

    def __repr__(self):
        obj = f"<td colspan={self.colspan}>\n" \
              f"     {self.data}\n" \
              f"   </td>"
        return obj




body = \
    """
                    <tr class="week-day">
                        <td colspan="2">Понедельник</td>
                        <td colspan="2">31.01.2021</td>
                     </tr>
                     <tr class="important row">
                        <td>1</td>
                        <td>ООП</td>
                        <td>Курсовая работа</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>

                     <tr class="week-day">
                        <td class="common week-day" colspan="2">Понедельник</td>
                        <td class="common week-day" colspan="2">01.01.2021</td>
                     </tr>
                     <tr class="common row">
                        <td>1</td>
                        <td>Физика 2пг</td>
                        <td>лаба №1</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                     <tr class="common row">
                        <td>2</td>
                        <td>Англ 1пг</td>
                        <td>тест</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                     <tr class="week-day">
                        <td colspan="2">Вторник</td>
                        <td colspan="2">02.01.2021</td>
                     </tr>
                     <tr class="common row">
                        <td>1</td>
                        <td>ЧМ</td>
                        <td>лаба №2</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                     <tr class="common row">
                        <td>1</td>
                        <td>ЧМ</td>
                        <td>лаба №2</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                      <tr class="common row">
                        <td>1</td>
                        <td>ЧМ</td>
                        <td>лаба №2</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                      <tr class="common row">
                        <td>1</td>
                        <td>ЧМ</td>
                        <td>лаба №2</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>

                    <tr class="week-day">
                        <td colspan="2">Среда</td>
                        <td colspan="2">03.01.2021</td>
                     </tr>
                     <tr class="week-day">
                        <td colspan="2">Четверг</td>
                        <td colspan="2">04.01.2021</td>
                     </tr>

                     <tr class="common week-day">
                        <td class="common week-day" colspan="2">Пятница</td>
                        <td class="common week-day" colspan="2">05.01.2021</td>
                     </tr>
                     <tr class="common row">
                        <td>1</td>
                        <td>Физика 2пг</td>
                        <td>лаба №1</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
                     <tr class="common row">
                        <td>2</td>
                        <td>Англ 1пг</td>
                        <td>тест</td>
                        <td>фывафыцвафывафывафывафыва фыва фыв афыв афыв афыва фыва фыв афыв афыва </td>
                     </tr>
    """
