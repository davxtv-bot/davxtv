#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DavxTV Telegram Bot
✅ Til tanlash: O'zbekcha | Русский | English
✅ Kod yozilsa → film chiqadi
✅ Noto'g'ri kodda — tanlangan tilda xabar
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from database import Database

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ── Config ────────────────────────────────────────────────────────────────────
BOT_TOKEN  = "8635105226:AAGbibuBkOF_Me9ZW7GJmyhp78VILO2L1Cg"
ADMIN_IDS  = [440715427]

db = Database("davxtv.db")

# ══════════════════════════════════════════════════════════════════════════════
#  TARJIMALAR
# ══════════════════════════════════════════════════════════════════════════════

TEXTS = {
    "uz": {
        "welcome": (
            "👋 Salom, <b>{name}</b>!\n\n"
            "🎬 <b>DavxTV</b> ga xush kelibsiz!\n\n"
            "📌 Kinoni topish uchun uning <b>kodini</b> yuboring.\n"
            "Masalan: <code>UZ001</code> yoki <code>TR042</code>\n\n"
            "❓ Kino kodini bilmasangiz — /list buyrug'ini yuboring."
        ),
        "ask_code":    "🎬 Kino kodini yuboring (masalan: <code>UZ001</code>):",
        "not_found":   "❌ <b>{code}</b> kodi bo'yicha kino topilmadi.\n\n✅ To'g'ri kod yuboring.\n📋 Barcha kodlar: /list",
        "category":    "📁 Kategoriya",
        "genre":       "⭐ Janr",
        "year":        "🗓 Yil",
        "lang_label":  "🌐 Til",
        "views":       "👁 Ko'rishlar",
        "code_label":  "🔑 Kod",
        "another":     "🔄 Boshqa kino",
        "no_movies":   "📭 Hozircha kinolar yo'q.",
        "all_movies":  "📋 <b>Barcha kinolar:</b>",
        "new_movies":  "🆕 <b>Yangi qo'shilgan kinolar:</b>",
        "help_text": (
            "📖 <b>Yordam</b>\n\n"
            "🔹 Kino kodini yuboring → film yuklanadi\n"
            "🔹 Kod formati:\n"
            "   • <code>UZ001</code> — O'zbek kino\n"
            "   • <code>TR001</code> — Turk serial\n"
            "   • <code>HN001</code> — Hind kino\n"
            "   • <code>XR001</code> — Xorij kino\n\n"
            "🔹 /start — Bosh menyu\n"
            "🔹 /list  — Barcha kinolar\n"
            "🔹 /new   — Yangi kinolar\n"
            "🔹 /lang  — Tilni o'zgartirish"
        ),
        "cat_empty":   "📭 Bu kategoriyada hozircha kinolar yo'q.",
        "send_code":   "🔑 Kodni yuboring → film ko'ring!",
        "about_text": (
            "ℹ️ <b>DavxTV Bot</b>\n\n"
            "🎬 O'zbek, Turk, Hind va Xorij kinolarini\n"
            "kod orqali toping va to'liq tomosha qiling!\n\n"
            "📲 Kod yuboring → Film yuklanadi!\n"
            "🛠 Admin: @davxtv_admin"
        ),
        "choose_cat":  "📋 <b>Kategoriyani tanlang:</b>",
        "no_admin":    "❌ Sizda admin huquqi yo'q.",
        "lang_changed":"✅ Til o'zgartirildi: O'zbekcha 🇺🇿\n\n🎬 Kino kodini yuboring:",
        "choose_lang": "🌐 Tilni tanlang / Выберите язык / Choose language:",
    },
    "ru": {
        "welcome": (
            "👋 Привет, <b>{name}</b>!\n\n"
            "🎬 Добро пожаловать в <b>DavxTV</b>!\n\n"
            "📌 Отправьте <b>код</b> фильма для поиска.\n"
            "Например: <code>UZ001</code> или <code>TR042</code>\n\n"
            "❓ Не знаете код? Напишите /list"
        ),
        "ask_code":    "🎬 Отправьте код фильма (например: <code>UZ001</code>):",
        "not_found":   "❌ Фильм с кодом <b>{code}</b> не найден.\n\n✅ Введите правильный код.\n📋 Все коды: /list",
        "category":    "📁 Категория",
        "genre":       "⭐ Жанр",
        "year":        "🗓 Год",
        "lang_label":  "🌐 Язык",
        "views":       "👁 Просмотры",
        "code_label":  "🔑 Код",
        "another":     "🔄 Другой фильм",
        "no_movies":   "📭 Фильмов пока нет.",
        "all_movies":  "📋 <b>Все фильмы:</b>",
        "new_movies":  "🆕 <b>Недавно добавленные:</b>",
        "help_text": (
            "📖 <b>Помощь</b>\n\n"
            "🔹 Отправьте код → фильм загрузится\n"
            "🔹 Формат кода:\n"
            "   • <code>UZ001</code> — Узбекский\n"
            "   • <code>TR001</code> — Турецкий\n"
            "   • <code>HN001</code> — Индийский\n"
            "   • <code>XR001</code> — Зарубежный\n\n"
            "🔹 /start — Главное меню\n"
            "🔹 /list  — Все фильмы\n"
            "🔹 /new   — Новые фильмы\n"
            "🔹 /lang  — Сменить язык"
        ),
        "cat_empty":   "📭 В этой категории пока нет фильмов.",
        "send_code":   "🔑 Отправьте код → смотрите фильм!",
        "about_text": (
            "ℹ️ <b>DavxTV Bot</b>\n\n"
            "🎬 Ищите узбекские, турецкие, индийские\n"
            "и зарубежные фильмы по коду!\n\n"
            "📲 Отправьте код → Фильм загрузится!\n"
            "🛠 Admin: @davxtv_admin"
        ),
        "choose_cat":  "📋 <b>Выберите категорию:</b>",
        "no_admin":    "❌ У вас нет прав администратора.",
        "lang_changed":"✅ Язык изменён: Русский 🇷🇺\n\n🎬 Отправьте код фильма:",
        "choose_lang": "🌐 Tilni tanlang / Выберите язык / Choose language:",
    },
    "en": {
        "welcome": (
            "👋 Hello, <b>{name}</b>!\n\n"
            "🎬 Welcome to <b>DavxTV</b>!\n\n"
            "📌 Send the movie <b>code</b> to find it.\n"
            "Example: <code>UZ001</code> or <code>TR042</code>\n\n"
            "❓ Don't know the code? Use /list"
        ),
        "ask_code":    "🎬 Send the movie code (e.g. <code>UZ001</code>):",
        "not_found":   "❌ Movie with code <b>{code}</b> not found.\n\n✅ Send a valid code.\n📋 All codes: /list",
        "category":    "📁 Category",
        "genre":       "⭐ Genre",
        "year":        "🗓 Year",
        "lang_label":  "🌐 Language",
        "views":       "👁 Views",
        "code_label":  "🔑 Code",
        "another":     "🔄 Another movie",
        "no_movies":   "📭 No movies yet.",
        "all_movies":  "📋 <b>All movies:</b>",
        "new_movies":  "🆕 <b>Recently added:</b>",
        "help_text": (
            "📖 <b>Help</b>\n\n"
            "🔹 Send a code → movie loads\n"
            "🔹 Code format:\n"
            "   • <code>UZ001</code> — Uzbek movie\n"
            "   • <code>TR001</code> — Turkish series\n"
            "   • <code>HN001</code> — Indian movie\n"
            "   • <code>XR001</code> — Foreign movie\n\n"
            "🔹 /start — Main menu\n"
            "🔹 /list  — All movies\n"
            "🔹 /new   — New movies\n"
            "🔹 /lang  — Change language"
        ),
        "cat_empty":   "📭 No movies in this category yet.",
        "send_code":   "🔑 Send code → watch movie!",
        "about_text": (
            "ℹ️ <b>DavxTV Bot</b>\n\n"
            "🎬 Find Uzbek, Turkish, Indian\n"
            "and Foreign movies by code!\n\n"
            "📲 Send code → Movie loads!\n"
            "🛠 Admin: @davxtv_admin"
        ),
        "choose_cat":  "📋 <b>Choose a category:</b>",
        "no_admin":    "❌ You don't have admin rights.",
        "lang_changed":"✅ Language changed: English 🇬🇧\n\n🎬 Send movie code:",
        "choose_lang": "🌐 Tilni tanlang / Выберите язык / Choose language:",
    },
}

