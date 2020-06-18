#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 23:29:08 2020

@author: renato h. f. branco
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import genextreme as gev
from scipy.stats import norm as nrm

#############################################
# Gráfico do ajuste Gaussiana e GEV
#############################################

def plotgev(dados,ndivh,titulo):
    plt.figure()
    shape, loc, scale = gev.fit(dados)
    
    plt.hist(dados, bins=ndivh, density=True)
    xmin, xmax = plt.xlim()
    
    xx = np.linspace(xmin, xmax, num=100)
    yy = gev.pdf(xx, shape, loc, scale)
    
    plt.title(titulo+" | GEV")
    
    plt.xlabel("")
    plt.ylabel("")

    plt.plot(xx, yy, 'orange')
    plt.draw()

def plotgaussiana(dados,ndivh,titulo):
    plt.figure()
    mean,std=nrm.fit(dados)
    plt.hist(dados, bins=ndivh, density=True)
    xmin, xmax = plt.xlim()
    
    xx = np.linspace(xmin, xmax, 100)
    yy = nrm.pdf(xx, mean, std)
    
    plt.title(titulo+" | Gaussian")
    
    plt.plot(xx, yy, 'orange')
    plt.draw()
    
def plotajuste(tipoajuste,dados,divh,titulo):
    #tipo do ajuste = 1: gaussiana
    #tipo do ajuste = 2: GEV
    #divh: número de divisões do histograma
    #titulo: título do gráfico
    
    
    if tipoajuste==1:
        plotgaussiana(dados,divh,titulo)
        
    if tipoajuste==2:
        plotgev(dados,divh,titulo)
        
def plotajuste_completo(dados,ndivh,titulo):

    plt.figure()

    #dados e histograma do ajuste    
    plt.hist(dados, bins=ndivh, density=True)
    xmin, xmax = plt.xlim()
    
    
    xx = np.linspace(xmin, xmax, num=100)

    #calcula ajuste GEV
    shape, loc, scale = gev.fit(dados)
    ygev = gev.pdf(xx, shape, loc, scale)
    plt.plot(xx, ygev, 'orange')
    
    #calcula ajuste gaussiana
    mean,std=nrm.fit(dados)
    ygaus = nrm.pdf(xx, mean, std)
    plt.plot(xx, ygaus, 'green')
    
    
    plt.title(titulo+" | GEV (orange) - Gaussian (green)")
    
    plt.draw()
        
def plothistograma(dados,ndivh,titulo,densidade=False):
    plt.figure()
    plt.hist(dados, bins=ndivh, density=densidade)
    plt.title(titulo)
    
    plt.draw()