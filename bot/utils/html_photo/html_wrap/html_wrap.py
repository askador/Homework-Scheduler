def top_block():
    top = \
        """
    <!DOCTYPE html>
    <html lang="ru">
        <head>
          <title>img</title>
            <link rel="stylesheet" type="text/css" href="../html_wrap/main.css">
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

    def __init__(self, class_name="common__row"):
        self.class_name = class_name
        self.elements = []

    def add_element(self, element):
        self.elements.append(element)

    def set_class_name(self, class_name):
        self.class_name = class_name

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

