import logging

from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from config import BOT_TOKEN
from combat import combat_attack, combat_flee, hunt
from explore import enter_location, locked_location, rest, show_explore
from inventory import show_inventory, use_item
from lore import show_lore
from menu import main_menu
from start import choose_class, choose_nation, start
from status import show_status

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def soon_handler(update, context):
    update.callback_query.answer(
        "🚧 Em breve! Ainda estamos construindo esta área.", show_alert=True
    )


def main():
    if not BOT_TOKEN:
        raise SystemExit("Defina BOT_TOKEN no arquivo .env ou nas variáveis de ambiente.")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    # Específicos primeiro
    dp.add_handler(CallbackQueryHandler(choose_nation, pattern=r"^nation_.+$"))
    dp.add_handler(CallbackQueryHandler(choose_class, pattern=r"^class_.+$"))
    dp.add_handler(CallbackQueryHandler(main_menu, pattern=r"^main_menu$"))
    dp.add_handler(CallbackQueryHandler(show_explore, pattern=r"^explore$"))
    dp.add_handler(CallbackQueryHandler(enter_location, pattern=r"^go_.+$"))
    dp.add_handler(CallbackQueryHandler(locked_location, pattern=r"^locked$"))
    dp.add_handler(CallbackQueryHandler(rest, pattern=r"^rest$"))
    dp.add_handler(CallbackQueryHandler(hunt, pattern=r"^hunt$"))
    dp.add_handler(CallbackQueryHandler(combat_attack, pattern=r"^combat_attack$"))
    dp.add_handler(CallbackQueryHandler(combat_flee, pattern=r"^combat_flee$"))
    dp.add_handler(CallbackQueryHandler(show_status, pattern=r"^status$"))
    dp.add_handler(CallbackQueryHandler(show_inventory, pattern=r"^inventory$"))
    dp.add_handler(CallbackQueryHandler(use_item, pattern=r"^itemuse_.+$"))
    dp.add_handler(CallbackQueryHandler(show_lore, pattern=r"^lore$"))

    # Genérico (em breve): sempre por último
    dp.add_handler(CallbackQueryHandler(soon_handler))

    print("✅ Bot rodando!")
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
