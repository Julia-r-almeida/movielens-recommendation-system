#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 10:22:42 2023

@author: julia
"""

avaliacoes = {
      'Ana': 
		{'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.5,
		 'Star Trek': 3.0, 
		 'Exterminador do Futuro': 3.5, 
		 'Norbit': 2.5, 
		 'Star Wars': 3.0},
	 
	  'Marcos': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 3.5, 
		 'Star Trek': 1.5, 
		 'Exterminador do Futuro': 5.0, 
		 'Star Wars': 3.0, 
		 'Norbit': 3.5}, 

	  'Pedro': 
	    {'Freddy x Jason': 2.5, 
		 'O Ultimato Bourne': 3.0,
		 'Exterminador do Futuro': 3.5, 
		 'Star Wars': 4.0},
			 
	  'Claudia': 
		{'O Ultimato Bourne': 3.5, 
		 'Star Trek': 3.0,
		 'Star Wars': 4.5, 
		 'Exterminador do Futuro': 4.0, 
		 'Norbit': 2.5},
				 
	  'Adriano': 
		{'Freddy x Jason': 3.0, 
		 'O Ultimato Bourne': 4.0, 
		 'Star Trek': 2.0, 
		 'Exterminador do Futuro': 3.0, 
		 'Star Wars': 3.0,
		 'Norbit': 2.0}, 

	  'Janaina': 
	     {'Freddy x Jason': 3.0, 
	      'O Ultimato Bourne': 4.0,
	      'Star Wars': 3.0, 
	      'Exterminador do Futuro': 5.0, 
	      'Norbit': 3.5},
			  
	  'Leonardo': 
	    {'O Ultimato Bourne':4.5,
             'Norbit':1.0,
	     'Exterminador do Futuro':4.0}
}
    
from math import sqrt

def euclidiana (usuario1, usuario2):
    similaridade = {}
    for item in avaliacoes[usuario1]:
        if item in avaliacoes[usuario2]:
            similaridade[item] = 1
    
    if len(similaridade) == 0: 
        return 0
    
    soma = sum([pow(avaliacoes[usuario1][item] - avaliacoes[usuario2][item], 2)
                for item in avaliacoes[usuario1] if item in avaliacoes[usuario2]])
    return 1/(1 + sqrt(soma))

def getSimilares(usuario):
    similaridade = [(euclidiana(usuario, outro), outro)
                    for outro in avaliacoes if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade

def getRecomendacoes(usuario):
    totais = {}
    somaSimilaridade = {}
    for outro in avaliacoes:
        if outro == usuario: continue
        similaridade = euclidiana(usuario, outro)
        if similaridade <= 0: continue 
        for item in avaliacoes[outro]:
            if item not in avaliacoes[usuario]: 
                totais.setdefault(item, 0)
                totais[item] += avaliacoes[outro][item] * similaridade
                somaSimilaridade.setdefault(item, 0)
                somaSimilaridade[item] += similaridade
    rankings = [(total / somaSimilaridade[item], item) for item, total in totais.items() ]
    rankings.sort()
    rankings.reverse()
    return rankings

# Carregando os dados do MovieLens
def carregaMovieLens(path = "/home/julia/Documentos/sistemas-recomendacao/ml-100k"):
    filmes = {}
    print(path)
    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    # print(filmes)
    
    base = {}
    for linha in open(path + '/u.data'):
        (usuario, idFilme, nota, tempo) = linha.split('\t')
        base.setdefault(usuario, {})
        base[usuario][filmes[idFilme]] = float(nota)
    return base