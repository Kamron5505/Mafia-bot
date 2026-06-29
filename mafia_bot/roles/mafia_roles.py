from roles.base_role import BaseRole


# ==================== QORA KUCHLAR (MAFIYA) ====================

class OkeanQirali(BaseRole):
    """Don — Mafiya rahbari, ovozlarni qayta yo'naltirishi mumkin"""
    name = "Don"
    title = "Okean Qirali"
    emoji = "👑"
    team = "mafia"
    description = "Siz mafiya rahbarisiz! Kechasi mafiya bilan birga qurbon tanlaysiz. Bundan tashqari, kunduzgi ovoz berishda bir marta ovozlarni boshqa o'yinchiga yo'naltirishingiz mumkin."
    night_action = True
    action_type = "mafia_kill"


class Akula(BaseRole):
    """Oddiy mafiya qotili"""
    name = "Mafiya"
    title = "Akula"
    emoji = "🦈"
    team = "mafia"
    description = "Siz oddiy mafiya a'zosisiz. Kechasi boshqa mafiya a'zolari bilan birga qurbon tanlaysiz."
    night_action = True
    action_type = "mafia_kill"


class QaroqchilarSardori(BaseRole):
    """Yakudza — bir shahar aholisini mafiyaga aylantirishi mumkin"""
    name = "Yakudza"
    title = "Qaroqchilar Sardori"
    emoji = "🏴‍☠️"
    team = "mafia"
    description = "Siz yakudza sardorisiz! Bir marta o'yin davomida bir shahar aholisini o'z tarafingizga o'tkazishingiz mumkin."
    night_action = True
    action_type = "convert"


class ZaharliFugu(BaseRole):
    """Mafiya yordamchisi — bir o'yinchini bloklaydi"""
    name = "Mafiya yordamchisi"
    title = "Zaharli Fugu"
    emoji = "🐡"
    team = "mafia"
    description = "Siz mafiya yordamchisisiz! Kechasi bir o'yinchining harakatini bloklashingiz mumkin."
    night_action = True
    action_type = "block"


class GigantKalmar(BaseRole):
    """Qora qaroqchi — rol ma'lumotini o'g'irlaydi"""
    name = "Qora qaroqchi"
    title = "Gigant Kalmar"
    emoji = "🦑"
    team = "mafia"
    description = "Siz qora qaroqchisiz! Kechasi bir o'yinchining rolini bilib olishingiz mumkin."
    night_action = True
    action_type = "steal_info"


class QisqichbaqaOGri(BaseRole):
    """O'g'ri — boshqa roldan qobiliyat o'g'irlaydi"""
    name = "O'g'ri"
    title = "Qisqichbaqa-o'g'ri"
    emoji = "🦀"
    team = "mafia"
    description = "Siz o'g'risiz! Bir marta bir o'yinchining qobiliyatini o'g'irlab, undan foydalanishingiz mumkin."
    night_action = True
    action_type = "steal_ability"


class ChaqquvchiMeduza(BaseRole):
    """Shantajchi — bir o'yinchi kunduzi gapira olmaydi"""
    name = "Shantajchi"
    title = "Chaqquvchi Meduza"
    emoji = "🪼"
    team = "mafia"
    description = "Siz shantajchisiz! Kechasi bir o'yinchini shantaj qilib, ertasi kuni uning gapirishiga yo'l qo'ymaysiz."
    night_action = True
    action_type = "silence"


class ShurSuvTimsohi(BaseRole):
    """Advokat — mafiya a'zosini ovozdan himoya qiladi"""
    name = "Advokat"
    title = "Sho'r suv Timsohi"
    emoji = "🐊"
    team = "mafia"
    description = "Siz advokatsiz! Kunduzi bir marta mafiya a'zosini chiqarilishdan himoya qilishingiz mumkin."
    night_action = False
    passive = True


class Qilichbaliq(BaseRole):
    """Qotil — kunduzi o'ldiradi"""
    name = "Qotil"
    title = "Qilichbaliq"
    emoji = "🗡"
    team = "mafia"
    description = "Siz qotilsiz! Kunduzi bir marta bir o'yinchini o'ldirishingiz mumkin."
    night_action = False
    passive = True


class XameleonBaliq(BaseRole):
    """Josus — detektivga shahar aholisi bo'lib ko'rinadi"""
    name = "Josus"
    title = "Xameleon Baliq"
    emoji = "🐠"
    team = "mafia"
    description = "Siz josussiz! Detektiv sizni tekshirganda, siz shahar aholisi bo'lib ko'rinasiz."
    night_action = False
    passive = True


