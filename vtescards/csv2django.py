import csv
from api.models import LibraryCard, CryptCard

LIBRARY_CSV = 'data/vteslib.csv'
CRYPT_CSV = 'data/vtescrypt.csv'

print("Getting library cards...")
n = 0
with open(LIBRARY_CSV, 'r', encoding='utf8') as csv_library:
    next(csv_library)
    reader = csv.reader(csv_library, delimiter=',')
    for row in reader:
        a = 1
        lc = LibraryCard(id=row[0],
                         name=row[1],
                         aka=row[2] if row[2] else None,
                         alias=row[1],
                         card_type=row[3],
                         clan=row[4],
                         discipline=row[5] if row[5] else None,
                         pool_cost=row[6] if row[6] else "0",
                         blood_cost=row[7] if row[7] else "0",
                         conviction_cost=row[8] if row[8] else "0",
                         burn_option=bool(row[9]),
                         card_text=row[10],
                         flavor_text=row[11] if row[11] else None,
                         publish_set=row[12] if row[12] else None,
                         requirement=row[13] if row[13] else None,
                         banned=int(row[14]) if row[14] else None,
                         artist=row[15],
                         capacity=row[16] if row[16] else None,
                         draft=row[17] if row[17] else None,
                         )
        lc.save()
        n += 1
        if n % 250 == 0:
            print("\t" + str(n))

print("Getting crypt cards...")
n = 0
with open(CRYPT_CSV, 'r', encoding='utf8') as csv_crypt:
    next(csv_crypt)
    reader = csv.reader(csv_crypt, delimiter=',')
    for row in reader:
        cc = CryptCard(id=row[0],
                       name=row[1],
                       aka=row[2] if row[2] else None,
                       alias=row[1] if not bool(row[5]) else row[1] + " (ADV)",
                       card_type=row[3],
                       clan=row[4],
                       advanced=bool(row[5]),
                       group_id=row[6],
                       capacity=int(row[7]),
                       disciplines=row[8],
                       card_text=row[9],
                       publish_set=row[10],
                       title=row[11] if row[11] else None,
                       banned=int(row[12]) if row[12] else None,
                       artist=row[13],
                       abombwe=int(row[14]) if row[14] else 0,
                       animalism=int(row[15]) if row[15] else 0,
                       auspex=int(row[16]) if row[16] else 0,
                       celerity=int(row[17]) if row[17] else 0,
                       chimerstry=int(row[18]) if row[18] else 0,
                       daimoinon=int(row[19]) if row[19] else 0,
                       dementation=int(row[20]) if row[20] else 0,
                       dominate=int(row[21]) if row[21] else 0,
                       fortitude=int(row[22]) if row[22] else 0,
                       melpominee=int(row[23]) if row[23] else 0,
                       mytherceria=int(row[24]) if row[24] else 0,
                       necromancy=int(row[25]) if row[25] else 0,
                       obeah=int(row[26]) if row[26] else 0,
                       obfuscate=int(row[27]) if row[27] else 0,
                       obtenebration=int(row[28]) if row[28] else 0,
                       potence=int(row[29]) if row[29] else 0,
                       presence=int(row[30]) if row[30] else 0,
                       protean=int(row[31]) if row[31] else 0,
                       quietus=int(row[32]) if row[32] else 0,
                       sanguinus=int(row[33]) if row[33] else 0,
                       serpentis=int(row[34]) if row[34] else 0,
                       spiritus=int(row[35]) if row[35] else 0,
                       temporis=int(row[36]) if row[36] else 0,
                       thanatosis=int(row[37]) if row[37] else 0,
                       thaumaturgy=int(row[38]) if row[38] else 0,
                       valeren=int(row[39]) if row[39] else 0,
                       vicissitude=int(row[40]) if row[40] else 0,
                       visceratika=int(row[41]) if row[41] else 0
                       )
        cc.save()
        n += 1
        if n % 250 == 0:
            print("\t" + str(n))

print("Done!")
