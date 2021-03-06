token = '1482334694:AAH6GzEuYH34ZOwuoXgZttO87lcP9WiH_B8'

db_setting = {
    "Host": "ec2-34-224-229-81.compute-1.amazonaws.com",
    "Database": "d7kotnui7ubmvq",
    "User": "rjblaxrzxaxpum",
    "Port": "5432",
    "Password": "ea00c427c5ef18079f94af132a47f42fe10ddc81393bdd48ba2c84b708f1a1d1"
}

admins = [
    526497876,
    534794338,
]

materials = "https://drive.google.com/drive/folders/1sirZ5VHO0djffSrOdWcMhMJ30DdSV1zQ?usp=sharing"

commands = {
    '/start': "",
    '/help': "",
}

db_url = f"postgres://{db_setting['User']}:{db_setting['Password']}@{db_setting['Host']}:{db_setting['Port']}/{db_setting['Database']}"