CAT_LABELS = {
    "uz": {"UZ": "🇺🇿 O'zbek",     "TR": "🇹🇷 Turk",       "HN": "🇮🇳 Hind",    "XR": "🌍 Xorij"},
    "ru": {"UZ": "🇺🇿 Узбекский",  "TR": "🇹🇷 Турецкий",   "HN": "🇮🇳 Индийский","XR": "🌍 Зарубежный"},
    "en": {"UZ": "🇺🇿 Uzbek",      "TR": "🇹🇷 Turkish",     "HN": "🇮🇳 Indian",   "XR": "🌍 Foreign"},
}

# ── Yordamchi funksiyalar ─────────────────────────────────────────────────────
def get_lang(ctx: ContextTypes.DEFAULT_TYPE) -> str:
    return ctx.user_data.get("lang", "uz")

def t(ctx, key, **kwargs):
    lang = get_lang(ctx)
    text = TEXTS[lang].get(key, TEXTS["uz"].get(key, ""))
    return text.format(**kwargs) if kwargs else text

def lang_keyboard():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="setlang_uz"),
        InlineKeyboardButton("🇷🇺 Русский",   callback_data="setlang_ru"),
        InlineKeyboardButton("🇬🇧 English",   callback_data="setlang_en"),
    ]])

# ══════════════════════════════════════════════════════════════════════════════
#  /start — Til tanlash → Bosh menyu
# ══════════════════════════════════════════════════════════════════════════════

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username or "", user.first_name or "")

    if "lang" in ctx.user_data:
        await _show_main_menu(update, ctx)
    else:
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=lang_keyboard(),
        )


