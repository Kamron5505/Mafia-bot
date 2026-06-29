import random
from typing import List

from roles.base_role import BaseRole
from roles.mafia_roles import (
    OkeanQirali, Akula, QaroqchilarSardori, ZaharliFugu,
    GigantKalmar, QisqichbaqaOGri, ChaqquvchiMeduza, ShurSuvTimsohi,
    Qilichbaliq, XameleonBaliq, QotilKit, DengizTubisiz,
    MinaBaliq, ZilzilaviySkat, DengizChayoni, KemaKalamushi,
    OlikDengizchi, DengizIloni, Piranya, IfloslanganSuv,
)
from roles.town_roles import (
    NeptunSoqchisi, QutqaruvchiDelfin, Dengizchi, MarjonQoriqchisi,
    DonishmandToshbaqa, DengizFarishtasi, Suvparisi, KemaTotiqushi,
    DengizBurguti, SodiqQisqichbaqa, Gavvos, KokKit,
    OkeanQozisi, BolgaboshAkula, Mayoqchi, Xazinabon,
    QaroqchilarOvchisi, TorUstasi, HayotQutqaruvchi, DengizSheri,
    EgizakBaliqlar, Langarsos, Kashfiyotchi, SavdoKemasi,
    QadimiyChiganok,
)
from roles.neutral_roles import (
    MarvaridJufti, DengizBoroni, AyyorOktopus, SuvostiVulgoni,
    Girdob, ChokkanKemaRuhi, MuzlaganDengizchi, Xarpunchi,
    BermudAsiri, YunonOlovi, SuvostiKorshapalagi, ZaharliSuvoti,
    Kraken, DengizQimorbozi, Sarob
)


# Barcha rollar ro'yxati
ALL_MAFIA_ROLES = [
    OkeanQirali, Akula, QaroqchilarSardori, ZaharliFugu,
    GigantKalmar, QisqichbaqaOGri, ChaqquvchiMeduza, ShurSuvTimsohi,
    Qilichbaliq, XameleonBaliq, QotilKit, DengizTubisiz,
    MinaBaliq, ZilzilaviySkat, DengizChayoni, KemaKalamushi,
    OlikDengizchi, DengizIloni, Piranya, IfloslanganSuv
]

ALL_TOWN_ROLES = [
    NeptunSoqchisi, QutqaruvchiDelfin, Dengizchi, MarjonQoriqchisi,
    DonishmandToshbaqa, DengizFarishtasi, Suvparisi, KemaTotiqushi,
    DengizBurguti, SodiqQisqichbaqa, Gavvos, KokKit,
    OkeanQozisi, BolgaboshAkula, Mayoqchi, Xazinabon,
    QaroqchilarOvchisi, TorUstasi, HayotQutqaruvchi, DengizSheri,
    EgizakBaliqlar, Langarsos, Kashfiyotchi, SavdoKemasi,
    QadimiyChiganok
]

ALL_NEUTRAL_ROLES = [
    MarvaridJufti, DengizBoroni, AyyorOktopus, SuvostiVulgoni,
    Girdob, ChokkanKemaRuhi, MuzlaganDengizchi, Xarpunchi,
    BermudAsiri, YunonOlovi, SuvostiKorshapalagi, ZaharliSuvoti,
    Kraken, DengizQimorbozi, Sarob
]


def select_roles(player_count: int) -> List[BaseRole]:
    """
    O'yin uchun 6 ta rolni muvozanatli tanlash.

    Algoritm:
    1. 1-2 ta mafiya roli
    2. 2-3 ta shahar roli
    3. 0-1 ta neytral rol
    4. Qolgan bo'sh joylar Dengizchi (oddiy fuqaro) bilan to'ldiriladi
    """
    mafia_pool = ALL_MAFIA_ROLES.copy()
    town_pool = ALL_TOWN_ROLES.copy()
    neutral_pool = ALL_NEUTRAL_ROLES.copy()

    random.shuffle(mafia_pool)
    random.shuffle(town_pool)
    random.shuffle(neutral_pool)

    selected_roles = []

    # 1-2 mafiya
    mafia_count = random.randint(1, min(2, len(mafia_pool)))
    for i in range(mafia_count):
        selected_roles.append(mafia_pool[i]())

    # 2-3 shahar
    remaining = 6 - len(selected_roles)
    town_target = min(remaining - 1, 3)
    town_count = random.randint(2, min(town_target, len(town_pool)))
    for i in range(town_count):
        selected_roles.append(town_pool[i]())

    # 0-1 neytral
    remaining = 6 - len(selected_roles)
    if remaining > 0 and random.random() < 0.5:
        selected_roles.append(neutral_pool[0]())

    # Qolgan joylarni Dengizchi bilan to'ldiramiz
    while len(selected_roles) < 6:
        selected_roles.append(Dengizchi())

    random.shuffle(selected_roles)

    return selected_roles


def get_role_by_name(name: str) -> BaseRole:
    """Rol nomi bo'yicha rol klassini qaytaradi"""
    for role_class in ALL_MAFIA_ROLES + ALL_TOWN_ROLES + ALL_NEUTRAL_ROLES:
        if role_class.name == name or role_class.title == name:
            return role_class()
    return Dengizchi()


def get_all_roles_by_category() -> dict:
    """Barcha rollarni kategoriya bo'yicha qaytaradi"""
    return {
        "mafia": [cls() for cls in ALL_MAFIA_ROLES],
        "town": [cls() for cls in ALL_TOWN_ROLES],
        "neutral": [cls() for cls in ALL_NEUTRAL_ROLES],
    }
