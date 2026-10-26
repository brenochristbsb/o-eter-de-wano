from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode

from data.locations import LOCATIONS
from database import require_player, update_player

MENU = [InlineKeyboardButton("🔙 Voltar ao Menu", callback_data="main_menu")]


def _edit(query, text, rows):
    query.edit_message_text(
        text, reply_markup=InlineKeyboardMarkup(rows), parse_mode=ParseMode.HTML
    )


def show_explore(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return
    query.answer()

    rows = []
    for key, loc in LOCATIONS.items():
        min_lvl = loc.get("min_level", 1)
        if player["level"] >= min_lvl:
            rows.append([InlineKeyboardButton(loc["name"], callback_data=f"go_{key}")])
        else:
            rows.append(
                [
                    InlineKeyboardButton(
                        f"🔒 {loc['name']} (Nível {min_lvl})", callback_data="locked"
                    )
                ]
            )
    rows.append(MENU)
    here = LOCATIONS[player["location"]]["name"]
    _edit(query, f"🗺️ <b>Para onde deseja ir?</b>\n\nVocê está em: {here}", rows)


def locked_location(update, context):
    update.callback_query.answer(
        "Você ainda não tem nível suficiente para entrar aqui!", show_alert=True
    )


def enter_location(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return

    loc_key = query.data.split("_", 1)[1]
    loc = LOCATIONS.get(loc_key)
    if not loc:
        query.answer("Local não encontrado!", show_alert=True)
        return
    if player["level"] < loc.get("min_level", 1):
        query.answer("Nível insuficiente para este local.", show_alert=True)
        return

    query.answer()
    context.user_data.pop("enemy", None)
    update_player(context, location=loc_key)

    if loc.get("safe"):
        action = InlineKeyboardButton("💤 Descansar", callback_data="rest")
        text = f"<b>{loc['name']}</b>\n\n{loc['desc']}\n\n✨ Você está em segurança."
    else:
        action = InlineKeyboardButton("🔍 Caçar", callback_data="hunt")
        text = f"<b>{loc['name']}</b>\n\n{loc['desc']}"

    _edit(
        query,
        text,
        [[action], [InlineKeyboardButton("🧭 Mudar de Local", callback_data="explore")], MENU],
    )


def rest(update, context):
    query = update.callback_query
    player = require_player(update, context)
    if not player:
        return

    if not LOCATIONS[player["location"]].get("safe"):
        query.answer("Só é possível descansar em local seguro.", show_alert=True)
        return

    query.answer()
    update_player(context, hp=player["max_hp"], mp=player["max_mp"])
    _edit(
        query,
        "💤 Você descansou e recuperou toda sua vida e mana!",
        [[InlineKeyboardButton("🧭 Explorar", callback_data="explore")], MENU],
    )
