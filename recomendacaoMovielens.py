#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  2 18:06:56 2023

@author: julia
"""


from math import sqrt

base = {}

# Carregando os dados do MovieLens
def carregaMovieLens(path = "/home/julia/Documentos/sistemas-recomendacao/ml-100k"):
    filmes = {}

    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo

    for linha in open(path + '/u.data'):
        (usuario, idFilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idFilme]] = float(nota)

    return base

# Algoritmo
def euclidiana (usuario1, usuario2):
    similaridade = {}
    for item in base[usuario1]:
        if item in base[usuario2]:
            similaridade[item] = 1
    
    if len(similaridade) == 0: 
        return 0
    
    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    return 1/(1 + sqrt(soma))

def getSimilares(usuario):
    similaridade = [(euclidiana(usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:30]

def getRecomendacoesUsuarios(usuario):
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == usuario: continue
        similaridade = euclidiana(usuario, outro)
        if similaridade <= 0: continue 
        for item in base[outro]:
            if item not in base[usuario]: 
                totais.setdefault(item, 0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings = [(total / somaSimilaridade[item], item) for item, total in totais.items() ]
    rankings.sort()
    rankings.reverse()
    return rankings[0:30]

def calculaItensSimilares(base):
    result = {}
    for item in base:
        notas = getSimilares(base, item)
        result[item] = notas
    return result

# Função para recomendação por item
def getRecomendacoesItens (baseUsuario, similaridadeItens, usuario):
    notasUsuario = baseUsuario[usuario]
    notas = {}
    totalSimilaridade = {}
    for (item, nota) in notasUsuario.items():
        for (similaridade, item2) in similaridadeItens[item]:
            if item2 in notasUsuario: continue
            notas.setdefault(item2, 0)
            notas[item2] += similaridade * nota
            totalSimilaridade.setdefault(item2, 0)
            totalSimilaridade[item2] += similaridade
    rankings = [(score/totalSimilaridade[item], item) for item, score in notas.items()]
    rankings.sort()
    rankings.reverse()
    return rankings