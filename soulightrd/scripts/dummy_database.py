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
"Justa", "Zambrano", "Pa", "Johnson", "Celestine", "Kell", "Malisa", "Dollinger", "Minh",
"Brianne", "Kates", "Isaura", "Stanton", "Fermina", "Leto", "Carmelina", "Badalamenti",
"Marlene", "Timmer", "Sherita", "Maynez", "Erline", "Balducci", "Laveta", "Mazzeo", "Cindi",
"Livengood", "Ana", "Bassett", "Isabell", "Newbold", "Leila", "Prochnow", "Deandrea",
"Gaertner", "Roxie", "Paquin", "Penni", "Quintanar", "Maye", "Polen", "Akilah", "Wince",
"Mariette", "Freed", "Cordia", "Moser", "Yi", "Nappi", "Dexter", "Deboer", "Herta","Newbill",
"Jenna", "Bronk", "Kiersten", "Walls", "Kira", "Leech", "Carlyn", "Tuner", "Gabriel", 
"Mickelsen", "Shantay", "Engelman", "Bernard", "Carstensen", "Xiomara", "Iannuzzi", "Sharron",
"Weimar", "Vera", "Tilley", "Grace", "Frankel", "Jenise", "Addy", "Cherilyn", "Platt", "Logan",
"Smolen", "Rhea", "Moreira", "Denae", "Marro", "Slyvia", "Caulkins", "Jame", "Strauch", 
"Ruthanne", "Griest", "Jeffery", "Ruppe", "Nolan", "Creasy", "Jada", "Pilger", "Ulysses",
"Theus", "Albert", "Biggins", "Deloras", "Brackin", "Rikki", "Culton", "Marquitta", "Fabre",
"Herman", "Leverette"]

ORGANIZATION_NAMES = list(string.ascii_uppercase)

PHONE_TESTING = [''.join(p) for p in permutations(string.digits)][:len(ORGANIZATION_NAMES)]

PROJECT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_uppercase[:15], 2)])[:78]

REPORT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_lowercase[:10], 4)])[:20]

COMMENT_REPORT_TESTING = sorted(
	["".join(x) for x in permutations(string.ascii_lowercase[:10], 8)])[:40]
