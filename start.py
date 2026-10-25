from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.classes import CLASSES
from data.nations import NATIONS
from database import get_player
from handlers.menu import render_menu


def start(update, context):
    if get_player(context):
        render_menu(update, context)
        return

    name = escape(update.effective_user.first_name or "Viajante")
    nations = "\n".join(
        f"{n['emoji']} <b>{n['name']}</b> — {n['description']}"
        for n in NATIONS.values()
    )
    rows = [
        [InlineKeyboardButton(f"{n['emoji']} {n['name']}", callback_data=f"nation_{k}")]
        for k, n in NATIONS.items()
    ]
    update.message.reply_text(
        f"⚡ <b>O Éter de Wano</b>\n\nBem-vindo, <b>{name}</b>.\n"
        f"Escolha sua nação:\n\n{nations}",
        reply_markup=InlineKeyboardMarkup(rows),
        parse_mode=ParseMode.HTML,
    )


def choose_nation(update, context):
    query = update.callback_query
    query.answer()

    if get_player(context):
        render_menu(update, context)
        return

    nation_key = query.data.split("_", 1)[1]
    if nation_key not in NATIONS:
        return

    nation = NATIONS[nation_key]
    classes = "\n".join(
        f"• <b>{c['name']}</b> — {c['description']}" for c in CLASSES.values()
    )
    buttons = [
        InlineKeyboardButton(c["name"], callback_data=f"class_{nation_key}_{k}")
        for k, c in CLASSES.items()
    ]
    rows = [buttons[i : i + 2] for i in range(0, len(buttons), 2)]
    query.edit_message_text(
        f"{nation['emoji']} <b>{nation['name']}</b>\n\n"
        f"Agora escolha sua classe:\n\n{classes}",
        reply_markup=InlineKeyboardMarkup(rows),
        parse_mode=ParseMode.HTML,
    )


def choose_class(update, context):
    query = update.callback_query
    query.answer()

    if get_player(context):
        render_menu(update, context)
        return

    _, nation_key, class_key = query.data.split("_", 2)
    if nation_key not in NATIONS or class_key not in CLASSES:
        return

    stats = CLASSES[class_key]["base_stats"]
    context.user_data["player"] = {
        "name": update.effective_user.first_name or "Aventureiro",
        "nation": nation_key,
        "class": class_key,
        "level": 1,
        "xp": 0,
        "hp": stats["max_hp"],
        "max_hp": stats["max_hp"],
        "mp": stats["max_mp"],
        "max_mp": stats["max_mp"],
        "attack": stats["attack"],
        "defense": stats["defense"],
        "gold": 50,
        "location": "vila",
        "inventory": {"pocao_vida": 2, "pocao_mana": 1},
    }
    render_menu(update, context)
