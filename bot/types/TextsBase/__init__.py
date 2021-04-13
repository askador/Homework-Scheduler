

Texts = {
    "settings": {
        "choice": {
            "emojis":
                {
                    "on": ["🔧"],
                    "off": [""]
                },
            "langs":
                {
                    "ru": "{} Меню настроек"
                }
        }
    }
}


def select_text(chat_id, command, stadia,  lang):
    text = Texts[command][stadia]["langs"][lang].format(emoji for emoji in Texts[command][stadia]["emojis"]["on"])
    return text


print(select_text(1, "settings", "choice", "ru"))
