ADT
- Parfois les contrôles de type de base sont trop spécifiques. Ex : TypeError: '2021-03-24 05:03:30' for '<Att(type=<class 'ADT.basictypes.datetime'>, default=None, mandatory=<class 'ADT.hbds.Att.required'>)>named begin'. Should be '<class 'ADT.basictypes.datetime'>' instead of '<class 'datetime.datetime'>'
 
# Versions
* 0.4:
	* ré-écriture des *foncteurs* avec le module *pipe*
	* parsing des *date, time et datetime* avec le module *dateutils* dans *basictypes*
* 0.3: 
  * ajout des couleurs, prise en compte de certains formats de chaine de caractères pour les datetime et date, 
  * correction d'un bug sur les foncteurs *psc et nsc* si null. 
  * Ajout d'une gestion de cache à l'essai dans *util*
  * début d'un dev pour la génération d'IHM avec pySimpleGUI :)
* 0.2: archivage et partage sur pip
* 0.1: début. Non archivé