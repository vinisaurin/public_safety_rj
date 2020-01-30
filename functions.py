#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 23 11:33:55 2020

@author: viniciussaurin
"""

import numpy as np
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from itertools import chain

def remove_dups(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def draw_grouped_stacked_bars(dicionario, k, **kwargs):

    fig = plt.figure(figsize=(20, 10))
    plt.suptitle(kwargs['suptitle'],fontsize=24)
        
    # Criando a lista de cores que será utilizada
    by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))),
                             name)
                            for name, color in mcolors.CSS4_COLORS.items())
    n_saltos_cores = len(by_hsv)//(len(dicionario[k].tipo_crime.unique()))
    color_list = [c[1] for i,c in enumerate(by_hsv) if i%n_saltos_cores==0]
    
    # Plotando cada DataFrame
    for i, g in enumerate(dicionario[k].groupby('tipo_crime')):
            ax = sns.barplot(data=g[1],
                             x="Regiao",
                             y="Cumsum",
                             hue="vano",
                             color=color_list[i],
                             zorder=-i, # so first bars stay on top
                             edgecolor="k")
    
    
    crimes = list(dicionario[k].tipo_crime.unique())
    patch = [mpatches.Patch(color=color_list[i], label=crimes[i]) for i in range(len(crimes))]
    
    
    plt.legend(handles=patch)
    
    
    ax = plt.gca()
    pos = []
    for bar in ax.patches:
        pos.append(bar.get_x() + bar.get_width()/2.)
        
    pos = remove_dups(pos)
    ax.set_xticks(pos, minor=True)
    lab = list(chain.from_iterable([[ano]*len(dicionario[k].Regiao.unique()) for ano in list(dicionario[k].vano.unique())]))
    ax.set_xticklabels(lab, minor=True)

    
    
    ax.tick_params(axis='x', which='major', pad=30, size=0)
    plt.setp(ax.get_xticklabels(), rotation=0, fontsize=18)
    ax.xaxis.remove_overlapping_locs = False
    
    plt.xlabel('Região', fontsize=20)
    plt.ylabel('Total de ocorrências', fontsize=18)
    
    plt.savefig(kwargs['file_name'])
    
    plt.show()
    
def graf_barras(my_dict, regiao, df_total_abs, **kwargs):
    fig, ax = plt.subplots(figsize=(20,12))  
    crimes = my_dict[regiao].tipo_crime.drop_duplicates()
    margin_bottom = np.zeros(len(my_dict[regiao].mesano.drop_duplicates()))
    colors = ["#006D2C", "#31A354","#74C476","#000600", "#AAAAAA", "#CCCCCC" ]
    
    for num, crime in enumerate(crimes):
        values = list(my_dict[regiao][my_dict[regiao].tipo_crime == crime].loc[:, 'Total'])
    
        my_dict[regiao][my_dict[regiao].tipo_crime == crime].plot.bar(x='mesano',y='Total', ax=ax, stacked=True, 
                                        bottom = margin_bottom, color=colors[num], label= kwargs['ylabel'][num])
        margin_bottom += values
    
    totais = df_total_abs.query("Regiao == @regiao & mesano >= 201701")
    pos = []
    k=0
    for bar in ax.patches:
        pos.append(bar.get_x() + bar.get_width()/2.)
        if k <= (len(totais.Total)-1):
            ax.text(pos[-1]-.35, 1.04, "{:2.1f}".format(totais.Total.iloc[k]/1000), color='black', fontweight='bold', fontsize=10)
        k += 1
    
    plt.title(f'Evolução do percentual da distribuição de crimes da(o) {regiao}', fontsize=24)
    plt.xlabel('Ano Mes', fontsize=18)
    plt.xticks(rotation=45)
    plt.ylabel('Percentual', fontsize=18)
    plt.ylim(top=1.1)
    plt.legend(loc='upper left', bbox_to_anchor=(1,1), ncol=1)
    plt.savefig(kwargs['file_name'])
    plt.show()