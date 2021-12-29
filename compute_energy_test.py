# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 15:57:59 2021

@author: 190356
"""

import Utils

signal=[1,2,3,4,5]
energy=1+4+9+16+25
if(Utils.compute_energy(signal)==energy):
    print("La formule de calcul de l'énergie est bien respectée")
else :
    print("La formule n'est pas respectée")
