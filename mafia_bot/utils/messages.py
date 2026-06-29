# =============================================
# Barcha matnlar O'zbek lotin alifbosida
# =============================================

# === Start / Profile ===
WELCOME_TEXT = """
🎮 **Mafiya O'yin Botiga Xush Kelibsiz!**

Men Telegram guruhingizda qiziqarli Mafiya o'yinlarini tashkil qilaman.
Guruhda /startgame buyrug'i bilan o'yin boshlang va do'stlaringiz bilan mafiya o'ynang!

📌 **Asosiy buyruqlar:**
/start - Botni ishga tushirish
/profile - Profilim
/help - Yordam
/rules - Qoidalar
/leave - O'yinni tark etish
"""

PROFILE_TEXT = """
👤 **PROFIL**

🎮 O'yinlar: {games_played}

🏆 G'alabalar: {wins} ({win_rate}%)
💀 Mag'lubiyatlar: {losses}

🎭 Sevimli rol: {favorite_role}

⚔️ Mafiya: {mafia_games} marta | 🛡 Shahar: {town_games} marta | 🌪 Neytral: {neutral_games} marta

🏅 Yutuqlar: {achievements}
"""

RULES_TEXT = """
📜 **MAFIYA O'YIN QOIDALARI**

🎯 **Maqsad:**
• 🦈 Qora Kuchlar (Mafiya) — barcha shahar aholisini yo'q qilish
• 🛡 Oq Kuchlar (Shahar) — barcha mafiya va neytral xavflarni bartaraf etish
• 🌪 Neytrallar — o'z shaxsiy maqsadlariga erishish

🌙 **Kecha Fazasi:**
Mafiya a'zolari birgalikda qurbon tanlaydi.
Doktor, Komissar va boshqa rollar o'z harakatlarini bajaradi.

☀️ **Kunduzgi Faza:**
Barcha o'yinchilar muhokama qiladi (5 daqiqa).
Ovoz berish orqali gumonlanuvchini chiqarib tashlashadi.

🏆 **G'alaba shartlari:**
• Mafiya: o'z soni shaharnikiga teng yoki ko'p bo'lganda
• Shahar: barcha mafiya va neytral tahdidlar yo'q qilinganda
• Neytral: o'z rol shartlariga qarab

👥 **O'yinchilar:**
Minimal: {min_players} | Maksimal: {max_players}
"""

HELP_TEXT = """
❓ **YORDAM**

**Asosiy buyruqlar:**
/start — Botni ishga tushirish
/profile — Profilimni ko'rish
/rules — O'yin qoidalari
/help — Yordam
/leave — O'yinni tark etish

**Guruh buyruqlari (faqat adminlar):**
/startgame — O'yin boshlash
/forcestart — Majburiy start
/endgame — O'yinni tugatish
/players — O'yinchilar ro'yxati
/stats — O'yin statistikasi

**Qo'llab-quvvatlanadigan tillar:**
🇺🇿 O'zbek (lotin)
"""

# === Game Lobby ===
GAME_STARTED = """
🎮 **MAFIYA O'YINI BOSHLANDI!**

O'yinga qo'shilish uchun pastdagi "Qo'shilish" tugmasini bosing.
O'yin boshlanishiga {time} soniya qoldi!

👥 Hozirgi o'yinchilar ({count}):
{players}
"""

GAME_FORCE_START = "⏩ **Majburiy start!** O'yin boshlanmoqda..."

NOT_ENOUGH_PLAYERS = "❌ O'yin boshlash uchun kamida {min_players} o'yinchi kerak. Hozir {count} ta."

PLAYER_JOINED = "✅ {name} o'yinga qo'shildi! ({count}/{max})"
PLAYER_LEFT = "🚪 {name} o'yinni tark etdi."

GAME_STARTING = """
🎯 **O'YIN BOSHLANMOQDA!**

Rollar taqsimlanmoqda...
"""

ROLE_REVEAL = """
{role_info}

📖 Sizning rolingiz: {role_full}

{description}

✅ {action_info}
"""

ROLE_DM_TITLE = "🎭 Sizning rolingiz"
ROLE_DM_TEXT = """
{role_full}

{description}

Jamoa: {team}
"""

# === Night Phase ===
NIGHT_FALL = """
🌙 **{night_count}-KECHA TUSHDI**

Barcha o'yinchilar uyquga ketishdi...
Mafiya a'zolari qurbon tanlamoqda...
"""

NIGHT_ACTION_REQUIRED = """
🌙 **Kecha harakatingiz**

{role_full}

{description}

Iltimos, harakatingizni bajaring:
"""

NIGHT_NO_ACTION = """
🌙 **Kecha**

Sizning bugun kechada maxsus harakatingiz yo'q.
Ertalabgacha kutib turing... 😴
"""

NIGHT_ACTION_DONE = "✅ Harakatingiz qabul qilindi!"

NIGHT_TIMEOUT = "⏰ Vaqt tugadi! Harakatingiz o'tkazib yuborildi."

# === Mafia Night ===
MAFIA_KILL_CHOOSE = """
🦈 **Mafiya hujumi**

Kim o'ldirilsin? Birgalikda qaror qiling:
"""

