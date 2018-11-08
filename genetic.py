import random, sys
from functools import reduce


def has_repetition(l):
    s = set()
    for i in l:
        if i in s:
            return True
        s.add(i)
    return False


def check_pop_clean(pop):
    for l in pop:
        if has_repetition(l):
            print(l)
            print('WRONG')
            sys.exit()


def print_board(l):
    for q in l:
        print('#' * 49)
        print(('#' + (' ' * 5)) * 8 + '#')
        print(('#' + (' ' * 5)) * q, end='')
        print('#  Q  ', end='')
        print(('#' + (' ' * 5)) * (7 - q) + '#')       
        print(('#' + (' ' * 5)) * 8 + '#')
    print('#' * 49)


def to_bit_vector(arr):
    vec = []
    for q in arr:
        vec.append(1 if q & 0b100 else 0)
        vec.append(1 if q & 0b10 else 0)
        vec.append(1 if q & 1 else 0)
    return vec


def to_int_array(vec):
    arr = []
    for i in range(8):
        arr.append(vec[i*3] * 4 + vec[i*3+1] * 2 + vec[i*3+2])
    return arr


def generateRandoms(amount, elements, lim=8):
  childrenSet = list()
  
  while True:
    child = []
    randomSet = set()
    while True:
      randomNumber = random.randint(0,lim - 1)
      if not randomSet:
        randomSet.add(randomNumber)
        child.append(randomNumber)
      else:
        while(randomNumber in randomSet):
          randomNumber = random.randint(0,lim - 1)
        randomSet.add(randomNumber)
        child.append(randomNumber)

      if len(child) >= elements:
        break

    if not childrenSet:
      childrenSet.append(child)
    else:
      flag = False
      for n in childrenSet:
        if n == child:
          flag = True
          break
      if not flag:
        childrenSet.append(child)

    if len(childrenSet) >= amount:
      break
  
  return(childrenSet)


def checkCollision(coord):
    collision = 0
    for counter, value in enumerate(coord):
        row = counter
        column = value
        currentRow = row
        currentColumn = column

        while currentColumn>0 and currentRow<7:
            currentColumn-=1
            currentRow+=1
            if coord[currentRow]==currentColumn:
                collision+=1
        currentRow = row
        currentColumn = column

        while currentColumn<8 and currentRow<7:
            currentColumn+=1
            currentRow+=1
            if coord[currentRow]==currentColumn:
                collision+=1
    return collision


def rank_population(pop):
    # Sorts population according to fitness function.
    return sorted(pop, key=lambda l: checkCollision(l))


def mutate(pop, percentage=0.1):
    # Mutates the population according to mutation percentage.
    indices_to_mutate = generateRandoms(1, int(round(len(pop) * percentage)), len(pop))[0]
    values_to_mutate = generateRandoms(1, int(round(len(pop) * percentage)), 8)[0]
    for idx, val in zip(indices_to_mutate, values_to_mutate):
        other_value = random.randint(0, 7)
        while other_value == val:
            other_value = random.randint(0, 7)
        pop[idx][val], pop[idx][other_value] = pop[idx][other_value], pop[idx][val]
    return pop


def generateChildren(list1, list2, swapList):
    children = list()
    child = list()

    for swap in swapList:
        for x in swap:
            try:
                position1 = list1.index(x)    
                position2 = list2.index(x)
            except ValueError:
                print(list1)
                print(list2)
                sys.exit()
            child = list1.copy()
            child[position1], child[position2] = child[position2] , child[position1]
        children.append(child.copy())
    return children


def select_parents(population):
    # Selects the parents from the population.
    inverse_fitness_sum = reduce((lambda x, y: x + 28 - checkCollision(y)), population, 0)
    parent_indices = []
    for i, l in enumerate(population):
        inverse_fitness = 28 - checkCollision(l)
        probability = inverse_fitness / inverse_fitness_sum
        if random.random() < probability:
            # Select this one for the pair.
            parent_indices.append(i)
    # Remove one if the size is odd.
    if len(parent_indices) % 2 != 0:
        parent_indices = parent_indices[:-1]
    return parent_indices


def generate_children(population, parent_indices):
    # Randomly shuffle parents.
    random.shuffle(parent_indices)
    children = []
    for i in range(0, len(parent_indices), 2):
        children = children + (generateChildren(population[parent_indices[i]], population[parent_indices[i+1]], generateRandoms(3, 3)))
    return children


def solve():
    # Generate first population of 10 randomly.
    population = generateRandoms(10,8)
    print('Initial population:')
    print('\n'.join(list(map(str,population))))
    print('\n'*3)
    generations_until_purge = 3
    generation_number = 1
    check_pop_clean(population)
    while True:
        print('Generation #', generation_number)
        
        # Select the appropriate parents
        parent_indices = select_parents(population)
        # Generate the children
        population = population + generate_children(population, parent_indices)
        check_pop_clean(population)
        # Mutate the population
        population = mutate(population)
        check_pop_clean(population)
        # Evaluate the population
        population = rank_population(population)
        if not checkCollision(population[0]):
            # Exit condition met.
            print('Found solution in {} generations:'.format(generation_number))
            print_board(population[0])
            break
        generations_until_purge -= 1
        if not generations_until_purge:
            # Remove all but the best 10.
            population = population[:10]
            generations_until_purge = 3
        generation_number += 1

solve()
