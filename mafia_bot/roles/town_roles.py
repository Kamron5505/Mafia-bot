from .base_role import Role, register_role

register_role(Role(
    name="detective",
    title="Komissar / Sherif",
    emoji="🔱",
    team="town",
    description="Komissar. Kechasi biror o'yinchini tekshirib, uning qaysi jamoadaligini bilib oladi.",
    night_action=True,
    action_type="investigate",
))

register_role(Role(
    name="doctor",
    title="Doktor — Tabib",
    emoji="🐬",
    team="town",
    description="Doktor. Kechasi mafiya otgan odamni davolab, hayotini saqlab qoladi.",
    night_action=True,
    action_type="heal",
))

register_role(Role(
    name="townsfolk",
    title="Oddiy Tinch Aholi",
    emoji="⚓️",
    team="town",
    description="Oddiy tinch aholi. Kechasi uxlashadi, kunduzi mantiqan o'ylab, ovoz berish orqali mafiyani topishga harakat qilishadi.",
    passive=True,
))

register_role(Role(
    name="bodyguard",
    title="Tansoqchi — Qo'riqchi",
    emoji="🛡",
    team="town",
    description="Tansoqchi. Kechasi biror o'yinchini himoya qiladi. Agar o'sha odam otilsa, tansoqchi uning o'rniga o'ladi.",
    night_action=True,
    action_type="guard",
))

register_role(Role(
    name="mayor",
    title="Donishmand Toshbaqa",
    emoji="🐢",
    team="town",
    description="Mer. Ovozi ikki hisoblanadi.",
    passive=True,
))

register_role(Role(
    name="priest",
    title="Dengiz Farishtasi",
    emoji="🕊",
    team="town",
    description="Ruhoniy. Bir o'yinchining tomonini ochib bera oladi.",
    night_action=True,
    action_type="reveal",
    max_uses=1,
))

register_role(Role(
    name="hooker",
    title="Suvparisi",
    emoji="🧜‍♀️",
    team="town",
    description="Fohisha. Kechagi harakatni bloklaydi.",
    night_action=True,
    action_type="block",
))

register_role(Role(
    name="journalist",
    title="Kema To'tiqushi",
    emoji="🦜",
    team="town",
    description="Jurnalist. Bir sirni e'lon qilish qobiliyatiga ega.",
    night_action=True,
    action_type="publish",
    max_uses=1,
))

register_role(Role(
    name="watcher",
    title="Dengiz Burguti",
    emoji="🦅",
    team="town",
    description="Kuzatuvchi. Kim kimga tashrif buyurganini ko'radi.",
    night_action=True,
    action_type="watch",
))

register_role(Role(
    name="jailer",
    title="Sodiq Qisqichbaqa",
    emoji="🦀",
    team="town",
    description="Qorovul. Bir o'yinchini qamab qo'yadi va himoyalaydi.",
    night_action=True,
    action_type="jail",
))

register_role(Role(
    name="hunter",
    title="G'avvos",
    emoji="🤿",
    team="town",
    description="Ovchi. O'lganda bir o'yinchini otib o'ldiradi.",
    passive=True,
))

register_role(Role(
    name="guard",
    title="Ko'k Kit",
    emoji="🐳",
    team="town",
    description="Gvardiyachi. Birinchi mafiya hujumiga chidamli.",
    passive=True,
))

register_role(Role(
    name="judge",
    title="Okean Qozisi",
    emoji="⚖️",
    team="town",
    description="Sudya. Bir ovozni bekor qilish qobiliyatiga ega.",
    night_action=False,
    action_type="cancel_vote",
    max_uses=1,
))

register_role(Role(
    name="prosecutor",
    title="Bolg'abosh Akula",
    emoji="🔨",
    team="town",
    description="Prokuror. Ovozsiz nomzodni sudga topshira oladi.",
    night_action=False,
    action_type="force_nominate",
    max_uses=1,
))

register_role(Role(
    name="investigator",
    title="Mayoqchi",
    emoji="🔍",
    team="town",
    description="Tekshiruvchi. Rol kategoriyasini aniqlaydi.",
    night_action=True,
    action_type="investigate_category",
))

register_role(Role(
    name="sponsor",
    title="Xazinabon",
    emoji="💰",
    team="town",
    description="Homiy. Bir o'yinchiga immunitet beradi.",
    night_action=True,
    action_type="grant_immunity",
    max_uses=1,
))

register_role(Role(
    name="veteran",
    title="Qaroqchilar Ovchisi",
    emoji="⚔️",
    team="town",
    description="Jangovar fuqaro. Hushyorlikka kirsa, tashrifchilarni o'ldiradi.",
    night_action=True,
    action_type="alert",
    max_uses=3,
))

register_role(Role(
    name="trapper",
    title="To'r Ustasi",
    emoji="🕸",
    team="town",
    description="Izolyatorchi. Bir o'yinchiga barcha tashriflarni bloklaydi.",
    night_action=True,
    action_type="trap",
))

register_role(Role(
    name="lifesaver",
    title="Hayot Qutqaruvchi",
    emoji="🛟",
    team="town",
    description="Qutqaruvchi. Ovoz berishdan chiqarilgan o'yinchini tiriltira oladi.",
    night_action=False,
    action_type="save",
    max_uses=1,
))

register_role(Role(
    name="lion",
    title="Dengiz Sheri",
    emoji="🦭",
    team="town",
    description="Kuchli fuqaro. Rol bloklashga immunitetli.",
    passive=True,
))

register_role(Role(
    name="twins",
    title="Egizak Baliqlar",
    emoji="🐟🐟",
    team="town",
    description="Egizaklar. Birga yutqazishadi/yutыshadi, bir-birini taniydi.",
    passive=True,
))

register_role(Role(
    name="blacksmith",
    title="Langarsoz",
    emoji="⚓️",
    team="town",
    description="Temirchi. Bir o'yinchiga zirh beradi.",
    night_action=True,
    action_type="armor",
    max_uses=1,
))

register_role(Role(
    name="explorer",
    title="Kashfiyotchi",
    emoji="🗺",
    team="town",
    description="Sayyoh. O'yinchini kuzatib, uning nishonini ko'radi.",
    night_action=True,
    action_type="track",
))

register_role(Role(
    name="merchant",
    title="Savdo Kemasi",
    emoji="🛳",
    team="town",
    description="Savdogar. Ikki o'yinchining qobiliyatini almashtiradi.",
    night_action=True,
    action_type="trade",
))

register_role(Role(
    name="alchemist",
    title="Qadimiy Chig'anoq",
    emoji="🐚",
    team="town",
    description="Alkimyogar. Har kecha ikkisidan bir ikkirni yaratadi.",
    night_action=True,
    action_type="create_potion",
))
