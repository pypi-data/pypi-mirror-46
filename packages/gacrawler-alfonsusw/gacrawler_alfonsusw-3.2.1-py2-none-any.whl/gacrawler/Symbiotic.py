from __future__ import division, unicode_literals
from . import function as fn
import random
import operator
from copy import deepcopy
from sklearn.metrics import jaccard_similarity_score

class Symbiotic:
    def __init__(self, _query):
        self.generation = 1

        # preprocess query
        self.query = _query.split()

        # individuals isinya tipe data Individu
        self.individuals = []

        # refine gen individu
        self.refined = False

    def calcFitness(self):
        for x in self.individuals:
            x.calcFitness(self.query)

    def generate(self):
        self.calcFitness()
        self.dimension = len(self.query)

        for i in range(len(self.individuals)):
            # Xbest = max(self.individuals, key=operator.attrgetter('fitness'))
            Xbest = self.findOptimum()
            Xi = self.individuals[i]

            while(True):
                j = random.randrange(len(self.individuals))
                Xj = self.individuals[j]
                if(Xj != Xi): break

            # lakukan mutualisme(Xi, Xj)
            # (Xi + Xj) / 2
            MV = [(Xi.gen[x] + Xj.gen[x]) / 2 for x in range(self.dimension)]
            BF1 = random.randint(1, 2)
            BF2 = random.randint(1, 2)

            XiNew = Individu()
            XjNew = Individu()
            XiNew.gen = [(Xi.gen[x] + random.random() * (Xbest.gen[x] - MV[x] * BF1)) for x in range(self.dimension)]
            XjNew.gen = [(Xj.gen[x] + random.random() * (Xbest.gen[x] - MV[x] * BF2)) for x in range(self.dimension)]

            XiNew.calcFitness(self.query)
            XjNew.calcFitness(self.query)

            if (XiNew.fitness > Xi.fitness):
                self.individuals[i] = XiNew
            if (XjNew.fitness > Xj.fitness):
                self.individuals[j] = XjNew

            # lakukan komensalisme(Xi, Xj)
            # i yang berubah
            while (True):
                j = random.randrange(len(self.individuals))
                Xj = self.individuals[j]
                if (Xj != Xi): break
            XiNew = Individu()
            XiNew.gen = [(Xi.gen[x] + random.uniform(-1, 1) * (Xbest.gen[x] - Xj.gen[x])) for x in range(self.dimension)]

            XiNew.calcFitness(self.query)

            if (XiNew.fitness > self.individuals[i].fitness):
                self.individuals[i] = XiNew

            # lakukan parasitisme(Xi, Xj)
            # j yang berubah
            # parasite vector = modifikasi Xi. Sama seperti mutasi pada genetic
            while (True):
                j = random.randrange(len(self.individuals))
                Xj = self.individuals[j]
                if (Xj != Xi): break

            PV = Individu()
            PV.gen = deepcopy(Xi.gen)
            
            PV.calcFitness(self.query)
            if (PV.fitness > Xj.fitness):
                self.individuals[j] = PV
        self.generation += 1

    def append(self, _text, _gen):
        self.individuals.append(Individu(_text, _gen))

    def set_query(self, _q):
        self.query = _q

    def set_keyword_document(self, _k):
        self.keyword_document = _k

    def findOptimum(self, targetFitness = 0.7):
        _ = sorted(self.individuals, key=operator.attrgetter('fitness'), reverse=True)
        for i in _:
            if i.fitness < targetFitness: return i
        return _[0]

    @property
    def query_best(self):
        best = self.best
        query = []
        for i, term in enumerate(self.keyword_document):
            if(round(best.gen[i]) == 1): query.append(term)
        return ' '.join(query)

    @property
    def best(self):
        # best = max(self.individuals, key=operator.attrgetter('fitness'))
        # return best
        return self.findOptimum()

class Individu:
    def __init__(self, _text=None, _gen=None):
        self.fitness = 0
        self.text = _text
        self.gen = _gen

    def calcFitness(self, _compare):
        # self.fitness = jaccard_similarity_score(_compare, self.gen)
        self.fitness = fn.get_jaccard_sim_binary([round(fn.sigmoid(x)) for x in _compare], [round(fn.sigmoid(x)) for x in self.gen])

    def __eq__(self, other):
        # make individu comparable
        return self.gen == other.gen

