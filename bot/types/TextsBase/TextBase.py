from bot.types.MongoDB.Collections import Chat

Texts = {
    "settings": {
        "choice": {
            "emojis":
                {
                    "on": ["🔧"],
                },
            "langs":
                {
                    "ru": "{} Меню настроек"
                }
        },
        "on_close": {
            "emojis":
                {
                    "on": ""
                },
            "langs":
                {
                    "ru": "Удачно завершено!"
                }
        }
    }
}


async def select_text(chat_id, command, stadia,  lang):
    chat = Chat(chat_id)
    emojis = await chat.get_field_value('emoji_on')
    if emojis:
        text = Texts[command][stadia]["langs"][lang].format(*Texts[command][stadia]["emojis"]["on"])
    else:
        # text = Texts[command][stadia]["langs"][lang].format(*Texts[command][stadia]["emojis"]["off"])
        text = Texts[command][stadia]["langs"][lang].format("")
    return text

# print(select_text(1, "settings", "choice", "ru"))