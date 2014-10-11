import string
from itertools import permutations

NAMES = ["Catherine", "Krone", "Yasmine", "Valdes", "Nella", "Bartle", "George", "Kunzman",
"Marc", "Riel", "Shalanda", "Muirhead", "Hailey", "Fugitt", "Elease", "Kesterson", "Lottie",
"Pohlman", "Brittni", "WidellLeonore", "Berg", "Jamika", "Hackworth", "Antoinette", "Hellard",
"Karly", "Minick", "Laquita", "Witherell", "Jennette", "Hendley", "Trinh", "Pedretti",
"Trista", "Doyle", "Chu", "Sammons", "Grant", "Lenk", "Lael", "Beavers", "Raylene", "Shkreli",
"Heike", "Guerra", "Merideth", "Leatherwood", "Roger", "Haggard", "Francina", "Rich", "Karyn",
"Shur", "Harold", "Bramhall", "Romeo", "Blasi", "Joe", "Canipe", "Dario", "Reif", "Louisa",
"Bassi", "Nydia", "Jacko", "Wyatt", "Defrancisco", "Stan", "Gose", "Pamelia", "Naval", "Andra",
"Drexler", "Lula", "Hiatt", "Diedra", "Haar", "Goldie", "Crean", "Melonie", "Luz", "Morton",
"Drolet", "Kraig", "Kitzman", "Judson", "Felkins", "Norine", "Bulow", "Rocio", "Soper", 
"Justa", "Zambrano", "Pa", "Johnson", "Celestine", "Kell", "Malisa", "Dollinger", "Minh"]

ORGANIZATION_NAMES = list(string.ascii_uppercase)

PHONE_TESTING = [''.join(p) for p in permutations(string.digits)][:len(ORGANIZATION_NAMES)]

PROJECT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_uppercase[:15], 2)])[:78]

REPORT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_lowercase[:10], 4)])[:20]

COMMENT_REPORT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_lowercase[:10], 8)])[:40]
