from bot.loader import dp
from aiogram.dispatcher import FSMContext
from bot.keyboards import edit_hw_keyboard
from bot.states import GetHomework
from bot.types.MongoDB import Chat, Homework
from bot.utils.methods import clear, update_last


@dp.message_handler(state=GetHomework.description)
async def edit_description(message, state: FSMContext):
    await clear(state)
    await state.update_data(description=message.text)

    chat = Chat(message.chat.id)

    async with state.proxy() as data:
        hw = Homework(chat_id=chat.id, _id=int(data["hw_id"]))
        await chat.update_hw(_id=data["hw_id"], description=data['description'])
        text = "Новое описание: {} \n Выберите что вы хотите отредактировать: ".format(data['description'])
        markup = await edit_hw_keyboard(common=((await hw.get_info(collection='chat', by_id=True))[0]["_id"]["priority"]))

    await update_last(state, await message.reply(text, reply_markup=markup))
    await GetHomework.choice.set()
