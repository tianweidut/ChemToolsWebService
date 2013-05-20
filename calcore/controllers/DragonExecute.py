# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: sytmac
'''

from calcore.controllers.Dragon import Dragon

def DragonDisposal(dragonFile):
    dragon=Dragon(dragonFile)
    dragon.DealWithMolFile()