token = '1683570768:AAFydK1ItIvQc2soe2LLAqxw9Q1XjcwihDE' #ai4
# token = '1482334694:AAH6GzEuYH34ZOwuoXgZttO87lcP9WiH_B8' #shishki
test_bot_token = '1173133322:AAG_E7H2IjRypO3dt-pygUjh9V1HP8X8JPk' # test_bot

mongodb_setting = {
    "User": "test_user",
    "Password": "1234",
    "Host": "cluster0.lajfk.mongodb.net",
    "Database": "hw_bot_db",
    "args": "retryWrites=true&w=majority"
}

admins = [
    526497876,
    534794338,
]

materials = "https://drive.google.com/drive/folders/1sirZ5VHO0djffSrOdWcMhMJ30DdSV1zQ?usp=sharing"

commands = {
    'help': "how to use @itai_hw_bot",
    'add_hw': "add new homework",
    'edit_hw': "edit homework",
    'del_hw': "delete homework",
    'show_hws': "show homework this week",
    'cancel': "cancel dialog",
    'settings': "bot settings",

}

mongodb_url = f"mongodb+srv://{mongodb_setting['User']}:{mongodb_setting['Password']}@" \
             f"{mongodb_setting['Host']}/{mongodb_setting['Database']}?{mongodb_setting['args']}"
