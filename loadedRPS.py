from randombot import randombotfunc
from greedy import greedyfunc
from antigreedy import antigreedyfunc
from themessenger import themessengerfunc
from rockstar import rockstarfunc
from assassin import assassinfunc
from copycat import copycatfunc
from nothungry import nothungryfunc
from useopponents import useopponentsfunc
from goodwinning import goodwinningfunc
from react import reactfunc
from artsychild import artsychildfunc
from antirepeater import antirepeaterfunc
from yggdrasil import yggdrasilfunc
from weigher import weigherfunc
from statistician2 import *
from cycler import cyclerfunc
from swap import *
from ensemble import *
from bobw import bobwfunc
from fitter import fitterfunc
from blodsocer import blodsocerfunc 
from weightedrandom import weightedrandomfunc
from antiantigreedy import antiantigreedyfunc
from somewhathungry import somewhathungryfunc
from nash import nashfunc
from nashbot import nashbotfunc

import random
import numpy
import time
import sys

R = 0
P = 1
S = 2

rounds = 1000

functions = [randombotfunc, greedyfunc, antigreedyfunc, themessengerfunc, rockstarfunc, assassinfunc, copycatfunc, nothungryfunc, useopponentsfunc, goodwinningfunc, reactfunc, artsychildfunc, antirepeaterfunc, yggdrasilfunc, weigherfunc, statistician2func, cyclerfunc, swapfunc, ensemblefunc, bobwfunc, fitterfunc, blodsocerfunc, weightedrandomfunc, antiantigreedyfunc, somewhathungryfunc, nashfunc, nashbotfunc] 

players = len(functions) 

results = numpy.zeros(shape=(players,players,2))

def play(id1, id2, f1, f2):
	points1, points2 = 0, 0
	loaded1, loaded2 = [1.0, 1.0, 1.0], [1.0, 1.0, 1.0]
	history1, history2 = "", ""

	for turn in range(100):
		p1 = f1(points1, points2, loaded1, loaded2, history1, history2)
		p2 = f2(points2, points1, loaded2, loaded1, history2, history1)

		history1 += p1
		history2 += p2

		if p1 == "R":
			if p2 == "R":
				loaded1[R] += 0.5
				loaded2[R] += 0.5
			elif p2 == "P":
				loaded1[R] += 1
				points2 += loaded2[P]
			elif p2 == "S":
				loaded2[S] += 1
				points1 += loaded1[R]
		elif p1 == "P":
			if p2 == "R":
				loaded2[R] += 1
				points1 += loaded1[P]
			elif p2 == "P":
				loaded1[P] += 0.5
				loaded2[P] += 0.5
			elif p2 == "S":
				loaded1[P] += 1
				points2 += loaded2[S]
		elif p1 == "S":
			if p2 == "R":
				loaded1[S] += 1
				points2 += loaded2[R]
			elif p2 == "P":
				loaded2[P] += 1
				points1 += loaded1[S]
			elif p2 == "S":
				loaded1[S] += 0.5
				loaded2[S] += 0.5

	if points1 > points2:
		results[id1][id2][0] += 1
	elif points1 < points2:
		results[id2][id1][0] += 1
	else:
		results[id1][id2][1] += 1
		results[id2][id1][1] += 1

invrounds = 2 / (players * (players-1))
played = 0

elapsed = [0] * players



for i in range(players):
	f1 = functions[i]
	for j in range(i):
		f2 = functions[j]
		start_time = time.time()
		for k in range(rounds):
			play(i, j, f1, f2)

		end_time = time.time()
		elapsed[i] += (end_time - start_time)
		elapsed[j] += (end_time - start_time)
		
		played += 1
		sys.stdout.write("\r")
		p = played * invrounds
		sys.stdout.write("[%-20s] %d%%" % ("=" * int(p * 20), int(p * 100))) 		
sys.stdout.write("\n")


f = open("results_grid", "w")
won = [0] * players
draw = [0] * players
for i in range(players):
	f.write(str(i))
	for j in range(players):
		r = results[i][j]
		f.write(";" + str(int(r[0])) + "," + str(int(r[1])))
		won[i] += r[0]
		draw[i] += r[1]
	f.write("\n")

f.close()
f = open("results_standing", "w")

for i in range(players):
	f.write(str(i) + "," + str(int(won[i])) + "," + str(int(draw[i])) + "," + str(elapsed[i] / (players-1)) + "\n")

f.close()


