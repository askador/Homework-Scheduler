token = '1482334694:AAH6GzEuYH34ZOwuoXgZttO87lcP9WiH_B8'

db_setting = {
    "Host": "ec2-46-137-124-19.eu-west-1.compute.amazonaws.com",
    "Database": "d52aadfi1esdet",
    "User": "puiejcfigqodwu",
    "Port": "5432",
    "Password": "4ec39612794d480bd8253264273e0e902a35b552c1d4ea809f0b7b720f84d6db"
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

db = f"postgres://{db_setting['User']}:{db_setting['Password']}@{db_setting['Host']}:{db_setting['Port']}/{db_setting['Database']}"