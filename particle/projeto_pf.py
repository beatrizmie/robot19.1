#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Esta classe deve conter todas as suas implementações relevantes para seu filtro de partículas
"""

from pf import Particle, create_particles, draw_random_sample
from scipy.stats import norm
import numpy as np
import inspercles # necessário para o a função nb_lidar que simula o laser
import math



largura = 775 # largura do mapa
altura = 748  # altura do mapa

# Robo
robot = Particle(largura/2, altura/2, math.pi/4, 1.0)

# Nuvem de particulas
particulas = []

num_particulas = 200


# Os angulos em que o robo simulado vai ter sensores
angles = np.linspace(0.0, 2*math.pi, num=8, endpoint=False)

# Lista mais longa
movimentos_longos = [[-10, -10, 0], [-10, 10, 0], [-10,0,0], [-10, 0, 0],
              [0,0,math.pi/12.0], [0, 0, math.pi/12.0], [0, 0, math.pi/12],[0,0,-math.pi/4],
              [-5, 0, 0],[-5,0,0], [-5,0,0], [-10,0,0],[-10,0,0], [-10,0,0],[-10,0,0],[-10,0,0],[-15,0,0],
              [0,0,-math.pi/4],[0, 10, 0], [0,10,0], [0, 10, 0], [0,10,0], [0,0,math.pi/8], [0,10,0], [0,10,0], 
              [0,10,0], [0,10,0], [0,10,0],[0,10,0],
              [0,0,-math.radians(90)],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],[math.cos(math.pi/3)*10, math.sin(math.pi/3),0],
              [math.cos(math.pi/3)*10, math.sin(math.pi/3),0]]

# Lista curta
movimentos_curtos = [[-10, -10, 0], [-10, 10, 0], [-10,0,0], [-10, 0, 0]]

movimentos_relativos = [[0, -math.pi/3],[10, 0],[10, 0], [10, 0], [10, 0],[15, 0],[15, 0],[15, 0],[0, -math.pi/2],[10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [0, -math.pi/2], 
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [0, -math.pi/2], 
                       [10,0], [0, -math.pi/4], [10,0], [10,0], [10,0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0],
                       [10,0], [10, 0], [10, 0], [10, 0], [10, 0], [10, 0]]



movimentos = movimentos_relativos



def cria_particulas(minx=0, miny=0, maxx=largura, maxy=altura, n_particulas=num_particulas):

	"""
		Cria uma lista de partículas distribuídas de forma uniforme entre minx, miny, maxx e maxy
	"""

	for i in range(num_particulas):
		x = np.random.uniform(minx, maxx)
		y = np.random.uniform(miny, maxy)
		theta = np.random.uniform(0, 2*math.pi)
		p = Particle(x, y, theta, 1.0)
		particulas.append(p)

	return particulas

def move_particulas(particulas, movimento):
	"""
		Recebe um movimento na forma [deslocamento, theta]  e o aplica a todas as partículas
		Assumindo um desvio padrão para cada um dos valores
		Esta função não precisa devolver nada, e sim alterar as partículas recebidas.

		Sugestão: aplicar move_relative(movimento) a cada partícula

		Você não precisa mover o robô. O código fornecido pelos professores fará isso

	"""

	for p in particulas:
		while movimento[0]!=0:
			deslocamento = np.random.normal(movimento[0], 3)
			theta = np.random.normal(movimento[1], 2*math.pi/180)
			p.move_relative(movimento)

	return particulas

def leituras_laser_evidencias(robot, particulas):
	"""
		Realiza leituras simuladas do laser para o robo e as particulas
		Depois incorpora a evidência calculando
		P(H|D) para todas as particulas
		Lembre-se de que a formula $P(z_t | x_t) = \alpha \prod_{j}^M{e^{\frac{-(z_j - \hat{z_j})}{2\sigma^2}}}$ 
		responde somente P(D|Hi), em que H é a hi

		Esta função não precisa retornar nada, mas as partículas precisa ter o seu w recalculado. 

		Você vai precisar calcular para o robo

	"""

	leitura_robo = inspercles.nb_lidar(robot, angles)
	total = 0.0

	for p in particulas:
		soma_p = 0.0

		leitura_p = inspercles.nb_lidar(p, angles).items()
		for a, b in leitura_p:
			x = norm.pdf(b, leitura_robo[a], 8)
			soma_p += x
		total += soma_p

		alpha = 1/total
		part_w = soma_p
		part_w *= alpha
		

	# Voce vai precisar calcular a leitura para cada particula usando inspercles.nb_lidar e depois atualizar as probabilidades




def reamostrar(particulas, n_particulas = num_particulas):
    """
        Reamostra as partículas devolvendo novas particulas sorteadas
        de acordo com a probabilidade e deslocadas de acordo com uma variação normal    
        
        O notebook como_sortear tem dicas que podem ser úteis
        
        Depois de reamostradas todas as partículas precisam novamente ser deixadas com probabilidade igual
        
        Use 1/n ou 1, não importa desde que seja a mesma
    """

    pesos_p = [p.w for p in particulas]
    novas_p = draw_random_sample(particulas, pesos_p, num_particulas)

    for p in novas_p:
    	p.x = norm.rvs(0, 3)
    	p.y = norm.rvs(0, 3)
    	p.theta = norm.rvs(0, math.radians(2))
    	p.w = 1

    return novas_p


    







