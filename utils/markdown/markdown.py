from aiogram.utils.markdown import hide_link as _hide_link


def remove_markdown_entities(text):
    # Защита от не-строковых значений (float/int/None) — сюда могут попасть цены.
    text = str(text)
    entities_list = ['**', '_', '!', '~~', '.', '#', '-', '[', ']', '=', '+', '(', ')']
    for entity in entities_list:
        text = text.replace(entity, "\\" + entity)
    return text


def hide_link(link):
    return _hide_link(url=link)
