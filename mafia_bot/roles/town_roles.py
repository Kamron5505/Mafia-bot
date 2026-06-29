from roles.base_role import BaseRole


# ==================== OQ KUCHLAR (SHAHAR) ====================

class NeptunSoqchisi(BaseRole):
    """Komissar — kechasi bir o'yinchini tekshiradi"""
    name = "Komissar"
    title = "Neptun Soqchisi"
    emoji = "🔱"
    team = "town"
    description = "Siz komissarsiz! Kechasi bir o'yinchini tekshirib, uning mafiya yoki shahar aholisi ekanligini bilib olasiz."
    night_action = True
    action_type = "investigate"


class QutqaruvchiDelfin(BaseRole):
    """Doktor — kechasi bir o'yinchini davolaydi"""
    name = "Doktor"
    title = "Qutqaruvchi Delfin"
    emoji = "🐬"
    team = "town"
    description = "Siz doktorsiz! Kechasi bir o'yinchini davolaysiz va uni mafiya hujumidan himoya qilasiz."
    night_action = True
    action_type = "heal"


class Dengizchi(BaseRole):
    """Oddiy fuqaro"""
    name = "Oddiy fuqaro"
    title = "Dengizchi"
    emoji = "⚓️"
    team = "town"
    description = "Siz oddiy fuqarosiz! Maxsus qobiliyatingiz yo'q, lekin muhokama va ovoz berish orqali mafiyani topishga yordam berasiz."
    night_action = False
    passive = True


class MarjonQoriqchisi(BaseRole):
    """Serjant — himoya qilgan o'yinchi o'rniga o'ladi"""
    name = "Serjant"
    title = "Marjon Qo'riqchisi"
    emoji = "🛡"
    team = "town"
    description = "Siz serjantsiz! Kechasi bir o'yinchini himoya qilasiz. Agar unga hujum qilinsa, siz uning o'rniga halok bo'lasiz."
    night_action = True
    action_type = "bodyguard"


class DonishmandToshbaqa(BaseRole):
    """Mer — ovozlari ikki barobar hisoblanadi"""
    name = "Mer"
    title = "Donishmand Toshbaqa"
    emoji = "🐢"
    team = "town"
    description = "Siz mersiz! Sizning ovozingiz ikki barobar hisoblanadi."
    night_action = False
    passive = True


class DengizFarishtasi(BaseRole):
    """Ruhoniy — bir o'yinchining tarafini ochib beradi"""
    name = "Ruhoniy"
    title = "Dengiz Farishtasi"
    emoji = "🕊"
    team = "town"
    description = "Siz ruhoniysiz! Bir marta o'yin davomida bir o'yinchining qaysi tarafda ekanligini ochib berishingiz mumkin."
    night_action = True
    action_type = "reveal_alignment"


class Suvparisi(BaseRole):
    """Fohisha — kechagi harakatni bloklaydi"""
    name = "Fohisha"
    title = "Suvparisi"
    emoji = "🧜‍♀️"
    team = "town"
    description = "Siz suvparisisiz! Kechasi bir o'yinchini chalg'itasiz va uning harakatini bloklaysiz."
    night_action = True
    action_type = "hook"


class KemaTotiqushi(BaseRole):
    """Jurnalist — bir marta bir sirni nashr qiladi"""
    name = "Jurnalist"
    title = "Kema To'tiqushi"
    emoji = "🦜"
    team = "town"
    description = "Siz jurnalistsiz! Bir marta o'yin davomida bir sirni (bir o'yinchining rolini) hammaga e'lon qilishingiz mumkin."
    night_action = True
    action_type = "publish_secret"


class DengizBurguti(BaseRole):
    """Kuzatuvchi — bir o'yinchiga kim kelganini ko'radi"""
    name = "Kuzatuvchi"
    title = "Dengiz Burguti"
    emoji = "🦅"
    team = "town"
    description = "Siz kuzatuvchisiz! Kechasi bir o'yinchini kuzatasiz va unga kim tashrif buyurganini bilib olasiz."
    night_action = True
    action_type = "watch"


class SodiqQisqichbaqa(BaseRole):
    """Qorovul — bir o'yinchini qamoqqa tashlaydi va himoya qiladi"""
    name = "Qorovul"
    title = "Sodiq Qisqichbaqa"
    emoji = "🦀"
    team = "town"
    description = "Siz qorovulsiz! Kechasi bir o'yinchini qamoqqa tashlaysiz. U hech kim bilan aloqa qila olmaydi va hujumlardan himoyalangan bo'ladi."
    night_action = True
    action_type = "jail"


class Gavvos(BaseRole):
    """Ovchi — o'lganda bir o'yinchini otadi"""
    name = "Ovchi"
    title = "G'avvos"
    emoji = "🤿"
    team = "town"
    description = "Siz ovchisiz! Agar o'ldirilsangiz, o'limingizdan oldin bir o'yinchini o'q uzib o'ldirishingiz mumkin."
    night_action = False
    passive = True


class KokKit(BaseRole):
    """Gvardiyachi — birinchi mafiya hujumiga chidamli"""
    name = "Gvardiyachi"
    title = "Ko'k Kit"
    emoji = "🐳"
    team = "town"
    description = "Siz gvardiyachisiz! Birinchi mafiya hujumiga chidamlisiz (o'lmaysiz)."
    night_action = False
    passive = True