class QotilKit(BaseRole):
    """Reketir — bir o'yinchini ma'lum targetga ovoz berishga majbur qiladi"""
    name = "Reketir"
    title = "Qotil Kit"
    emoji = "🐋"
    team = "mafia"
    description = "Siz reketirsiz! Kechasi bir o'yinchini ma'lum bir kishiga ovoz berishga majburlashingiz mumkin."
    night_action = True
    action_type = "force_vote"


class DengizTubisiz(BaseRole):
    """Ko'lanka — kechagi tekshiruvlardan yashirinadi"""
    name = "Ko'lanka"
    title = "Dengiz Tubisiz"
    emoji = "🕳"
    team = "mafia"
    description = "Siz ko'lankasiz! Kechagi barcha tekshiruvlardan yashirinib qolasiz. Sizni hech kim tekshira olmaydi."
    night_action = False
    passive = True


class MinaBaliq(BaseRole):
    """Bombachi — chiqarilganda portlaydi va yonidagini o'ldiradi"""
    name = "Bombachi"
    title = "Mina-baliq"
    emoji = "💣"
    team = "mafia"
    description = "Siz bombachisiz! Agar ovoz berish orqali chiqarilsangiz, portlaysiz va bir tasodifiy o'yinchini o'zingiz bilan birga olib ketasiz."
    night_action = False
    passive = True


class ZilzilaviySkat(BaseRole):
    """Zaharlovchi — zaharlaydi, keyingi kechada o'ladi"""
    name = "Zaharlovchi"
    title = "Zilzilaviy Skat"
    emoji = "🧪"
    team = "mafia"
    description = "Siz zaharlovchisiz! Kechasi bir o'yinchini zaharlaysiz, u keyingi kechada halok bo'ladi."
    night_action = True
    action_type = "poison"


class DengizChayoni(BaseRole):
    """Yollanma qotil — bir targetni o'ldirish uchun yollangan"""
    name = "Yollanma qotil"
    title = "Dengiz Chayoni"
    emoji = "🦂"
    team = "mafia"
    description = "Siz yollanma qotilsiz! Bir marta bir o'yinchini o'ldirishingiz mumkin. Agar muvaffaqiyatli o'ldirsangiz, g'alaba qozonasiz."
    night_action = True
    action_type = "kill_once"


class KemaKalamushi(BaseRole):
    """Sotqin — shahar aholisi lekin mafiya uchun ishlaydi"""
    name = "Sotqin"
    title = "Kema Kalamushi"
    emoji = "🐀"
    team = "mafia"
    description = "Siz sotqinsiz! Shahar aholisiga o'xshaysiz, lekin aslida mafiya uchun ishlaysiz. Mafiya g'alaba qozonsa, siz ham g'alaba qozonasiz."
    night_action = False
    passive = True


class OlikDengizchi(BaseRole):
    """Nekromant — o'lgan o'yinchining qobiliyatidan bir marta foydalanadi"""
    name = "Nekromant"
    title = "O'lik Dengizchi"
    emoji = "🦴"
    team = "mafia"
    description = "Siz nekromantsiz! Bir marta o'lgan o'yinchining qobiliyatidan foydalanishingiz mumkin."
    night_action = True
    action_type = "necromancy"


class DengizIloni(BaseRole):
    """Yovuz jodugar — ikki o'yinchining rolini almashtiradi"""
    name = "Yovuz jodugar"
    title = "Dengiz Iloni"
    emoji = "🐍"
    team = "mafia"
    description = "Siz yovuz jodugarsiz! Kechasi ikki o'yinchining rollarini almashtirishingiz mumkin."
    night_action = True
    action_type = "swap_roles"


class Piranya(BaseRole):
    """Odamxo'r — har o'ldirishda kuchayadi"""
    name = "Odamxo'r"
    title = "Piranya"
    emoji = "🩸"
    team = "mafia"
    description = "Siz odamxo'rsiz! Har bir o'ldirishingizda kuchayib borasiz. Ovozingiz qo'shimcha vaznga ega bo'ladi."
    night_action = True
    action_type = "mafia_kill"


class IfloslanganSuv(BaseRole):
    """Qora Tabib — mafiyani davolaydi, shaharni zaharlaydi"""
    name = "Qora Tabib"
    title = "Ifloslangan Suv"
    emoji = "🦠"
    team = "mafia"
    description = "Siz qora tabibsiz! Kechasi bir mafiya a'zosini davolaysiz yoki bir shahar aholisini zaharlaysiz."
    night_action = True
    action_type = "dark_heal"
