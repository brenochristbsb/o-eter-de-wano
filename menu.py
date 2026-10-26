from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.classes import CLASSES
from data.nations import NATIONS
from database import get_player, require_player

KEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("🧭 Explorar", callback_data="explore"),
            InlineKeyboardButton("📊 Status", callback_data="status"),
        ],
        [
            InlineKeyboardButton("🎒 Inventário", callback_data="inventory"),
            InlineKeyboardButton("📜 Lore", callback_data="lore"),
        ],
    ]
)


def render_menu(update, context):
    player = get_player(context)
    nation = NATIONS[player["nation"]]
    cls = CLASSES[player["class"]]
    text = (
        "⚡ <b>O Éter de Wano</b>\n\n"
        f"👤 <b>Nome:</b> {escape(player['name'])}\n"
        f"🏯 <b>Nação:</b> {nation['emoji']} {nation['name']}\n"
        f"⚔️ <b>Classe:</b> {cls['name']}"
    )
    if update.callback_query:
        update.callback_query.edit_message_text(
            text, reply_markup=KEYBOARD, parse_mode=ParseMode.HTML
        )
    else:
        update.effective_message.reply_text(
            text, reply_markup=KEYBOARD, parse_mode=ParseMode.HTML
        )


def main_menu(update, context):
    if not require_player(update, context):
        return
    update.callback_query.answer()
    render_menu(update, context)
