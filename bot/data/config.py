token = '11111111111111:AAAAAAAAAAAAAAAAAAAAAA' #ai4
MAX_CHATS_AMOUNT = 3

mongodb_setting = {
    "User": "user",
    "Password": "password",
    "Host": "host",
    "Database": "db_name",
    "args": "retryWrites=true&w=majority"
}

admins = [
    526497876,
    534794338,
]

materials = "https://drive.google.com/"

commands = {
    'help': "how to use @itai_hw_bot",
    'add_hw': "add new homework",
    'edit_hw': "edit homework",
    'del_hw': "delete homework",
    'show_hws': "show homework this week",
    'settings': "bot settings",
    'cancel': "cancel dialog",
    'my_chat': "your group chat",

}

mongodb_url = f"mongodb+srv://{mongodb_setting['User']}:{mongodb_setting['Password']}@" \
             f"{mongodb_setting['Host']}/{mongodb_setting['Database']}?{mongodb_setting['args']}"
