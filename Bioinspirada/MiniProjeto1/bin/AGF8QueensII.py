import numpy
import numpy.random as npr
import random
from math import trunc

max_fitness = 28

def main():
    population = list()
    qtFitness = 0

    #Gera a população
    for i in range(100):
        a = random.sample(range(1,9), 8)
        if a not in population:
            fitn = fitness(a)
            qtFitness += 1
            tuple = (a, fitn)
            population.append(tuple)
            binaryArray = ['', '', '', '', '', '', '', '']
            b = numpy.array(tuple[0])
            for u in range(8):
                binaryArray[u] = '{0:03b}'.format(b[u])
            print "Genótipo " + str(i) + ":" + str(binaryArray)

    population.sort(key=takeSecond,reverse=True)

    while ((population[0])[1] < max_fitness and qtFitness < 10000):
        probRecombNumber = random.randint(1,10)
        probMutNumber = random.randint(1,10)

        if (probRecombNumber > 0) and (probRecombNumber < 10):
            firstEl = roulletteSelection(population)
            secondEl = roulletteSelection(population)
            childs = reproduce(firstEl[0], secondEl[0])
            fitness1 = fitness(childs[0])
            fitness2 = fitness(childs[1])
            qtFitness += 2
            tuple = (childs[0], fitness1)
            tuple2 = (childs[1], fitness2)
            population = excludeBad(population, [tuple, tuple2])
            population.sort(key=takeSecond, reverse=True)

        if(probMutNumber > 0) and (probMutNumber < 5):
            firstEl = roulletteSelection(population)
            child = mutate(firstEl[0])
            fitn = fitness(child)
            qtFitness += 1
            tuple = (child, fitn)
            population = excludeBad(population, [tuple])
            population.sort(key=takeSecond, reverse=True)

    binaryArray = ['','','','','','','','']
    print "Melhor Solução:"
    element = population[0]

    a = numpy.array(element[0])

    for i in range(8):
        binaryArray[i] = '{0:03b}'.format(a[i])

    print binaryArray

    print "Fitness:"
    print (population[0])[1]

    print "Número de avaliações de fitness:"
    print qtFitness

def fitness(individual):
    clashes = 0;
    # calculate row and column clashes
    # just subtract the unique length of array from total length of array
    # [1,1,1,2,2,2] - [1,2] => 4 clashes
    row_col_clashes = abs(len(individual) - len(numpy.unique(individual)))
    clashes += row_col_clashes

    # calculate diagonal clashes
    for i in range(len(individual)):
        for j in range(len(individual)):
            if (i != j):
                dx = abs(i - j)
                dy = abs(individual[i] - individual[j])
                if (dx == dy):
                    clashes += 1

    fitns = max_fitness - clashes
    if(fitns < 0):
        fitns = 0

    return fitns

def mutate(x):
    n = len(x)
    c = 0
    a = 0
    while(c==a):
        c = random.randint(0, n - 1)
        m = random.randint(1, n)
        t = x[c]
        a = x.index(m)
    x[c] = m
    x[a] = t
    return x

def mutateByInversion(x):
    n = len(x)
    firstPosition = random.randint(0, n - 2)
    secondPosition = random.randint(firstPosition, n - 1)

    return x[0:firstPosition] + (x[firstPosition:secondPosition])[::-1] + x[secondPosition:len(x)]

def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    childX = x[0:(c+1)]
    childY = y[0:(c+1)]
    d = c + 1

    if d==n or d==(n-1):
        return (x, y)
    else:
        for k in range(d,n):
            #Generate new elements for Child Y
            count = k
            for i in range(k,n):
                tempX = x[i]

                if tempX not in childY:
                    childY+=[tempX]
                    count += 1
                    break
                count += 1

            if(count == n):
                for j in range(c+1):
                    tempX = x[j]
                    if tempX not in childY:
                        childY += [tempX]
                        break

            # Generate new elements for Child X
            count = k
            for i in range(k,n):
                tempY = y[i]

                if tempY not in childX:
                    childX+=[tempY]
                    count += 1
                    break
                count += 1

            if(count == n):
                for j in range(c+1):
                    tempY = y[j]
                    if tempY not in childX:
                        childX += [tempY]
                        break
    return (childX, childY)

def excludeBad(finalList, elements):
    for i in range(len(elements)):
        finalList[len(finalList)-(i+1)] = elements[i]

    return finalList

def takeSecond(elem):
    return elem[1]

def roulletteSelection(population):
    max = sum([c[1] for c in population])
    selection_probs = [float(c[1])/float(max) for c in population]
    return population[npr.choice(len(population), p=selection_probs)]

if __name__ == '__main__':
    main()