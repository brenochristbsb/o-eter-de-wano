from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.classes import CLASSES
from data.nations import NATIONS

INTRO = (
    "📖 <b>A LENDA DE WANO</b>\n\n"
    "Há muito tempo, o mundo de Wano era envolto em trevas. Forças sombrias "
    "espalhavam medo e caos por todas as terras. Até que um dia, guerreiros "
    "lendários se levantaram, cada um com um poder único, para selar as "
    "trevas e restaurar a paz."
)

WORLD = (
    "🌍 <b>O Mundo:</b>\n"
    "A Vila é seu refúgio seguro. Daqui você pode partir para explorar novas "
    "regiões e enfrentar os desafios que aguardam em cada nação. Seu destino "
    "está em suas mãos, jovem aventureiro. Que as estrelas guiem seu caminho! ✨"
)

KEYBOARD = InlineKeyboardMarkup(
    [[InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="main_menu")]]
)


def show_lore(update, context):
    query = update.callback_query
    query.answer()

    nations = "\n".join(
        f"• {n['emoji']} <b>{n['name']}</b> — {n['description']}"
        for n in NATIONS.values()
    )
    classes = "\n".join(
        f"• <b>{c['name']}</b> — {c['description']}" for c in CLASSES.values()
    )

    text = (
        f"{INTRO}\n\n"
        f"🏔️ <b>As Cinco Nações:</b>\n{nations}\n\n"
        f"⚔️ <b>As Grandes Classes:</b>\n{classes}\n\n"
        f"{WORLD}"
    )
    query.edit_message_text(text, reply_markup=KEYBOARD, parse_mode=ParseMode.HTML)