MAFIA_KILL_CONFIRM = "🦈 Mafiya {target} ni o'ldirishga qaror qildi."

# === Day Phase ===
DAY_BREAK = """
🌅 **TONG KELDI** — {night_count}-kecha tugadi
☠️ Kecha hech kim halok bo'lmadi!

🗣 **Muhokama boshlandi!** Vaqt: 5 daqiqa
"""

DAY_BREAK_DEATH = """
🌅 **TONG KELDI** — {night_count}-kecha tugadi
☠️ Kecha {victim} halok bo'ldi!

{death_reason}

🗣 **Muhokama boshlandi!** Vaqt: 5 daqiqa
"""

VOTE_PHASE = """
⚖️ **OVOZ BERISH VAQTI!**

Kim chiqarilsin? Quyidagilardan birini tanlang:

Vaqt: {time} soniya
"""

VOTE_CAST = "✅ Ovozingiz qabul qilindi!"
VOTE_NOBODY = "❌ Hech kim"
VOTE_SKIP = "⏭ O'tkazib yuborish"

VOTE_RESULTS = """
📊 **OVOZ NATIJALARI**

{vote_details}

{JUDGEMENT}
"""

VOTE_TIED = """
⚖️ Ovozlar teng! Hech kim chiqarilmaydi.
"""

VOTE_ELIMINATE = """
⚖️ **{player} o'yindan chiqarildi!**

🎭 Uning roli: {role_full}

{death_story}
"""

VOTE_NO_MAJORITY = "📊 Hech kim yetarli ovoz olmadi. Chiqarilish yo'q."

# === Game End ===
GAME_OVER = """
🏁 **O'YIN TUGADI!**

{GAME_RESULT}

🎭 **Barcha rollar:**
{all_roles}

📊 **Statistika:**
Jami o'yinchilar: {total_players}
Davomiylik: {nights} kecha
"""

MAFIA_WIN = "🦈 **Qora Kuchlar g'alaba qozondi!**"
TOWN_WIN = "🛡 **Oq Kuchlar g'alaba qozondi!**"
NEUTRAL_WIN = "🌪 **Neytral kuchlar g'alaba qozondi!**"

# === Admin ===
ADMIN_ONLY = "❌ Faqat guruh adminlari bu buyruqni ishlata oladi."
GROUP_ONLY = "❌ Bu buyruq faqat guruhda ishlaydi."
NO_ACTIVE_GAME = "❌ Faol o'yin topilmadi."
GAME_ENDED = "✅ O'yin tugatildi."
ALREADY_IN_GAME = "❌ Siz allaqachon o'yindasiz!"
NOT_IN_GAME = "❌ Siz o'yinda emassiz!"
GAME_FULL = "❌ O'yin to'lgan! (Maks: {max})"

GAME_STATS = """
📊 **O'YIN STATISTIKASI**

🎭 Rollar: {roles}

📅 Hodisalar:
{events}

👥 Tirik: {alive}
{alive_list}

💀 O'lgan: {dead}
{dead_list}
"""

PLAYERS_LIST = """
👥 *O'yinchilar:*
{players}
"""

# === Errors ===
ERROR_OCCURRED = "❌ Xatolik yuz berdi. Keyinroq urinib ko'ring."
ERROR_START_PRIVATE = "❌ /start buyrug'i faqat shaxsiy xabarlarda ishlaydi."

# === Button texts (lotin) ===
BTN_JOIN_GAME = "✅ Qo'shilish"
BTN_LEAVE_GAME = "🚪 Chiqish"
BTN_START_GAME = "🎮 O'yinni boshlash"
BTN_FORCE_START = "⏩ Majburiy start"
BTN_END_GAME = "⛔ O'yinni tugatish"
BTN_VOTE = "🗳 Ovoz berish"
BTN_SKIP_VOTE = "⏭ O'tkazib yuborish"
BTN_NO_VOTE = "❌ Hech kim"
BTN_PROFILE = "👤 Profil"
BTN_ROLES = "🎭 Rollar"
BTN_BACK = "◀ Orqaga"
BTN_CONFIRM = "✅ Tasdiqlash"
BTN_CANCEL = "❌ Bekor qilish"
BTN_LANGUAGE = "🌐 Til / Language"

# === Main Menu ===
MAIN_MENU_TEXT = """
🎮 **Mafiya O'yin Boti**

Kerakli bo'limni tanlang:
"""

# === Death Stories ===
DEATH_STORIES = [
    "{player} ni mafiya tun bo'yi kuzatib, nihoyat halok qildi. Uning jasadi ertalab topildi.",
    "{player} uyida o'lik holda topildi. Devorda qon bilan 'Mafiya' deb yozilgan edi.",
    "{player} g'oyib bo'ldi. Ertalab uning tanasi daryoda suzib yurgan holda topildi.",
    "{player} ni ovoz berish orqali chiqarib tashlashdi. U oxirgi so'zlarida begunoh ekanligini aytdi.",
    "{player} ni jamoat joyida osilgan holda topishdi. Bu mafiyaning ogohlantirishi edi.",
]
