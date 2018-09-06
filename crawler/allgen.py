import subprocess

fics = (
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25446", "Les Chasseurs de l'Ombre", "Malak", "shadow-hunters", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=22161", "Gardiens de l'Harmonie T.1 : La Mélodie de Vie", "Malak", "gardiens1", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad", "Malak", "x-squad", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=24837", "Pokémonis T.1 : La Pokéball Perdue", "Malak", "pokemonis1", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26045", "Pokémonis T.2 : L'Embrasement de l'Aura", "Malak", "pokemonis2", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25588", "Le Grand Essaimage T.1 : L'Éveil de l'essaim", "Malak", "essaim1", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=26053", "Le Grand Essaimage T.2 : Une Colonie d'Acier", "Malak", "essaim2", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=23864", "Cinhol, le Royaume Perdu", "Malak", "cinhol", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=24699", "Le Sauveur du Millénaire", "Malak", "sauveur", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=25526", "Le Destin des Primordiaux", "Malak", "primordiaux", "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc I : Team Cisaille", "Malak", "x-squad1", '--from="Chapitre 1"', '--to="Chapitre 17"', "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc II : L'Empire de Vriff", "Malak", "x-squad2", '--from="Chapitre 18"', '--to="Chapitre 42"', "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc III : Invasion", "Malak", "x-squad3", '--from="Chapitre 43"', '--to="Aquatros (8/8)"', "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc VI : Pokémon Méchas", "Malak", "x-squad4", '--from="Chapitre 81"', '--to="Chapitre 105"', "--clean"),
	("https://www.pokebip.com/index.php?phppage=membres/fanfics/affichage-fanfic&f=17488", "Team Rocket X-Squad, Arc V : Elysium", "Malak", "x-squad5", '--from="Chapitre 106"', '--to="Fruits de Vie (8/8)"', "--clean"),
)
