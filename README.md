# DrawNamesForChristmas
Draw names and presents for christmas. 

For a list of 2 types of presents, their are 2 draws.
People cannot offer twice to the same personne.
People offer and receive only one present of each type.
If specified, they cannot offer to specific personnes (here p5 <-> p4, and p2 <->p3).

An email is sent to each person with the peoples to gift. But they don't know who will gift them.

## Configuration
Open [noel.py](noel.py) and update fields 'personnes', 'types' and mail configuration.

## Usage
`python noel.py`

## Output:

```
Resultat du tirage:
	 personne1 offre un    taille1 cadeau à  personne5 sur le thème     theme1
	 personne2 offre un    taille1 cadeau à  personne4 sur le thème     theme1
	 personne5 offre un    taille1 cadeau à  personne2 sur le thème     theme1
	 personne3 offre un    taille1 cadeau à  personne1 sur le thème     theme1
	 personne4 offre un    taille1 cadeau à  personne3 sur le thème     theme1
Resultat du tirage:
	 personne1 offre un    taille2 cadeau à  personne4 sur le thème     theme2
	 personne2 offre un    taille2 cadeau à  personne1 sur le thème     theme2
	 personne5 offre un    taille2 cadeau à  personne3 sur le thème     theme2
	 personne3 offre un    taille2 cadeau à  personne5 sur le thème     theme2
	 personne4 offre un    taille2 cadeau à  personne2 sur le thème     theme2
```