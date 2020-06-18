#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 17 22:58:08 2020

Versão 0: Giovanni Guarnieri
Versão 1: Renato H. F. Branco
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from mpl_toolkits.mplot3d import Axes3D
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans

def makeK(d,ilist, title,report):
    #d: sinal contendo variância, assimetria e curtose já calculados
    #ilist: nome de cada sinal
    #title: título do gráfico
    print(ilist)
    d=np.array(d)
    kk=pd.DataFrame({'Variance': d[:,0], 'Skewness': d[:,1], 'Kurtosis': d[:,2]})
    K=10
    model=KMeans()
    visualizer = KElbowVisualizer(model, k=(1,K))
    kIdx=visualizer.fit(kk)        # Fit the data to the visualizer
    visualizer.show()
    plt.draw()
    report.add_fig()        # Finalize and render the figure
    kIdx=kIdx.elbow_value_
    model=KMeans(n_clusters=kIdx).fit(kk)
    
    # scatter plot
    fig = plt.figure()
    ax = Axes3D(fig) #.add_subplot(111))
    cmap = plt.get_cmap('gnuplot')
    clr = [cmap(i) for i in np.linspace(0, 1, kIdx)]
    for i in range(0,kIdx):
        ind = (model.labels_==i)
        ax.scatter(d[ind,2],d[ind,1], d[ind,0], s=30, c=clr[i], label='Cluster %d'%i)
    ax.set_xlabel("Kurtosis")
    ax.set_ylabel("Skew")
    ax.set_zlabel("Variance")
    plt.title(title+': KMeans clustering with K=%d' % kIdx)
    plt.legend()
    #plt.savefig(title+"clusters.png")
    plt.draw()
    #d=pd.DataFrame({'Variance': d[:,0], 'Skewness': d[:,1], 'Kurtosis': d[:,2], 'Alpha': d[:,3], 'Beta': d[:,4], "Psi": d[:,5], "Cluster": model.labels_}, index=ilist)
    #return d
    return kIdx

