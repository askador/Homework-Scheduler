from bot.types.MongoDB.Collections import Chat

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


async def select_text(chat_id, command, stadia,  lang):
    chat = Chat(chat_id)
    emojis = await chat.get_field_value('emoji_on')
    if emojis:
        text = Texts[command][stadia]["langs"][lang].format(*Texts[command][stadia]["emojis"]["on"])
    else:
        text = Texts[command][stadia]["langs"][lang].format(*Texts[command][stadia]["emojis"]["off"])
    return text

# print(select_text(1, "settings", "choice", "ru"))