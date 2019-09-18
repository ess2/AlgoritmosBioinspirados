import numpy
import random
import time

max_fitness = 28
qt_exec = 20
qt_population = 200

def main():
    for f in range(qt_exec):
        inicio = time.time()
        population = list()
        qtFitness = 0

        #Gera a população
        for i in range(qt_population):
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
                #print "Genótipo " + str(i) + ":" + str(binaryArray)
            else:
                i = i - 1

        population.sort(key=takeSecond,reverse=True)
    #(population[0])[1] < max_fitness
        while (qtFitness < 10000):
            probRecombNumber = random.randint(1,10)
            probMutNumber = random.randint(1,10)

            if (probRecombNumber > 0) and (probRecombNumber < 10):
                firstEl = population[0]
                secondEl = population[1]
                childs = reproduce(firstEl[0], secondEl[0])
                fitness1 = fitness(childs[0])
                fitness2 = fitness(childs[1])
                qtFitness += 2
                tuple = (childs[0], fitness1)
                tuple2 = (childs[1], fitness2)
                population = excludeBad(population, [tuple, tuple2])
                population.sort(key=takeSecond, reverse=True)

            if(probMutNumber > 0) and (probMutNumber < 5):
                firstEl = population[0]
                child = mutate(firstEl[0])
                fitn = fitness(child)
                qtFitness += 1
                tuple = (child, fitn)
                population = excludeBad(population, [tuple])
                population.sort(key=takeSecond, reverse=True)

        binaryArray = ['','','','','','','','']
        #print "Melhor Solução:"
        #element = population[0]

        #a = numpy.array(element[0])

        #for i in range(8):
        #    binaryArray[i] = '{0:03b}'.format(a[i])

        #print binaryArray

        #print "Fitness:"
        #print (population[0])[1]

        #print "Número de avaliações de fitness:" + str(qtFitness)


        qtMaxFit = 0
        for i in range(len(population)):
            if (population[i])[1] == max_fitness:
                qtMaxFit += 1
            else:
                break

        print "Quantidade de indíviduos que atingiram o fitness máximo:" + str(qtMaxFit)
        fim = time.time()

        print "Tempo de Execução " + str(f) + ": " + str((fim - inicio))
        print "################################################################"


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
    #print max_fitness - clashes
    return max_fitness - clashes

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

if __name__ == '__main__':
    main()