class OkeanQozisi(BaseRole):
    """Sudya — bir ovozni bekor qilishi mumkin"""
    name = "Sudya"
    title = "Okean Qozisi"
    emoji = "⚖️"
    team = "town"
    description = "Siz sudyasiz! Bir marta o'yin davomida bir o'yinchining ovozini bekor qilishingiz mumkin."
    night_action = False
    passive = True


class BolgaboshAkula(BaseRole):
    """Prokuror — ovozlarsiz nomzod ko'rsatishi mumkin"""
    name = "Prokuror"
    title = "Bolg'abosh Akula"
    emoji = "🔨"
    team = "town"
    description = "Siz prokurorsiz! Bir marta ovozlarsiz bir o'yinchini chiqarilishga nomzod qilib ko'rsatishingiz mumkin."
    night_action = False
    passive = True


class Mayoqchi(BaseRole):
    """Tekshiruvchi — rol kategoriyasini tekshiradi"""
    name = "Tekshiruvchi"
    title = "Mayoqchi"
    emoji = "🔍"
    team = "town"
    description = "Siz tekshiruvchisiz! Kechasi bir o'yinchining rol kategoriyasini (mafiya/shahar/neytral) tekshirishingiz mumkin."
    night_action = True
    action_type = "check_category"


class Xazinabon(BaseRole):
    """Homi'y — bir o'yinchiga immunitet beradi"""
    name = "Homi'y"
    title = "Xazinabon"
    emoji = "💰"
    team = "town"
    description = "Siz homi'ysiz! Bir marta bir o'yinchiga immunitet berib, uni keyingi chiqarilishdan himoya qilishingiz mumkin."
    night_action = True
    action_type = "grant_immunity"


class QaroqchilarOvchisi(BaseRole):
    """Jangovar fuqaro — hushyor turib, tashrif buyurganlarni o'ldiradi"""
    name = "Jangovar fuqaro"
    title = "Qaroqchilar Ovchisi"
    emoji = "⚔️"
    team = "town"
    description = "Siz jangovar fuqarosiz! Kechasi hushyor turishingiz mumkin. Agar kimdir sizga tashrif buyursa, u o'ladi."
    night_action = True
    action_type = "alert"


class TorUstasi(BaseRole):
    """Izolyatorchi — bir o'yinchiga tashriflarni bloklaydi"""
    name = "Izolyatorchi"
    title = "To'r Ustasi"
    emoji = "🕸"
    team = "town"
    description = "Siz to'r ustasisiz! Kechasi bir o'yinchini to'r bilan o'rab, unga bo'lgan barcha tashriflarni bloklaysiz."
    night_action = True
    action_type = "trap"


class HayotQutqaruvchi(BaseRole):
    """Qutqaruvchi — bir marta chiqarilgan o'yinchini qutqaradi"""
    name = "Qutqaruvchi"
    title = "Hayot Qutqaruvchi"
    emoji = "🛟"
    team = "town"
    description = "Siz qutqaruvchisiz! Bir marta ovoz berish orqali chiqarilgan o'yinchini qutqarishingiz mumkin."
    night_action = False
    passive = True


class DengizSheri(BaseRole):
    """Kuchli fuqaro — bloklashga chidamli"""
    name = "Kuchli fuqaro"
    title = "Dengiz Sheri"
    emoji = "🦭"
    team = "town"
    description = "Siz kuchli fuqarosiz! Sizni hech kim bloklay olmaydi va sizning harakatingiz to'xtatilmaydi."
    night_action = False
    passive = True


class EgizakBaliqlar(BaseRole):
    """Egizaklar — birga yutadi/yutqazadi, bir-birini tanidi"""
    name = "Egizaklar"
    title = "Egizak Baliqlar"
    emoji = "🐟🐟"
    team = "town"
    description = "Siz egizaksiz! Yana bir egizak bor, siz uni bilasiz va u sizni biladi. Birga yutasiz yoki yutqazasiz."
    night_action = False
    passive = True


class Langarsos(BaseRole):
    """Temirchi — bir o'yinchiga zirh beradi"""
    name = "Temirchi"
    title = "Langarsos"
    emoji = "⚓️"
    team = "town"
    description = "Siz temirchisiz! Kechasi bir o'yinchiga zirh yasab berasiz va uni bir marta hujumdan himoya qilasiz."
    night_action = True
    action_type = "give_armor"


class Kashfiyotchi(BaseRole):
    """Sayyoh — bir o'yinchini kuzatib, uning targetini ko'radi"""
    name = "Sayyoh"
    title = "Kashfiyotchi"
    emoji = "🗺"
    team = "town"
    description = "Siz sayyohsiz! Kechasi bir o'yinchini kuzatasiz va uning kimga borganini bilib olasiz."
    night_action = True
    action_type = "track"


class SavdoKemasi(BaseRole):
    """Savdogar — o'yinchilar orasida qobiliyat almashadi"""
    name = "Savdogar"
    title = "Savdo Kemasi"
    emoji = "🛳"
    team = "town"
    description = "Siz savdogarsiz! Kechasi ikki o'yinchining qobiliyatlarini vaqtincha almashtirishingiz mumkin."
    night_action = True
    action_type = "trade_abilities"


class QadimiyChiganok(BaseRole):
    """Alkimyogar — har kecha iksir yaratadi"""
    name = "Alkimyogar"
    title = "Qadimiy Chig'anoq"
    emoji = "🐚"
    team = "town"
    description = "Siz alkimyogarsiz! Har kecha bir iksir (davolovchi yoki zaharlovchi) yaratib, uni bir o'yinchiga ishlatasiz."
    night_action = True
    action_type = "brew_potion"
