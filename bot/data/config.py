# token = '1683570768:AAFydK1ItIvQc2soe2LLAqxw9Q1XjcwihDE' #ai4
token = '1482334694:AAH6GzEuYH34ZOwuoXgZttO87lcP9WiH_B8' #shishki
#token = '1173133322:AAG_E7H2IjRypO3dt-pygUjh9V1HP8X8JPk' # test_bot

postgresql_db_setting = {
    "Host": "ec2-34-224-229-81.compute-1.amazonaws.com",
    "Database": "d7kotnui7ubmvq",
    "User": "rjblaxrzxaxpum",
    "Port": "5432",
    "Password": "ea00c427c5ef18079f94af132a47f42fe10ddc81393bdd48ba2c84b708f1a1d1"
}

mongodb_setting = {
    "User": "test_user",
    "Password": "1234",
    "Host": "cluster0.lajfk.mongodb.net",
    "Database": "aiogram_fsm",
    "args": "retryWrites=true&w=majority"
}

mongodb_setting1 = {
    "User": "master",
    "Password": "4321",
    "Host": "chekaimat.aunqh.mongodb.net",
    "Database": "aiogram_fsm",
    "args": "retryWrites=true&w=majority"
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

postresql_db_url = f"postgres://{postgresql_db_setting['User']}:{postgresql_db_setting['Password']}" \
         f"@{postgresql_db_setting['Host']}:{postgresql_db_setting['Port']}/{postgresql_db_setting['Database']}"

#mongodb_url = f"mongodb+srv://{mongodb_setting['User']}:{mongodb_setting['Password']}@" \
#              f"{mongodb_setting['Host']}/{mongodb_setting['Database']}?{mongodb_setting['args']}"

mongodb_url = f"mongodb+srv://{mongodb_setting1['User']}:{mongodb_setting1['Password']}@" \
              f"{mongodb_setting1['Host']}/{mongodb_setting1['Database']}?{mongodb_setting1['args']}"