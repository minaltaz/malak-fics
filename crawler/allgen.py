import sys
import subprocess

fics = {
	"shadowhunters": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25446", "Les Chasseurs de l'Ombre", "Malak", "shadow-hunters", "--clean"),
	"gardiens1": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=22161", "Gardiens de l'Harmonie T.1 : La Mélodie de Vie", "Malak", "gardiens1", "--clean"),
	"xsquad": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad", "Malak", "x-squad", "--clean"),
	"pokemonis1": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=24837", "Pokémonis T.1 : La Pokéball Perdue", "Malak", "pokemonis1", "--clean"),
	"pokemonis2": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26045", "Pokémonis T.2 : L'Embrasement de l'Aura", "Malak", "pokemonis2", "--clean"),
	#"essaim1": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25588", "Le Grand Essaimage T.1 : L'Éveil de l'essaim", "Malak", "essaim1", "--clean"),
	#"essaim2": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26053", "Le Grand Essaimage T.2 : Une Colonie d'Acier", "Malak", "essaim2", "--clean"),
	"cinhol": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=23864", "Cinhol, le Royaume Perdu", "Malak", "cinhol", "--clean"),
	"sauveur": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=24699", "Le Sauveur du Millénaire", "Malak", "sauveur", "--clean"),
	"primordiaux": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25526", "Le Destin des Primordiaux", "Malak", "primordiaux", "--clean"),
	"apotres": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26382", "Les Apôtres d'Erubin", "Malak", "apotres", "--clean"),
	"destinee": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26379", "Entre Destinée et Fatalité", "Malak", "destinee", "--clean"), 
	"xsquad1": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc I : Team Cisaille", "Malak", "x-squad1", '--from="Chapitre 1 :"', '--to="Chapitre 17 :"', "--clean"),
	"xsquad2": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc II : L'Empire de Vriff", "Malak", "x-squad2", '--from="Chapitre 18 :"', '--to="Chapitre 42 :"', "--clean"),
	"xsquad3": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc III : Invasion", "Malak", "x-squad3", '--from="Chapitre 43 :"', '--to="Aquatros (8/8)"', "--clean"),
	"xsquad4": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc VI : Pokémon Méchas", "Malak", "x-squad4", '--from="Chapitre 81 :"', '--to="Chapitre 105 :"', "--clean"),
	"xsquad5": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc V : Elysium", "Malak", "x-squad5", '--from="Chapitre 106 :"', '--to="Fruits de Vie (8/8)"', "--clean"),
	"xsquad6": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc VI : Agents de la Corruption", "Malak", "x-squad6", '--from="Chapitre 161 :"', '--to="Chapitre 187 :"', "--clean"),
	"xsquad7": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc VII : GSR", "Malak", "x-squad7", '--from="Chapitre 188 :"', '--to="cule d\'or (8/8)"', "--clean"),
	"xsquad8": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc VIII : Venamia", "Malak", "x-squad8", '--from="Chapitre 238 :"', '--to="Le destin des Primordiaux"', "--clean"),
	"xsquad9": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc IX : Guerre Mondiale", "Malak", "x-squad9", '--from="Chapitre 301 :"', '--to="Chapitre 370 :"', "--clean"),
        "xsquad10": ("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc X : Jugement Dernier", "Malak", "x-squad10", '--from="Chapitre 371 :"', "--clean")
}

if __name__ == "__main__":
	if len(sys.argv) == 1:
		opt = "all"
	else:
		opt = sys.argv[1]
	if opt == "all":
		for name in fics:
			subprocess.run(("python3", "pokebip_fic_crawler.py") + fics[name] + ("--verbose", ))
	elif opt == "xsquadarcs":
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad1"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad2"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad3"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad4"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad5"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad6"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad7"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad8"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad9"])
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics["xsquad10"])
	else:
		subprocess.run(("python3", "pokebip_fic_crawler.py") + fics[opt] + ("--verbose",))
