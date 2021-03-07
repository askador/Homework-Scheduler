class Column:

    def __init__(self, title, type, *, primary_key=False, not_null=False, unique=False,
                 unsigned=False, serial=False, default=None):

        self.title = title
        self.type = type
        self.primary_key = primary_key
        self.not_null = not_null
        self.unique = unique
        self.unsigned = unsigned
        self.serial = serial
        self.default = default

    def create_column(self):
        column = f"{self.title} {self.type} "

        for key in self.__dict__.keys():
            if self.__dict__[key] and key != "title" and key != "type":
                if key == "primary_key":
                    column += f"primary key "
                elif key == "not_null":
                    column += f"not null "
                elif key == "default":
                    column += f"default({self.default}) "
                else:
                    column += f"{key} "

        column += ","
        return column

    def __repr__(self):
        return self.create_column()
