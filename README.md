# p6_installation_paquet
Ce script est créé dans le cadre d'une formation openclassrooms administrateur infrastructure et cloud
Il permet, sur une serie de postes distant sous debian:
  *D'établir une connexion ssh avec mot de passe.
  *De vérifier le système d'exploitation.
  *De vérifier l'espace disque disponible.
  *De vérifier l'emplacement de sauvegarde.
  *De copier un fichier (option).
  *D'installer un paquet.

## Prérequis
Pour utiliser ce script, il faut tout d'abord installer python3-paramikode et que la session administrateur soit identique sur tous les postes distant.
 
## Configuration
Plusieurs données sont à modifier 
 * Dans le fichier donnees.py
    * les différents emplacement et le nom du document à transférer
    * les identifiants de session
    * le port ouvert pour ssh (par defaut le 22)
    * les ip des postes à modifier
 
 * Dans p6_installation_paquet
    * Warning disk, qui correspond, en G, à l'espace disque nécessaire pour effectuer les installations
 
 
 * Au lancement du sript
    * Il faut renseigner en argument le paquet à installer (expl : python3 p6_modif_prog nano)

## Utilisation
Lors du lancement, une serie d'information sera affichée.
  * la machine cible
  * Si la connexion est établie
  * la verification de l'espace disque
  * la verification des chemins serveur et clients
  * si le transfert est effectué
  * si l'installation est effectuée
  * la fin du script

## Contribution
Vous pouvez contribuer comme vous le souhaitez (ajouter des fonctionnalités, optimiser, traduire, etc ...). Vous pouvez également aider en signalant des bogues ou en suggérant des améliorations.

## Contact
Pour plus d'informations ou d'aide sur l'utilisation de p6_installation_paquet, n'hésitez pas à me contacter à pseuso[at]live.fr.
