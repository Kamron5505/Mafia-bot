from roles.base_role import BaseRole


# ==================== NEYTRAL VA YOLG'IZ KUCHLAR ====================

class MarvaridJufti(BaseRole):
    """Oshiqlar — birga yutadi yoki yutqazadi"""
    name = "Oshiqlar"
    title = "Marvarid Jufti"
    emoji = "🐚"
    team = "neutral"
    description = "Siz oshiqlardan birisiz! Yana bir oshiq bor. Agar bir oshiq o'lsa, ikkinchisi ham o'ladi. Birga yutasiz yoki yutqazasiz."
    night_action = False
    passive = True


class DengizBoroni(BaseRole):
    """Manyak — yolg'iz qolib, hammni o'ldirish orqali yutadi"""
    name = "Manyak"
    title = "Dengiz Bo'roni"
    emoji = "🌪"
    team = "neutral"
    description = "Siz manyaksiz! Yolg'iz qolib, hamma o'yinchilarni o'ldirish orqali g'alaba qozonasiz. Kechasi bir o'yinchini o'ldirasiz."
    night_action = True
    action_type = "serial_kill"


class AyyorOktopus(BaseRole):
    """Joker — ovoz berish orqali chiqarilish orqali yutadi"""
    name = "Joker"
    title = "Ayyor Oktopus"
    emoji = "🐙"
    team = "neutral"
    description = "Siz jokersiz! G'alaba qozonish uchun ovoz berish orqali chiqarilishingiz kerak."
    night_action = False
    passive = True


class SuvostiVulgoni(BaseRole):
    """Qasoskor — agar o'ldirilgan o'yinchi chiqarilsa, yutadi"""
    name = "Qasoskor"
    title = "Suvosti Vulgoni"
    emoji = "🌋"
    team = "neutral"
    description = "Siz qasoskorsiz! Agar sizni o'ldirgan o'yinchi ovoz berish orqali chiqarilsa, g'alaba qozonasiz."
    night_action = False
    passive = True


class Girdob(BaseRole):
    """Telba — tashrif buyurgan rollarni tasodifiy yo'naltiradi"""
    name = "Telba"
    title = "Girdob"
    emoji = "🌀"
    team = "neutral"
    description = "Siz telbasiz! Sizga tashrif buyurgan barcha rollar tasodifiy ravishda boshqa o'yinchilarga yo'naltiriladi."
    night_action = False
    passive = True


class ChokkanKemaRuhi(BaseRole):
    """Arvoh — o'lgandan keyin ham ovoz bera oladi"""
    name = "Arvoh"
    title = "Cho'kkan Kema Ruhi"
    emoji = "👻"
    team = "neutral"
    description = "Siz arvohsiz! O'lgandan keyin ham ovoz berishda qatnashishingiz mumkin."
    night_action = False
    passive = True


class MuzlaganDengizchi(BaseRole):
    """La'natlangan — agar mafiya o'ldirsa, mafiyaga aylanadi"""
    name = "La'natlangan"
    title = "Muzlagan Dengizchi"
    emoji = "🧟‍♂️"
    team = "neutral"
    description = "Siz la'natlangansiz! Agar mafiya sizni o'ldirishga urinsa, o'lish o'rniga mafiyaga aylanasiz."
    night_action = False
    passive = True


class Xarpunchi(BaseRole):
    """Jallod — bir targetni chiqarish uchun tayinlangan"""
    name = "Jallod"
    title = "Xarpunchi"
    emoji = "🪓"
    team = "neutral"
    description = "Siz jallodsiz! Bir o'yinchini chiqarilishiga erishishingiz kerak. Agar u chiqarilsa, g'alaba qozonasiz."
    night_action = False
    passive = True


class BermudAsiri(BaseRole):
    """Sektant — o'yinchilarni sektaga qabul qiladi"""
    name = "Sektant"
    title = "Bermud Asiri"
    emoji = "🧿"
    team = "neutral"
    description = "Siz sektantsiz! Har kecha bir o'yinchini o'z sektangizga qabul qilishingiz mumkin. Sekta a'zolari birga yutadi."
    night_action = True
    action_type = "recruit"


class YunonOlovi(BaseRole):
    """Piroman — o'yinchilarni yog'lab, keyin yoqadi"""
    name = "Piroman"
    title = "Yunon Olovi"
    emoji = "🔥"
    team = "neutral"
    description = "Siz piromansiz! Kechasi o'yinchilarni yog'laysiz. Keyin bir kechada hammasini yoqib yuborishingiz mumkin."
    night_action = True
    action_type = "douse"


class SuvostiKorshapalagi(BaseRole):
    """Vampir — har kecha o'yinchilarni vampirga aylantiradi"""
    name = "Vampir"
    title = "Suvosti Ko'rshapalagi"
    emoji = "🦇"
    team = "neutral"
    description = "Siz vampirsiz! Har kecha bir o'yinchini vampirga aylantirasiz. Vampirlar birga yutadi."
    night_action = True
    action_type = "convert_vampire"


class ZaharliSuvoti(BaseRole):
    """Infeksiya tashuvchi — 2 kechadan keyin o'ldiradigan infeksiya yuqtiradi"""
    name = "Infeksiya tashuvchi"
    title = "Zaharli Suvo'ti"
    emoji = "🟢"
    team = "neutral"
    description = "Siz infeksiya tashuvchisiz! Kechasi bir o'yinchiga infeksiya yuqtirasiz. U 2 kechadan keyin halok bo'ladi."
    night_action = True
    action_type = "infect"


class Kraken(BaseRole):
    """Iblis — kuchli solo qotil, maxsus immunitetga ega"""
    name = "Iblis"
    title = "Kraken"
    emoji = "🐙"
    team = "neutral"
    description = "Siz krakensiz! Kuchli solo qotil. Kechasi bir o'yinchini o'ldirasiz va hech qanday bloklashga uchramaysiz."
    night_action = True
    action_type = "demon_kill"


class DengizQimorbozi(BaseRole):
    """Qimorboz — natijalarga pul tikib, kuch oladi"""
    name = "Qimorboz"
    title = "Dengiz Qimorbozi"
    emoji = "🎲"
    team = "neutral"
    description = "Siz qimorbozsiz! Har kecha bir o'yinchining ertasi kuni o'ladimi yoki yo'qligiga pul tikishingiz mumkin. To'g'ri topsangiz, kuch olasiz."
    night_action = True
    action_type = "gamble"


class Sarob(BaseRole):
    """Ilyuziyachi — o'yinchilarni boshqa rollardek ko'rsatadi"""
    name = "Ilyuziyachi"
    title = "Sarob"
    emoji = "🪞"
    team = "neutral"
    description = "Siz ilyuziyachisiz! Kechasi bir o'yinchini boshqa bir rol sifatida ko'rsatishingiz mumkin."
    night_action = True
    action_type = "illusion"
