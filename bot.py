#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════╗
║       DavxTV Bot  v3.0          ║
║  Mukammal • Qulay • Barqaror    ║
╚══════════════════════════════════╝
"""

import logging
import os
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

# ═══════════════════════════════════════════════════
BOT_TOKEN = "8635105226:AAGbibuBkOF_Me9ZW7GJmyhp78VILO2L1Cg"
ADMIN_IDS = [440715427]
# ═══════════════════════════════════════════════════

# DB ni /app/data/ da saqlash (Railway Volume)
os.makedirs("/app/data", exist_ok=True)
db = Database("/app/data/davxtv.db")

# Boshlang'ich kanal — DB ga qo'shiladi
DEFAULT_CHANNEL = "@davxtv"
if not db.get_channels():
    db.add_channel(DEFAULT_CHANNEL, "DavxTV")

# ──────────────────────────────────────────
#  MATNLAR (3 til)
# ──────────────────────────────────────────
T = {
    "uz": {
        "choose_lang":  "🌐 Assalomu alaykum!\nTilni tanlang:",
        "lang_set":     "✅ O'zbekcha tanlandi!",
        "sub_required": (
            "📢 <b>Kanalga a'zo bo'ling!</b>\n\n"
            "Kinolarni ko'rish uchun quyidagi kanalga\n"
            "a'zo bo'lishingiz kerak 👇"
        ),
        "sub_done":     "✅ Rahmat! Endi kino kodini yuboring 🎬",
        "sub_fail":     "❌ Siz hali a'zo bo'lmadingiz!\nIltimos kanalga a'zo bo'ling 👇",
        "welcome": (
            "👋 Salom <b>{n}</b>!\n\n"
            "🎬 <b>DavxTV</b> ga xush kelibsiz!\n\n"
            "📌 Kino <b>kodini</b> yuboring → film tomosha qiling\n\n"
            "📋 /list — barcha kinolar\n"
            "🆕 /new  — yangi kinolar"
        ),
        "enter_code":   "🔑 Kino kodini yuboring:",
        "not_found":    "❌ <b>{c}</b> — bu kod topilmadi.\n\n📋 Barcha kodlar: /list",
        "cat":          "📁 Tur",
        "genre":        "⭐ Janr",
        "year":         "🗓 Yil",
        "lang_f":       "🌐 Til",
        "views":        "👁 Ko'rishlar",
        "code_l":       "🔑 Kod",
        "another":      "🔄 Boshqa kino",
        "no_films":     "📭 Hozircha kinolar yo'q.",
        "all_films":    "📋 <b>Barcha kinolar:</b>",
        "new_films":    "🆕 <b>Yangi kinolar:</b>",
        "no_cat":       "📭 Bu turda kino yo'q.",
        "see_code":     "👆 Kodini yuboring → film tomosha qiling!",
        "no_right":     "❌ Admin huquqi yo'q.",
        "help": (
            "📖 <b>Yordam</b>\n\n"
            "🔹 Kino kodini yuboring → film yuklanadi\n\n"
            "📌 <b>Kod formati:</b>\n"
            "   <code>UZ001</code> — O'zbek kino\n"
            "   <code>TR001</code> — Turk serial\n"
            "   <code>HN001</code> — Hind kino\n"
            "   <code>XR001</code> — Xorij kino\n\n"
            "📋 /list — barcha kinolar\n"
            "🆕 /new  — yangi kinolar\n"
            "🌐 /lang — tilni o'zgartirish"
        ),
    },
    "ru": {
        "choose_lang":  "🌐 Добро пожаловать!\nВыберите язык:",
        "lang_set":     "✅ Русский язык выбран!",
        "sub_required": (
            "📢 <b>Подпишитесь на канал!</b>\n\n"
            "Для просмотра фильмов необходимо\n"
            "подписаться на наш канал 👇"
        ),
        "sub_done":     "✅ Спасибо! Теперь отправьте код фильма 🎬",
        "sub_fail":     "❌ Вы ещё не подписались!\nПожалуйста подпишитесь на канал 👇",
        "welcome": (
            "👋 Привет <b>{n}</b>!\n\n"
            "🎬 Добро пожаловать в <b>DavxTV</b>!\n\n"
            "📌 Отправьте <b>код</b> фильма → смотрите кино\n\n"
            "📋 /list — все фильмы\n"
            "🆕 /new  — новые фильмы"
        ),
        "enter_code":   "🔑 Отправьте код фильма:",
        "not_found":    "❌ <b>{c}</b> — такой код не найден.\n\n📋 Все коды: /list",
        "cat":          "📁 Категория",
        "genre":        "⭐ Жанр",
        "year":         "🗓 Год",
        "lang_f":       "🌐 Язык",
        "views":        "👁 Просмотры",
        "code_l":       "🔑 Код",
        "another":      "🔄 Другой фильм",
        "no_films":     "📭 Фильмов пока нет.",
        "all_films":    "📋 <b>Все фильмы:</b>",
        "new_films":    "🆕 <b>Новые фильмы:</b>",
        "no_cat":       "📭 В этой категории нет фильмов.",
        "see_code":     "👆 Отправьте код → смотрите фильм!",
        "no_right":     "❌ Нет прав администратора.",
        "help": (
            "📖 <b>Помощь</b>\n\n"
            "🔹 Отправьте код → фильм загрузится\n\n"
            "📌 <b>Формат кода:</b>\n"
            "   <code>UZ001</code> — Узбекский\n"
            "   <code>TR001</code> — Турецкий\n"
            "   <code>HN001</code> — Индийский\n"
            "   <code>XR001</code> — Зарубежный\n\n"
            "📋 /list — все фильмы\n"
            "🆕 /new  — новые фильмы\n"
            "🌐 /lang — сменить язык"
        ),
    },
    "en": {
        "choose_lang":  "🌐 Welcome!\nChoose language:",
        "lang_set":     "✅ English selected!",
        "sub_required": (
            "📢 <b>Subscribe to our channel!</b>\n\n"
            "To watch movies you need to\n"
            "subscribe to our channel 👇"
        ),
        "sub_done":     "✅ Thank you! Now send the movie code 🎬",
        "sub_fail":     "❌ You haven't subscribed yet!\nPlease subscribe to the channel 👇",
        "welcome": (
            "👋 Hello <b>{n}</b>!\n\n"
            "🎬 Welcome to <b>DavxTV</b>!\n\n"
            "📌 Send the movie <b>code</b> → watch movies\n\n"
            "📋 /list — all movies\n"
            "🆕 /new  — new movies"
        ),
        "enter_code":   "🔑 Send movie code:",
        "not_found":    "❌ <b>{c}</b> — code not found.\n\n📋 All codes: /list",
        "cat":          "📁 Category",
        "genre":        "⭐ Genre",
        "year":         "🗓 Year",
        "lang_f":       "🌐 Language",
        "views":        "👁 Views",
        "code_l":       "🔑 Code",
        "another":      "🔄 Another movie",
        "no_films":     "📭 No movies yet.",
        "all_films":    "📋 <b>All movies:</b>",
        "new_films":    "🆕 <b>New movies:</b>",
        "no_cat":       "📭 No movies in this category.",
        "see_code":     "👆 Send code → watch movie!",
        "no_right":     "❌ No admin rights.",
        "help": (
            "📖 <b>Help</b>\n\n"
            "🔹 Send code → movie loads\n\n"
            "📌 <b>Code format:</b>\n"
            "   <code>UZ001</code> — Uzbek\n"
            "   <code>TR001</code> — Turkish\n"
            "   <code>HN001</code> — Indian\n"
            "   <code>XR001</code> — Foreign\n\n"
            "📋 /list — all movies\n"
            "🆕 /new  — new movies\n"
            "🌐 /lang — change language"
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
    return db.get_user_lang(uid)

def tx(uid, key, **kw):
    lang = get_lang(uid) or "uz"
    text = T[lang].get(key, T["uz"].get(key, ""))
    return text.format(**kw) if kw else text

def lang_kb():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz"),
        InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
    ]])

# ──────────────────────────────────────────
#  KANAL TEKSHIRUVI
# ──────────────────────────────────────────
async def is_subscribed(uid: int, ctx: ContextTypes.DEFAULT_TYPE) -> bool:
    channels = db.get_channels()
    if not channels:
        return True
    for ch in channels:
        try:
            member = await ctx.bot.get_chat_member(chat_id=ch["username"], user_id=uid)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except Exception:
            pass
    return True

async def send_sub_keyboard(update_or_query, lang: str, is_callback=False):
    channels = db.get_channels()
    buttons  = []
    for ch in channels:
        name = ch["title"] or ch["username"]
        buttons.append([InlineKeyboardButton(
            f"📢 {name}", url=f"https://t.me/{ch['username'].lstrip('@')}"
        )])
    buttons.append([InlineKeyboardButton("✅ A'zo bo'ldim / Подписался / Subscribed", callback_data="check_sub")])
    kb   = InlineKeyboardMarkup(buttons)
    text = T[lang]["sub_required"]

    if is_callback:
        await update_or_query.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
    else:
        await update_or_query.message.reply_text(text, parse_mode="HTML", reply_markup=kb)

# ──────────────────────────────────────────
#  /start
# ──────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username or "", user.first_name or "")
    lang = get_lang(user.id)

    if lang is None:
        await update.message.reply_text(
            T["uz"]["choose_lang"],
            reply_markup=lang_kb(),
        )
        return

    if not await is_subscribed(user.id, ctx):
        await send_sub_keyboard(update, lang)
        return

    await update.message.reply_text(
        tx(user.id, "welcome", n=user.first_name),
        parse_mode="HTML",
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
    await update.message.reply_text(tx(update.effective_user.id, "help"), parse_mode="HTML")

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
#  KOD YOZILGANDA → FILM
# ──────────────────────────────────────────
async def handle_code(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid  = update.effective_user.id
    lang = get_lang(uid)

    if lang is None:
        await update.message.reply_text(
            T["uz"]["choose_lang"], reply_markup=lang_kb()
        )
        return

    if not await is_subscribed(uid, ctx):
        await send_sub_keyboard(update, lang)
        return

    raw   = update.message.text.strip().upper()
    movie = db.get_movie(raw)

    if not movie:
        await update.message.reply_text(tx(uid, "not_found", c=raw), parse_mode="HTML")
        return

    db.inc_views(movie["code"])
    cl = CATS[get_lang(uid) or "uz"]

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
#  VIDEO → FILE_ID (Admin)
# ──────────────────────────────────────────
async def get_file_id(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    if update.message.video:
        fid = update.message.video.file_id
    elif update.message.document:
        fid = update.message.document.file_id
    else:
        await update.message.reply_text("❌ Video yuboring!")
        return
    await update.message.reply_text(
        f"✅ <b>file_id:</b>\n<code>{fid}</code>\n\n"
        f"📝 Kino qo'shish:\n"
        f"<code>/add KOD | Nomi | UZ | Janr | Yil | Til | {fid}</code>",
        parse_mode="HTML",
    )

# ──────────────────────────────────────────
#  CALLBACK
# ──────────────────────────────────────────
async def cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q    = update.callback_query
    data = q.data
    uid  = q.from_user.id
    lang = get_lang(uid) or "uz"
    await q.answer()

    # ── TIL TANLASH ──────────────────────────────────────────────────────
    if data.startswith("lang_"):
        new_lang = data[5:]
        db.set_user_lang(uid, new_lang)

        if not await is_subscribed(uid, ctx):
            await q.message.reply_text(T[new_lang]["lang_set"])
            await send_sub_keyboard(q, new_lang, is_callback=True)
            return

        user = q.from_user
        await q.message.reply_text(T[new_lang]["lang_set"])
        await q.message.reply_text(
            T[new_lang]["welcome"].format(n=user.first_name),
            parse_mode="HTML",
        )
        return

    # ── KANAL TEKSHIRUVI ─────────────────────────────────────────────────
    if data == "check_sub":
        if await is_subscribed(uid, ctx):
            user = q.from_user
            await q.message.reply_text(T[lang]["sub_done"])
            await q.message.reply_text(
                T[lang]["welcome"].format(n=user.first_name),
                parse_mode="HTML",
            )
        else:
            channels = db.get_channels()
            buttons  = []
            for ch in channels:
                name = ch["title"] or ch["username"]
                buttons.append([InlineKeyboardButton(
                    f"📢 {name}", url=f"https://t.me/{ch['username'].lstrip('@')}"
                )])
            buttons.append([InlineKeyboardButton(
                "✅ A'zo bo'ldim / Подписался / Subscribed", callback_data="check_sub"
            )])
            await q.message.reply_text(
                T[lang]["sub_fail"],
                parse_mode="HTML",
                reply_markup=InlineKeyboardMarkup(buttons),
            )
        return

    # ── KOD SO'RASH ──────────────────────────────────────────────────────
    if data == "ask_code":
        await q.message.reply_text(T[lang]["enter_code"])
        return

    # ── ADMIN CALLBACKLAR ────────────────────────────────────────────────
    if data.startswith("adm_") and uid in ADMIN_IDS:
        if data == "adm_stat":
            s = db.stats()
            await q.message.reply_text(
                f"📊 <b>Statistika</b>\n\n"
                f"👥 Foydalanuvchilar: <b>{s['users']}</b>\n"
                f"🎬 Kinolar: <b>{s['movies']}</b>\n"
                f"👁 Ko'rishlar: <b>{s['views']}</b>\n\n"
                f"🏆 <b>Top 5:</b>\n" +
                "\n".join(f"  • <code>{m['code']}</code> {m['title']} — {m['views']} 👁" for m in s["top"]),
                parse_mode="HTML",
            )
        elif data == "adm_users":
            await q.message.reply_text(f"👥 Jami: <b>{len(db.get_all_users())}</b> ta foydalanuvchi", parse_mode="HTML")
        elif data == "adm_channels":
            channels = db.get_channels()
            if channels:
                text = "📢 <b>Kanallar:</b>\n\n" + "\n".join(
                    f"  • {ch['username']} — {ch['title']}" for ch in channels
                )
            else:
                text = "📭 Kanallar yo'q."
            text += "\n\n➕ Kanal qo'shish: <code>/addch @username Kanal nomi</code>"
            text += "\n🗑 O'chirish: <code>/rmch @username</code>"
            await q.message.reply_text(text, parse_mode="HTML")
        elif data == "adm_add":
            await q.message.reply_text(
                "➕ <b>Kino qo'shish:</b>\n\n"
                "Botga video yuboring → file_id oling\n"
                "Keyin:\n"
                "<code>/add KOD | Nomi | Tur | Janr | Yil | Til | file_id</code>\n\n"
                "<b>Turlar:</b> UZ | TR | HN | XR\n\n"
                "<b>Misol:</b>\n"
                "<code>/add UZ001 | Alpomish | UZ | Drama | 2023 | O'zbek | AgACAgIA...</code>",
                parse_mode="HTML",
            )
        elif data == "adm_del":
            await q.message.reply_text("🗑 <code>/del KOD</code>", parse_mode="HTML")
        return

# ──────────────────────────────────────────
#  ADMIN /admin
# ──────────────────────────────────────────
async def admin_panel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        await update.message.reply_text(tx(uid, "no_right"))
        return
    s  = db.stats()
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Kino qo'sh", callback_data="adm_add"),
            InlineKeyboardButton("🗑 Kino o'chir", callback_data="adm_del"),
        ],
        [
            InlineKeyboardButton("📊 Statistika", callback_data="adm_stat"),
            InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="adm_users"),
        ],
        [
            InlineKeyboardButton("📢 Kanallar", callback_data="adm_channels"),
        ],
    ])
    await update.message.reply_text(
        f"🛠 <b>Admin Panel</b>\n\n"
        f"👥 {s['users']} foydalanuvchi\n"
        f"🎬 {s['movies']} kino\n"
        f"👁 {s['views']} ko'rish",
        parse_mode="HTML",
        reply_markup=kb,
    )

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
            "<code>/add KOD | Nomi | Tur | Janr | Yil | Til | file_id</code>\n\n"
            "<b>Turlar:</b> UZ | TR | HN | XR\n\n"
            "<b>Misol:</b>\n"
            "<code>/add UZ001 | Alpomish | UZ | Drama | 2023 | O'zbek | AgACAgIA...</code>",
            parse_mode="HTML",
        )
        return
    parts = [p.strip() for p in " ".join(ctx.args).split("|")]
    if len(parts) != 7:
        await update.message.reply_text(
            f"❌ {len(parts)} ta qism topildi, 7 ta kerak!\n"
            "Har birini <b>|</b> bilan ajrating.",
            parse_mode="HTML",
        )
        return
    code, title, cat, genre, year, lang_f, file_id = parts
    cat = cat.upper()
    if cat not in ["UZ", "TR", "HN", "XR"]:
        await update.message.reply_text("❌ Tur: UZ, TR, HN yoki XR bo'lishi kerak.")
        return
    ok = db.add_movie(code, title, cat, genre, year, lang_f, file_id)
    if ok:
        await update.message.reply_text(
            f"✅ <b>Qo'shildi!</b>\n\n"
            f"🎬 {title}\n"
            f"🔑 Kod: <code>{code.upper()}</code>\n"
            f"📁 Tur: {cat}",
            parse_mode="HTML",
        )
    else:
        await update.message.reply_text(
            f"❌ <code>{code.upper()}</code> kodi allaqachon mavjud!", parse_mode="HTML"
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
    if db.delete_movie(code):
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
    await sm.edit_text(
        f"✅ Yuborildi: {sent}\n❌ Xato: {failed}\n👥 Jami: {len(users)}"
    )

# ──────────────────────────────────────────
#  ADMIN /addch — kanal qo'shish
# ──────────────────────────────────────────
async def add_channel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text(
            "Format: <code>/addch @username Kanal nomi</code>\n\n"
            "Misol: <code>/addch @davxtv2 DavxTV 2</code>",
            parse_mode="HTML",
        )
        return
    username = ctx.args[0]
    title    = " ".join(ctx.args[1:]) if len(ctx.args) > 1 else username
    ok = db.add_channel(username, title)
    if ok:
        await update.message.reply_text(f"✅ <b>{title}</b> ({username}) qo'shildi!", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ {username} allaqachon mavjud!", parse_mode="HTML")

# ──────────────────────────────────────────
#  ADMIN /rmch — kanal o'chirish
# ──────────────────────────────────────────
async def remove_channel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return
    if not ctx.args:
        await update.message.reply_text("Format: <code>/rmch @username</code>", parse_mode="HTML")
        return
    username = ctx.args[0]
    ok = db.remove_channel(username)
    if ok:
        await update.message.reply_text(f"🗑 {username} o'chirildi.", parse_mode="HTML")
    else:
        await update.message.reply_text(f"❌ {username} topilmadi.", parse_mode="HTML")

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    # Foydalanuvchi
    app.add_handler(CommandHandler("start",     start))
    app.add_handler(CommandHandler("help",      help_cmd))
    app.add_handler(CommandHandler("list",      list_cmd))
    app.add_handler(CommandHandler("new",       new_cmd))
    app.add_handler(CommandHandler("lang",      lang_cmd))

    # Admin
    app.add_handler(CommandHandler("admin",     admin_panel))
    app.add_handler(CommandHandler("add",       add_movie))
    app.add_handler(CommandHandler("del",       del_movie))
    app.add_handler(CommandHandler("stats",     stats_cmd))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("addch",     add_channel))
    app.add_handler(CommandHandler("rmch",      remove_channel))

    # Video → file_id
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, get_file_id))

    # Callback
    app.add_handler(CallbackQueryHandler(cb))

    # Kod
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))

    logger.info("🚀 DavxTV Bot v3.0 ishga tushdi!")
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)


if __name__ == "__main__":
    main()
