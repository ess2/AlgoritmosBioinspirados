import numpy
import random

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

    return 28 - clashes

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
    tx = x[0:(c+1)]
    ty = y[0:(c+1)]
    d = c + 1

    if d==n:
        return (x, y)
    else:
        for k in range(d,n):
            tempX = x[k]

            if tempX not in ty:
                ty += [tempX]
            else:
                count = k
                for i in range(k,n):
                    tempX = x[i]

                    if tempX not in ty:
                        ty+=[tempX]
                        count += 1
                        break
                    count += 1

                if(count == n):
                    for j in range(c+1):
                        tempX = x[j]
                        if tempX not in ty:
                            ty += [tempX]
                            break

            #Trocando o array X
            tempY = y[k]

            if tempY not in tx:
                tx += [tempY]
            else:
                count = k
                for i in range(k,n):
                    tempY = y[i]

                    if tempY not in tx:
                        tx+=[tempY]
                        count += 1
                        break
                    count += 1

                if(count == n):
                    for j in range(c+1):
                        tempY = y[j]
                        if tempY not in tx:
                            tx += [tempY]
                            break
    return (tx, ty)

def excludeBad(finalList, elements):
    for i in range(len(elements)):
        finalList[len(finalList)-(i+1)] = elements[i]

    return finalList

def takeSecond(elem):
    return elem[1]

popl = list()
listPositions = list()
qtFitness = 0

#Gera a população
for i in range(100):
    a = random.sample(range(1,9), 8)
    if a not in listPositions:
        fitn = fitness(a)
        qtFitness += 1
        tuple = (a, fitn)
        listPositions.append(tuple)
        binaryArray = ['', '', '', '', '', '', '', '']
        b = numpy.array(tuple[0])
        for u in range(8):
            binaryArray[u] = '{0:03b}'.format(b[u])
        print "Genótipo " + str(i) + ":" + str(binaryArray)
    else:
        i = i - 1

print len(listPositions)
listPositions.sort(key=takeSecond,reverse=True)

firstElementList = listPositions[0]

while ((listPositions[0])[1] < 28 and qtFitness < 10000):
    probRecombNumber = random.randint(1,10)
    probMutNumber = random.randint(1,10)

    if (probRecombNumber > 0) and (probRecombNumber < 10):
        firstEl = listPositions[0]
        secondEl = listPositions[1]
        childs = reproduce(firstEl[0], secondEl[0])
        fitness1 = fitness(childs[0])
        fitness2 = fitness(childs[1])
        qtFitness += 2
        tuple = (childs[0], fitness1)
        tuple2 = (childs[1], fitness2)
        listPositions = excludeBad(listPositions, [tuple, tuple2])
        listPositions.sort(key=takeSecond, reverse=True)

    if(probMutNumber > 0) and (probMutNumber < 5):
        firstEl = listPositions[0]
        child = mutate(firstEl[0])
        fitn = fitness(child)
        qtFitness += 1
        tuple = (child, fitn)
        listPositions = excludeBad(listPositions, [tuple])
        listPositions.sort(key=takeSecond, reverse=True)

    firstElementList = listPositions[0]


binaryArray = ['','','','','','','','']
print "Melhor Solução:"
element = listPositions[0]

a = numpy.array(element[0])

for i in range(8):
    binaryArray[i] = '{0:03b}'.format(a[i])

print binaryArray

print "Fitness:"
print (listPositions[0])[1]

print "Número de avaliações de fitness:"
print qtFitness
