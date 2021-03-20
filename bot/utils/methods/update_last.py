async def update_last(state, sent):
    await state.update_data(last_message_id=sent.message_id)