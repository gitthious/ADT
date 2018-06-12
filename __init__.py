# -*- coding: utf-8 -*-
"""
TODO:
 * Tester encore dans tous les cas du data model de pyhon
 * Sauvegarder le objectCtrl.ui pour pouvoir le retoucher avec Designer

Réflexions:
    PyClass -> attrs non typés à priori
    ADTClass -> attrs typés

Pour les deux types de classes, il faudrait:
    - Gérer les attrs modifiables et non modifaibles
    - pouvoir représenter tous les attrs d'un objet ou une partie seulement
       * que public
       * pas callable
       * une liste choisie
    - A la génération de l'IHM, on doit générer un .ui et être capable ensuite de
      reprendre avec Deisgner. La régénération doit tenir compte des modifications
      manuelles.
    - le modèle doit être full MVC
    - représentation des types simples (en faire une liste) et complexes (autres)
    - On a usuellement une représentation de type formulaire d'un objet
      et une autre plutôt linéaire - qui s'intégre dans une liste d'objets.
    - L'accès à la représentation d'un objet complexe peut se faire de manière:
       * directe cad emboitée dans la représentation mère
       * indirecte ou référencée à l'aide d'un bouton par exemple.

See:
    http://www.google.fr/url?sa=t&rct=j&q=&esrc=s&source=video&cd=3&cad=rja&ved=0CD8QtwIwAg&url=http%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DsPiWg5jSoZI&ei=DHD8UpnFAseG0AWBn4GoAg&usg=AFQjCNGDRP9_S_1s7cTPcNmlnc2MuLy73Q&sig2=lEVOr8SHi4Gytm0xN9b3wg&bvm=bv.61190604,d.d2k
    http://pyvideo.org/video/1760/encapsulation-with-descriptors
    http://pyvideo.org/video/1779/pythons-class-development-toolkit
    http://python-3-patterns-idioms-test.readthedocs.org/en/latest/Metaprogramming.html
    http://www.dabeaz.com/py3meta/

V0.1: première version sous py27
V0.2: passage sous py3 et GitHub

"""


