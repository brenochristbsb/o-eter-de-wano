from html import escape

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.classes import CLASSES
from data.nations import NATIONS
from database import require_player

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="main_menu")]]
)


def show_status(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return
    query.answer()

    nation = NATIONS[player["nation"]]
    cls = CLASSES[player["class"]]
    xp_next = player["level"] * 100
    filled = min(10, int(player["xp"] / xp_next * 10))
    bar = "█" * filled + "░" * (10 - filled)

    text = (
        f"📊 <b>Status de {escape(player['name'])}</b>\n"
        "─────────────────\n"
        f"🏅 Nível: <b>{player['level']}</b>\n"
        f"✨ XP: {player['xp']}/{xp_next} | {bar}\n"
        f"❤️ Vida: {player['hp']}/{player['max_hp']}\n"
        f"💧 Mana: {player['mp']}/{player['max_mp']}\n"
        f"⚔️ Ataque: {player['attack']}\n"
        f"🛡️ Defesa: {player['defense']}\n"
        f"💰 Ouro: {player['gold']}\n"
        f"🏯 Nação: {nation['emoji']} {nation['name']}\n"
        f"🎭 Classe: {cls['name']}"
    )
    query.edit_message_text(text, reply_markup=KEYBOARD, parse_mode=ParseMode.HTML)
