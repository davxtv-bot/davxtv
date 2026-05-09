#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DavxTV Telegram Bot  v2.0
- Til DB da saqlanadi (restart da ham esda qoladi)
- Barqaror ishlaydi
- Kino qo'shish oson
"""

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters,
)
from database import Database

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════
BOT_TOKEN = "8635105226:AAGbibuBkOF_Me9ZW7GJmyhp78VILO2L1Cg"
ADMIN_IDS = [440715427]
# ═══════════════════════════════════════════

db = Database("davxtv.db")

# ──────────────────────────────────────────
#  MATNLAR (3 til)
# ──────────────────────────────────────────
T = {
    "uz": {
        "select_lang": "🌐 Tilni tanlang:",
        "lang_set":    "✅ Til: O'zbekcha 🇺🇿",
        "welcome":     "👋 Salom <b>{n}</b>! DavxTV ga xush kelibsiz 🎬\n\n📌 Kino <b>kodini</b> yuboring.\nMasalan: <code>UZ001</code>\n\n/list — barcha kinolar\n/new  — yangi kinolar\n/lang — tilni o'zgartirish",
        "enter_code":  "🔑 Kino kodini yuboring (masalan: <code>UZ001</code>):",
        "not_found":   "❌ <b>{c}</b> — bunday kod topilmadi.\n\n📋 Barcha kodlar: /list",
        "cat":         "📁 Kategoriya",
        "genre":       "⭐ Janr",
        "year":        "🗓 Yil",
        "lang_f":      "🌐 Til",
        "views":       "👁 Ko'rishlar",
        "code_l":      "🔑 Kod",
        "another":     "🔄 Boshqa kino",
        "no_films":    "📭 Hozircha kinolar yo'q.",
        "all_films":   "📋 <b>Barcha kinolar:</b>",
        "new_films":   "🆕 <b>Yangi kinolar:</b>",
        "no_cat":      "📭 Bu kategoriyada kino yo'q.",
        "see_code":    "👆 Kodini yuboring → film ko'ring!",
        "about":       "ℹ️ <b>DavxTV</b> — kino kodi yuboring, to'liq film oling! 🎬\n\nAdmin: @davxtv_admin",
        "no_right":    "❌ Admin huquqi yo'q.",
        "choose_cat":  "📋 Kategoriyani tanlang:",
        "help": (
            "📖 <b>Yordam:</b>\n\n"
            "🔹 Kod yuboring → film yuklanadi\n"
            "🔹 /list — barcha kinolar\n"
            "🔹 /new  — yangi kinolar\n"
            "🔹 /lang — tilni o'zgartirish\n\n"
            "📌 Kod formati:\n"
            "   <code>UZ001</code> — O'zbek kino\n"
            "   <code>TR001</code> — Turk serial\n"
            "   <code>HN001</code> — Hind kino\n"
            "   <code>XR001</code> — Xorij kino"
        ),
    },
    "ru": {
        "select_lang": "🌐 Выберите язык:",
        "lang_set":    "✅ Язык: Русский 🇷🇺",
        "welcome":     "👋 Привет <b>{n}</b>! Добро пожаловать в DavxTV 🎬\n\n📌 Отправьте <b>код</b> фильма.\nНапример: <code>UZ001</code>\n\n/list — все фильмы\n/new  — новые фильмы\n/lang — сменить язык",
        "enter_code":  "🔑 Отправьте код фильма (например: <code>UZ001</code>):",
        "not_found":   "❌ <b>{c}</b> — такой код не найден.\n\n📋 Все коды: /list",
        "cat":         "📁 Категория",
        "genre":       "⭐ Жанр",
        "year":        "🗓 Год",
        "lang_f":      "🌐 Язык",
        "views":       "👁 Просмотры",
        "code_l":      "🔑 Код",
        "another":     "🔄 Другой фильм",
        "no_films":    "📭 Фильмов пока нет.",
        "all_films":   "📋 <b>Все фильмы:</b>",
        "new_films":   "🆕 <b>Новые фильмы:</b>",
        "no_cat":      "📭 В этой категории нет фильмов.",
        "see_code":    "👆 Отправьте код → смотрите фильм!",
        "about":       "ℹ️ <b>DavxTV</b> — отправьте код, получите фильм! 🎬\n\nAdmin: @davxtv_admin",
        "no_right":    "❌ Нет прав администратора.",
        "choose_cat":  "📋 Выберите категорию:",
        "help": (
            "📖 <b>Помощь:</b>\n\n"
            "🔹 Код → фильм загружается\n"
            "🔹 /list — все фильмы\n"
            "🔹 /new  — новые фильмы\n"
            "🔹 /lang — сменить язык\n\n"
            "📌 Формат кода:\n"
            "   <code>UZ001</code> — Узбекский\n"
            "   <code>TR001</code> — Турецкий\n"
            "   <code>HN001</code> — Индийский\n"
            "   <code>XR001</code> — Зарубежный"
        ),
    },
    "en": {
        "select_lang": "🌐 Choose language:",
        "lang_set":    "✅ Language: English 🇬🇧",
        "welcome":     "👋 Hello <b>{n}</b>! Welcome to DavxTV 🎬\n\n📌 Send the movie <b>code</b>.\nExample: <code>UZ001</code>\n\n/list — all movies\n/new  — new movies\n/lang — change language",
        "enter_code":  "🔑 Send movie code (e.g. <code>UZ001</code>):",
        "not_found":   "❌ <b>{c}</b> — code not found.\n\n📋 All codes: /list",
        "cat":         "📁 Category",
        "genre":       "⭐ Genre",
        "year":        "🗓 Year",
        "lang_f":      "🌐 Language",
        "views":       "👁 Views",
        "code_l":      "🔑 Code",
        "another":     "🔄 Another movie",
        "no_films":    "📭 No movies yet.",
        "all_films":   "📋 <b>All movies:</b>",
        "new_films":   "🆕 <b>New movies:</b>",
        "no_cat":      "📭 No movies in this category.",
        "see_code":    "👆 Send code → watch movie!",
        "about":       "ℹ️ <b>DavxTV</b> — send code, get full movie! 🎬\n\nAdmin: @davxtv_admin",
        "no_right":    "❌ No admin rights.",
        "choose_cat":  "📋 Choose category:",
        "help": (
            "📖 <b>Help:</b>\n\n"
            "🔹 Send code → movie loads\n"
            "🔹 /list — all movies\n"
            "🔹 /new  — new movies\n"
            "🔹 /lang — change language\n\n"
            "📌 Code format:\n"
            "   <code>UZ001</code> — Uzbek\n"
            "   <code>TR001</code> — Turkish\n"
            "   <code>HN001</code> — Indian\n"
            "   <code>XR001</code> — Foreign"
        ),
    },
}

CATS = {
    "uz": {"UZ": "🇺🇿 O'zbek", "TR": "🇹🇷 Turk", "HN": "🇮🇳 Hind", "XR": "🌍 Xorij"},
    "ru": {"UZ": "🇺🇿 Узбекский", "TR": "🇹🇷 Турецкий", "HN": "🇮🇳 Индийский", "XR": "🌍 Зарубежный"},
    "en": {"UZ": "🇺🇿 Uzbek", "TR": "🇹🇷 Turkish", "HN": "🇮🇳 Indian", "XR": "🌍 Foreign"},
}

# ──────────────────────────────────────────
#  YORDAMCHI FUNKSIYALAR
# ──────────────────────────────────────────
def get_lang(uid):
    """DB dan tilni oladi. Agar yo'q bo'lsa None qaytaradi."""
    return db.get_user_lang(uid)

def tx(uid, key, **kw):
    """Foydalanuvchi tilidagi matn."""
    lang = get_lang(uid) or "uz"
    text = T[lang].get(key, T["uz"].get(key, ""))
    return text.format(**kw) if kw else text

def lang_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский",   callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English",   callback_data="lang_en"),
    ]])

def main_kb(uid):
    lang = get_lang(uid) or "uz"
    cl   = CATS[lang]
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(cl["UZ"], callback_data="cat_UZ"),
            InlineKeyboardButton(cl["TR"], callback_data="cat_TR"),
        ],
        [
            InlineKeyboardButton(cl["HN"], callback_data="cat_HN"),
            InlineKeyboardButton(cl["XR"], callback_data="cat_XR"),
        ],
        [
            InlineKeyboardButton("ℹ️ Haqida", callback_data="about"),
            InlineKeyboardButton("🌐 Til",    callback_data="change_lang"),
        ],
    ])

# ──────────────────────────────────────────
#  /start
# ──────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username or "", user.first_name or "")

    lang = get_lang(user.id)
    if lang is None:
        # Birinchi marta: til tanlash
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=lang_kb(),
        )
    else:
        await update.message.reply_text(
            tx(user.id, "welcome", n=user.first_name),
            parse_mode="HTML",
            reply_markup=main_kb(user.id),
        )

# ──────────────────────────────────────────
#  /lang
# ──────────────────────────────────────────
async def lang_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Tilni tanlang / Выберите язык / Choose language:",
        reply_markup=lang_kb(),
    )

# ──────────────────────────────────────────
#  /help
# ──────────────────────────────────────────
async def help_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        tx(update.effective_user.id, "help"),
        parse_mode="HTML",
    )

# ──────────────────────────────────────────
#  /list
# ──────────────────────────────────────────
async def list_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid    = update.effective_user.id
    movies = db.get_all_movies()
    if not movies:
        await update.message.reply_text(tx(uid, "no_films"))
        return
    lang = get_lang(uid) or "uz"
    cl   = CATS[lang]
    cats = {}
    for m in movies:
        cats.setdefault(m["category"], []).append(m)
    lines = [tx(uid, "all_films") + "\n"]
    for cat in ["UZ", "TR", "HN", "XR"]:
        if cat in cats:
            lines.append(f"\n{cl[cat]}:")
            for m in cats[cat]:
                lines.append(f"  📽 <code>{m['code']}</code> — {m['title']}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

# ──────────────────────────────────────────
#  /new
# ──────────────────────────────────────────
async def new_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid    = update.effective_user.id
    movies = db.get_recent(10)
    if not movies:
        await update.message.reply_text(tx(uid, "no_films"))
        return
    lines = [tx(uid, "new_films") + "\n"]
    for m in movies:
        lines.append(f"📽 <code>{m['code']}</code> — {m['title']}")
    await update.message.reply_text("\n".join(lines), parse_mode="HTML")

# ──────────────────────────────────────────
#  KANAL TEKSHIRUVI
# ──────────────────────────────────────────
CHANNEL = "@davxtv"

async def is_subscribed(uid: int, ctx: ContextTypes.DEFAULT_TYPE) -> bool:
    try:
        member = await ctx.bot.get_chat_member(chat_id=CHANNEL, user_id=uid)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False

async def send_sub_msg(update: Update, lang: str):
    msgs = {
        "uz": "📢 Kinolarni ko'rish uchun kanalimizga a'zo bo'ling!",
        "ru": "📢 Подпишитесь на наш канал чтобы смотреть фильмы!",
        "en": "📢 Subscribe to our channel to watch movies!",
    }
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Kanalga o'tish", url=f"https://t.me/davxtv")],
        [InlineKeyboardButton("✅ A'zo bo'ldim", callback_data="check_sub")],
    ])
    await update.message.reply_text(msgs.get(lang, msgs["uz"]), reply_markup=kb)

# ──────────────────────────────────────────
#  KOD YOZILGANDA → FILM
# ──────────────────────────────────────────
async def handle_code(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    lang = get_lang(uid)

    # Til tanlanmagan
    if lang is None:
        await update.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=lang_kb(),
        )
        return

    # Kanal tekshiruvi
    if not await is_subscribed(uid, ctx):
        await send_sub_msg(update, lang)
        return

    raw   = update.message.text.strip().upper()
    movie = db.get_movie(raw)

    if not movie:
        await update.message.reply_text(tx(uid, "not_found", c=raw), parse_mode="HTML")
        return

    db.inc_views(movie["code"])
    cl = CATS[lang]

    caption = (
        f"🎬 <b>{movie['title']}</b>\n\n"
        f"{tx(uid,'cat')}: {cl.get(movie['category'], movie['category'])}\n"
        f"{tx(uid,'genre')}: {movie['genre']}\n"
        f"{tx(uid,'year')}: {movie['year']}\n"
        f"{tx(uid,'lang_f')}: {movie['language']}\n\n"
        f"{tx(uid,'views')}: {movie['views'] + 1}\n"
        f"{tx(uid,'code_l')}: <code>{movie['code']}</code>"
    )
    kb = InlineKeyboardMarkup([[
        InlineKeyboardButton(tx(uid, "another"), callback_data="ask_code")
    ]])
    await update.message.reply_video(
        video=movie["file_id"],
        caption=caption,
        parse_mode="HTML",
        reply_markup=kb,
    )

# ──────────────────────────────────────────
#  CALLBACK
# ──────────────────────────────────────────
async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    uid  = q.from_user.id
    await q.answer()

    # A'ZO BO'LDIM TUGMASI
    if data == "check_sub":
        lang = get_lang(uid) or "uz"
        if await is_subscribed(uid, ctx):
            msgs = {
                "uz": "✅ Rahmat! Endi kino kodini yuboring:",
                "ru": "✅ Спасибо! Теперь отправьте код фильма:",
                "en": "✅ Thanks! Now send the movie code:",
            }
            await q.message.reply_text(msgs.get(lang, msgs["uz"]), parse_mode="HTML")
        else:
            msgs = {
                "uz": "❌ Siz hali kanalga a'zo bo'lmadingiz!",
                "ru": "❌ Вы ещё не подписались на канал!",
                "en": "❌ You haven't subscribed yet!",
            }
            kb = InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Kanalga o'tish", url="https://t.me/davxtv")],
                [InlineKeyboardButton("✅ A'zo bo'ldim", callback_data="check_sub")],
            ])
            await q.message.reply_text(msgs.get(lang, msgs["uz"]), reply_markup=kb)
        return

    # TIL TANLASH
    if data.startswith("lang_"):
        new_lang = data[5:]             # uz / ru / en
        db.set_user_lang(uid, new_lang)
        await q.message.reply_text(
            T[new_lang]["lang_set"] + "\n\n" + T[new_lang]["enter_code"],
            parse_mode="HTML",
        )
        return

    # TIL O'ZGARTIRISH
    if data == "change_lang":
        await q.message.reply_text(
            "🌐 Tilni tanlang / Выберите язык / Choose language:",
            reply_markup=lang_kb(),
        )
        return

    # KOD SO'RASH
    if data == "ask_code":
        await q.message.reply_text(tx(uid, "enter_code"), parse_mode="HTML")
        return

    # HAQIDA
    if data == "about":
        await q.message.reply_text(tx(uid, "about"), parse_mode="HTML")
        return

    # KATEGORIYA
    if data.startswith("cat_"):
        cat    = data[4:]
        movies = db.get_by_category(cat)
        lang   = get_lang(uid) or "uz"
        cl     = CATS[lang]
        if not movies:
            await q.message.reply_text(tx(uid, "no_cat"))
            return
        lines = [f"📋 <b>{cl.get(cat, cat)}:</b>\n"]
        for m in movies:
            lines.append(f"📽 <code>{m['code']}</code> — {m['title']}")
        lines.append(f"\n{tx(uid, 'see_code')}")
        await q.message.reply_text("\n".join(lines), parse_mode="HTML")
        return

    # ADMIN CALLBACKLAR
    if data.startswith("adm_") and uid in ADMIN_IDS:
        if data == "adm_stat":
            s = db.stats()
            await q.message.reply_text(
                f"📊 Foydalanuvchilar: {s['users']}\n"
                f"🎬 Kinolar: {s['movies']}\n"
                f"👁 Ko'rishlar: {s['views']}"
            )
        elif data == "adm_users":
            await q.message.reply_text(f"👥 Jami: {len(db.get_all_users())} ta foydalanuvchi")
        elif data == "adm_add":
            await q.message.reply_text(
                "➕ Kino qo'shish:\n\n"
                "<code>/add KOD | Nomi | Kategoriya | Janr | Yil | Til | file_id</code>\n\n"
                "Misol:\n"
                "<code>/add UZ001 | Alpomish | UZ | Drama | 2023 | O'zbek | AgACAgIA...</code>",
                parse_mode="HTML",
            )
        elif data == "adm_del":
            await q.message.reply_text(
                "🗑 Kino o'chirish:\n<code>/del KOD</code>", parse_mode="HTML"
            )

# ──────────────────────────────────────────
#  ADMIN /admin
# ──────────────────────────────────────────
async def admin_panel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        await update.message.reply_text(tx(uid, "no_right"))
        return
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Kino qo'shish",   callback_data="adm_add")],
        [InlineKeyboardButton("🗑 Kino o'chirish",  callback_data="adm_del")],
        [InlineKeyboardButton("📊 Statistika",       callback_data="adm_stat")],
        [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="adm_users")],
    ])
    await update.message.reply_text("🛠 <b>Admin Panel</b>", parse_mode="HTML", reply_markup=kb)

# ──────────────────────────────────────────
#  ADMIN /add
# ──────────────────────────────────────────
async def add_movie(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return

    if not ctx.args:
        await update.message.reply_text(
            "📝 <b>Format:</b>\n"
            "<code>/add KOD | Nomi | Kategoriya | Janr | Yil | Til | file_id</code>\n\n"
            "<b>Kategoriyalar:</b> UZ | TR | HN | XR\n\n"
            "<b>Misol:</b>\n"
            "<code>/add UZ001 | Alpomish | UZ | Drama | 2023 | O'zbek | AgACAgIA...</code>\n\n"
            "❗ file_id ni olish uchun: botga video yuboring → /getid yozing",
            parse_mode="HTML",
        )
        return

    raw   = " ".join(ctx.args)
    parts = [p.strip() for p in raw.split("|")]

    if len(parts) != 7:
        await update.message.reply_text(
            f"❌ {len(parts)} ta qism topildi, 7 ta kerak!\n"
            "Har birini | bilan ajrating.\n\n"
            "Format: <code>KOD | Nomi | Kategoriya | Janr | Yil | Til | file_id</code>",
            parse_mode="HTML",
        )
        return

    code, title, cat, genre, year, lang_f, file_id = parts
    cat = cat.upper()

    if cat not in ["UZ", "TR", "HN", "XR"]:
        await update.message.reply_text("❌ Kategoriya: UZ, TR, HN yoki XR bo'lishi kerak.")
        return

    ok = db.add_movie(code, title, cat, genre, year, lang_f, file_id)
    if ok:
        await update.message.reply_text(
            f"✅ Kino qo'shildi!\n\n"
            f"🎬 <b>{title}</b>\n"
            f"🔑 Kod: <code>{code.upper()}</code>\n"
            f"📁 Kategoriya: {cat}",
            parse_mode="HTML",
        )
    else:
        await update.message.reply_text(
            f"❌ <code>{code.upper()}</code> kodi allaqachon mavjud!",
            parse_mode="HTML",
        )

# ──────────────────────────────────────────
#  ADMIN /del
# ──────────────────────────────────────────
async def del_movie(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
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

# ──────────────────────────────────────────
#  ADMIN /stats
# ──────────────────────────────────────────
async def stats_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    s    = db.stats()
    text = (
        "📊 <b>Statistika</b>\n\n"
        f"👥 Foydalanuvchilar: <b>{s['users']}</b>\n"
        f"🎬 Kinolar: <b>{s['movies']}</b>\n"
        f"👁 Ko'rishlar: <b>{s['views']}</b>\n\n"
        "🏆 <b>Top 5:</b>\n"
    )
    for m in s["top"]:
        text += f"  • <code>{m['code']}</code> {m['title']} — {m['views']} 👁\n"
    await update.message.reply_text(text, parse_mode="HTML")

# ──────────────────────────────────────────
#  ADMIN /broadcast
# ──────────────────────────────────────────
async def broadcast(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text("Format: <code>/broadcast Xabar matni</code>", parse_mode="HTML")
        return
    msg   = " ".join(ctx.args)
    users = db.get_all_users()
    sent = failed = 0
    sm   = await update.message.reply_text(f"📤 Yuborilmoqda... 0/{len(users)}")
    for i, user in enumerate(users):
        try:
            await ctx.bot.send_message(chat_id=user["user_id"], text=msg, parse_mode="HTML")
            sent += 1
        except Exception:
            failed += 1
        if (i + 1) % 20 == 0:
            await sm.edit_text(f"📤 {i+1}/{len(users)}")
    await sm.edit_text(f"✅ Yuborildi: {sent}\n❌ Xato: {failed}\n👥 Jami: {len(users)}")

# ──────────────────────────────────────────
#  ADMIN /getid  — video file_id olish
# ──────────────────────────────────────────
async def get_file_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    """Botga video yuborganda file_id olish uchun"""
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    if update.message.video:
        fid = update.message.video.file_id
        await update.message.reply_text(
            f"✅ <b>file_id:</b>\n<code>{fid}</code>",
            parse_mode="HTML",
        )
    elif update.message.document:
        fid = update.message.document.file_id
        await update.message.reply_text(
            f"✅ <b>file_id (document):</b>\n<code>{fid}</code>",
            parse_mode="HTML",
        )
    else:
        await update.message.reply_text("❌ Video yuboring!")

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Foydalanuvchi buyruqlari
    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("help",      help_cmd))
    app.add_handler(CommandHandler("list",      list_cmd))
    app.add_handler(CommandHandler("new",       new_cmd))
    app.add_handler(CommandHandler("lang",      lang_cmd))

    # Admin buyruqlari
    app.add_handler(CommandHandler("admin",     admin_panel))
    app.add_handler(CommandHandler("add",       add_movie))
    app.add_handler(CommandHandler("del",       del_movie))
    app.add_handler(CommandHandler("stats",     stats_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))

    # Video/document yuborilganda file_id berish (admin uchun)
    app.add_handler(MessageHandler(
        filters.VIDEO | filters.Document.ALL,
        get_file_id,
    ))

    # Callback tugmalar
    app.add_handler(CallbackQueryHandler(cb))

    # Matn (kino kodi)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    logger.info("🚀 DavxTV Bot v2.0 ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