async def _show_main_menu(update_or_msg, ctx, from_callback=False):
    lang    = get_lang(ctx)
    cl      = CAT_LABELS[lang]
    user    = update_or_msg.effective_user if not from_callback else None

    keyboard = [
        [
            InlineKeyboardButton(cl["UZ"], callback_data="cat_UZ"),
            InlineKeyboardButton(cl["TR"], callback_data="cat_TR"),
        ],
        [
            InlineKeyboardButton(cl["HN"], callback_data="cat_HN"),
            InlineKeyboardButton(cl["XR"], callback_data="cat_XR"),
        ],
        [
            InlineKeyboardButton("ℹ️ Haqida / About", callback_data="about"),
            InlineKeyboardButton("🌐 Til / Lang",      callback_data="change_lang"),
        ],
    ]

    name = update_or_msg.effective_user.first_name if hasattr(update_or_msg, "effective_user") else "User"
    text = t(ctx, "welcome", name=name)

    if from_callback:
        await update_or_msg.callback_query.message.reply_text(
            text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await update_or_msg.message.reply_text(
            text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(keyboard)
        )

# ══════════════════════════════════════════════════════════════════════════════
#  BUYRUQLAR
# ══════════════════════════════════════════════════════════════════════════════

async def choose_language(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(t(ctx, "choose_lang"), reply_markup=lang_keyboard())


async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(t(ctx, "help_text"), parse_mode="HTML")


async def list_movies(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    movies = db.get_all_movies()
    if not movies:
        await update.message.reply_text(t(ctx, "no_movies"))
        return
    lang = get_lang(ctx)
    cl   = CAT_LABELS[lang]
    cats = {}
    for m in movies:
        cats.setdefault(m["category"], []).append(m)
    lines = [t(ctx, "all_movies") + "\n"]
    for cat in ["UZ", "TR", "HN", "XR"]:
        if cat in cats:
            lines.append(f"\n{cl[cat]}:")
            for m in cats[cat]:
                lines.append(f"  📽 <code>{m['code']}</code> — {m['title']}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


async def new_movies(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    movies = db.get_recent_movies(10)
    if not movies:
        await update.message.reply_text(t(ctx, "no_movies"))
        return
    lines = [t(ctx, "new_movies") + "\n"]
    for m in movies:
        lines.append(f"📽 <code>{m['code']}</code> — {m['title']}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")


# ══════════════════════════════════════════════════════════════════════════════
#  KOD YOZILGANDA → FILM YUBORISH
# ══════════════════════════════════════════════════════════════════════════════

async def handle_code(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if "lang" not in ctx.user_data:
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=lang_keyboard(),
        )
        return

    raw   = update.message.text.strip().upper()
    movie = db.get_movie_by_code(raw)

    if not movie:
        await update.message.reply_text(t(ctx, "not_found", code=raw), parse_mode="HTML")
        return

    db.increment_views(movie["code"])
    lang = get_lang(ctx)
    cl   = CAT_LABELS[lang]

    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"{t(ctx,'category')}: {cl.get(movie['category'], movie['category_label'])}\n"
        f"{t(ctx,'genre')}: {movie['genre']}\n"
        f"{t(ctx,'year')}: {movie['year']}\n"
        f"{t(ctx,'lang_label')}: {movie['language']}\n\n"
        f"{t(ctx,'views')}: {movie['views'] + 1}\n"
        f"{t(ctx,'code_label')}: <code>{movie['code']}</code>"
    )

    keyboard = [[InlineKeyboardButton(t(ctx, "another"), callback_data="ask_code")]]

    await update.message.reply_video(
        video=movie["file_id"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


# ══════════════════════════════════════════════════════════════════════════════
#  CALLBACK HANDLER
# ══════════════════════════════════════════════════════════════════════════════

async def callback_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    await q.answer()

    # ── TIL O'RNATISH ────────────────────────────────────────────────────────
    if data.startswith("setlang_"):
        lang = data[8:]                    # uz / ru / en
        ctx.user_data["lang"] = lang
        await q.message.reply_text(TEXTS[lang]["lang_changed"], parse_mode="HTML")
        return

    # ── TIL ALMASHTIRISH ─────────────────────────────────────────────────────
    if data == "change_lang":
        await q.message.reply_text(t(ctx, "choose_lang"), reply_markup=lang_keyboard())
        return

    # ── KOD SO'RASH ──────────────────────────────────────────────────────────
    if data == "ask_code":
        await q.message.reply_text(t(ctx, "ask_code"), parse_mode="HTML")
        return

    # ── KATEGORIYA ───────────────────────────────────────────────────────────
    if data.startswith("cat_"):
        cat    = data[4:]
        movies = db.get_movies_by_category(cat)
        lang   = get_lang(ctx)
        cl     = CAT_LABELS[lang]
        if not movies:
            await q.message.reply_text(t(ctx, "cat_empty"))
            return
        lines = [f"📋 <b>{cl.get(cat, cat)}:</b>\n"]
        for m in movies:
            lines.append(f"📽 <code>{m['code']}</code> — {m['title']}")
        lines.append(f"\n{t(ctx, 'send_code')}")
        await q.message.reply_text("\n".join(lines), parse_mode="HTML")
        return

    # ── HAQIDA ───────────────────────────────────────────────────────────────
    if data == "about":
        await q.message.reply_text(t(ctx, "about_text"), parse_mode="HTML")
        return

    # ── ADMIN CALLBACK ───────────────────────────────────────────────────────
    if data.startswith("adm_") and update.effective_user.id in ADMIN_IDS:
        s = db.get_stats()
        if data == "adm_stat":
            await q.message.reply_text(
                f"📊 Users: {s['users']}\n🎬 Movies: {s['movies']}\n👁 Views: {s['views']}"
            )
        elif data == "adm_users":
            await q.message.reply_text(f"👥 Total users: {len(db.get_all_users())}")
        elif data == "adm_add":
            await q.message.reply_text(
                "➕ <code>/add KOD | Sarlavha | Kategoriya | Janr | Yil | Til | file_id</code>",
                parse_mode="HTML",
            )
        elif data == "adm_del":
            await q.message.reply_text("🗑 <code>/del KOD</code>", parse_mode="HTML")
        return


# ══════════════════════════════════════════════════════════════════════════════
#  ADMIN BUYRUQLARI
# ══════════════════════════════════════════════════════════════════════════════

async def admin_panel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        await update.message.reply_text(t(ctx, "no_admin"))
        return
    keyboard = [
        [InlineKeyboardButton("➕ Kino qo'shish",   callback_data="adm_add")],
        [InlineKeyboardButton("🗑 Kino o'chirish",  callback_data="adm_del")],
        [InlineKeyboardButton("📊 Statistika",       callback_data="adm_stat")],
        [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="adm_users")],
    ]
    await update.message.reply_text(
        "🛠 <b>Admin Panel</b>", parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def add_movie(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text(
            "📝 Format:\n"
            "<code>/add KOD | Sarlavha | Kategoriya | Janr | Yil | Til | file_id</code>\n\n"
            "Kategoriya: UZ TR HN XR\n\n"
            "Misol:\n"
            "<code>/add UZ001 | Alpomish | UZ | Drama | 2023 | O'zbek | AgACAgIA...</code>",
            parse_mode="HTML",
        )
        return
    parts = " ".join(ctx.args).split("|")
    if len(parts) != 7:
        await update.message.reply_text("❌ 7 ta qism kerak! | bilan ajrating.")
        return
    code, title, cat, genre, year, lang, file_id = [p.strip() for p in parts]
    cat = cat.upper()
    cat_labels = {"UZ": "🇺🇿 O'zbek", "TR": "🇹🇷 Turk", "HN": "🇮🇳 Hind", "XR": "🌍 Xorij"}
    if cat not in cat_labels:
        await update.message.reply_text("❌ Kategoriya: UZ, TR, HN yoki XR bo'lishi kerak.")
        return
    ok = db.add_movie(code.upper(), title, cat, cat_labels[cat], genre, year, lang, file_id)
    if ok:
        await update.message.reply_text(
            f"✅ <b>{title}</b> (<code>{code.upper()}</code>) qo'shildi!", parse_mode="HTML"
        )
    else:
        await update.message.reply_text(
            f"❌ <code>{code.upper()}</code> allaqachon mavjud!", parse_mode="HTML"
        )


async def del_movie(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text("Format: <code>/del KOD</code>", parse_mode="HTML")
        return
    code = ctx.args[0].upper()
    ok   = db.delete_movie(code)
    if ok:
        await update.message.reply_text(f"🗑 <code>{code}</code> o'chirildi.", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ <code>{code}</code> topilmadi.", parse_mode="HTML")


async def stats(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    s    = db.get_stats()
    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{s['users']}</b>\n"
        f"🎬 Kinolar: <b>{s['movies']}</b>\n"
        f"👁 Ko'rishlar: <b>{s['views']}</b>\n\n"
        "🏆 Top 5:\n"
    )
    for m in s["top"]:
        text += f"  • <code>{m['code']}</code> — {m['title']} ({m['views']} 👁)\n"
    await update.message.reply_text(text, parse_mode="HTML")


async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text("Format: <code>/broadcast Xabar</code>", parse_mode="HTML")
        return
    msg    = " ".join(ctx.args)
    users  = db.get_all_users()
    sent   = 0
    failed = 0
    sm     = await update.message.reply_text(f"📤 0/{len(users)}")
    for i, user in enumerate(users):
        try:
            await ctx.bot.send_message(chat_id=user["user_id"], text=msg, parse_mode="HTML")
            sent += 1
        except Exception:
            failed += 1
        if (i + 1) % 20 == 0:
            await sm.edit_text(f"📤 {i+1}/{len(users)}")
    await sm.edit_text(f"✅ Yuborildi: {sent}\n❌ Xato: {failed}")


# ══════════════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("help",      help_cmd))
    app.add_handler(CommandHandler("list",      list_movies))
    app.add_handler(CommandHandler("new",       new_movies))
    app.add_handler(CommandHandler("lang",      choose_language))
    app.add_handler(CommandHandler("admin",     admin_panel))
    app.add_handler(CommandHandler("add",       add_movie))
    app.add_handler(CommandHandler("del",       del_movie))
    app.add_handler(CommandHandler("stats",     stats))
    app.add_handler(CommandHandler("broadcast", broadcast))

    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    logger.info("🚀 DavxTV bot ishga tushdi! (O'zbekcha | Русский | English)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()