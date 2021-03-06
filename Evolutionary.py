# ################################     Evolutionary     ################################
import numpy as np
import random
import copy
# from memory_profiler import profile
import time
import sys
import os


number_of_queens = int(input("Please enter the number of queens: "))
start_time = time.time()
new_population = {}
next_population = {}
chromosome_tab = {}


def finish(alfa, beta):
    print("\n\n\n================================================================")
    print("A correct placement of %s queens with no threats have been found!" % number_of_queens)
    print(alfa, "   --->   ", beta)

    # define a nxn 0 matrix in order to map the final matrix - the final answer
    final = np.zeros((number_of_queens, number_of_queens), dtype=np.int64)

    # map the chromosome to the (final) matrix
    for fin in range(len(beta)):
        final[fin][beta[fin]] = 1
    print(final)

    # calculate the overall time
    total_time = time.time() - start_time
    print("------------------ %s seconds ------------------" % total_time)
    print("================================================================")

    if os.path.exists("Evolutionary_time.txt"):
        os.remove("Evolutionary_time.txt")

    f = open("Evolutionary_time.txt", "w+")
    f.write(str(round(total_time, 6)))
    f.close()

    # exit
    sys.exit(0)


#   ########################################    Threat Detection    ########################################
def threat(given):

    # assign an integer (count) to keep track of threats
    count = 0

    nn = len(given)

    # define a nxn 0 matrix in order to map the chromosome
    sample = np.zeros((nn, nn), dtype=np.int64)

    # map the chromosome to the (sample) matrix
    for v in range(nn):
        sample[v][given[v]] = 1

    # calculate number of threats
    # if queen1 is threatened by queen2, queen2 is also threatened by queen1    =>  number_of_threats = 2
    for i in range(nn):
        for j in range(nn):

            # find queens' places
            if sample[i][j] == 1:

                # enumerate cells around the queen and check if any of them contains a queen
                for a in range(0, nn-1):

                    # check north-west side of queen's cell
                    if i-a >= 0 and j-a >= 0 and sample[i-a][j-a] == 1 and j-a != j and i-a != i:
                        count += 1
                    # check south-east side of queen's cell
                    if i+a < nn and j+a < nn and sample[i+a][j+a] == 1 and j+a != j and i+a != i:
                        count += 1
                    # check south-east side of queen's cell
                    if i+a < nn and j-a >= 0 and sample[i+a][j-a] == 1 and j-a != j and i-a != i:
                        count += 1
                    # check north-east side of queen's cell
                    if i-a >= 0 and j+a < nn and sample[i-a][j+a] == 1 and j+a != j and i+a != i:
                        count += 1
    return count


# ########################################    initial population  ########################################
print()
for e in range(1, 11):
    globals()['Chromosome %s' % e] = random.sample(range(0, number_of_queens), number_of_queens)
    chromosome_tab['Chromosome %s' % e] = globals()['Chromosome %s' % e]
    print("Chromosome ", e, " : ", globals()['Chromosome %s' % e])
print()


while True:

    for q, w in chromosome_tab.items():

        if threat(w) == 0:
            finish(q, w)

#   ########################################      Tournament      ########################################
#   this function passes the candidate chromosomes to the threat_counter function
#   then returns the chromosome with the lowest number of threats(lowest cost)
    def tournament(candidates, y):
        x = copy.deepcopy(candidates)
        for d in x.keys():
            x[d] = threat(x[d])
        x_sorted = sorted(x.items(), key=lambda yy: yy[1])
        if y == 1:
            print("chromosomes with each threats:   ")
            for u in range(len(x_sorted)):
                print(x_sorted[u])
        return x_sorted[:y]


#   ########################################      tournament selection        ########################################
    # make a copy of chromosome tab so that we can delete the chromosome chosen in te first tournament
    # it makes sure that the winner of the first tournament won't participate in second one
    child_counter = 1
    generation_counter = 1
    while len(new_population) != 10:
        print("\n\n-------------------------     generation %s for offsprings     -------------------------"
              % generation_counter)
        local_tab = copy.deepcopy(chromosome_tab)
        generation_counter += 1

    # make a dictionary that's going to contain the participants of the first tournament
        tournament1 = {}
    # choose 3 of candidates randomly to participate them in the first tournament
        while len(tournament1) < 3:
            key = random.choice(list(local_tab.keys()))
            tournament1[key] = local_tab[key]
        print("tournament1 : ")
        return1 = tournament(tournament1, 1)
    # delete the winner from list of candidates
        del local_tab[return1[0][0]]

        tournament2 = {}
    # choose 3 of candidates randomly to participate them in the second tournament
        while len(tournament2) < 3:
            key = random.choice(list(local_tab.keys()))
            tournament2[key] = local_tab[key]
        print("\ntournament2 : ")
        return2 = tournament(tournament2, 1)

        print("\nReturn value of first tournament: ", return1)
        print("Return value of second tournament: ", return2, "\n")


#   ##################################################      PMX      ##################################################
        parent1 = globals()['Chromosome %s' % return1[0][0].split()[1]]
        parent2 = globals()['Chromosome %s' % return2[0][0].split()[1]]
        print("parent1 :", parent1)
        print("parent2 :", parent2, "\n")
        if random.uniform(0, 1) < 0.9:
            points_2 = sorted(random.sample(range(1, number_of_queens), 2))
            print("the selected points are :", points_2, "\n")
            child1 = [0 for i in range(number_of_queens)]
            child2 = [0 for i in range(number_of_queens)]
            child1[points_2[0]:points_2[1]] = parent1[points_2[0]:points_2[1]]
            child2[points_2[0]:points_2[1]] = parent2[points_2[0]:points_2[1]]
            m = 0
            for k in range(0, number_of_queens-points_2[1]):
                if parent2[points_2[1]+k] in child1[points_2[0]:points_2[1]]:
                    pass
                else:
                    child1[points_2[1]+m] = parent2[points_2[1]+k]
                    m += 1
                if points_2[1] + m == number_of_queens:
                    m = m - number_of_queens

            for k in range(0, points_2[1]):
                if parent2[k] in child1[points_2[0]: points_2[1]]:
                    pass
                elif points_2[1] + m != number_of_queens:
                    child1[points_2[1] + m] = parent2[k]
                    m += 1
                if points_2[1] + m == number_of_queens:
                    m = m - number_of_queens

            n = 0
            for k in range(0, number_of_queens - points_2[1]):
                if parent1[points_2[1] + k] in child2[points_2[0]: points_2[1]]:
                    pass
                else:
                    child2[points_2[1] + n] = parent1[points_2[1] + k]
                    n += 1
                if points_2[1] + n == number_of_queens:
                    n = n - number_of_queens

            for k in range(0, points_2[1]):
                if parent1[k] in child2[points_2[0]: points_2[1]]:
                    pass
                elif points_2[1] + n != number_of_queens:
                    child2[points_2[1] + n] = parent1[k]
                    n += 1
                if points_2[1] + n == number_of_queens:
                    n = n - number_of_queens
            print("child1 by pmx :", child1, " with", threat(child1), " threats")
            print("child2 by pmx :", child2, " with", threat(child2), " threats\n")


#   ##########################################    swap mutation    ############################################
        # child1's chance for mutation
            mutation_flag1 = 0
            if random.uniform(0, 1) < 1 - (1 - 0.1) ** number_of_queens:
                for i in range(0, number_of_queens):
                    if random.uniform(0, 1) < 0.1:
                        mutation_flag1 = 1
                        pair = list(range(0, number_of_queens))
                        pair.remove(i)
                        pair = random.choice(pair)
                        print(i, "swap with", pair)
                        child1[i], child1[pair] = child1[pair], child1[i]
                        print("child1 after mutation : ", child1, " with ", threat(child1), " threats")
                if mutation_flag1 == 0:
                    print("There is no mutation on child1")

            else:
                print("There is no mutation on child1")

        # child2's chance for mutation
            mutation_flag2 = 0
            if random.uniform(0, 1) < 1 - (1 - 0.1) ** number_of_queens:
                for i in range(0, number_of_queens):
                    if random.uniform(0, 1) < 0.1:
                        mutation_flag2 = 1
                        pair = list(range(0, number_of_queens))
                        pair.remove(i)
                        pair = random.choice(pair)
                        print(i, "swap with", pair)
                        child2[i], child2[pair] = child2[pair], child2[i]
                        print("child2 after mutation : ", child2, " with ", threat(child2), " threats")
                if mutation_flag2 == 0:
                    print("There is no mutation on child2")
            else:
                print("There is no mutation on child2")
            new_population['child %s' % child_counter] = child1
            child_counter += 1
            new_population['child %s' % child_counter] = child2
            child_counter += 1
        else:
            print("There is no crossover between parents")


#   ##################################################     New Population     ########################################
    print("\n\n-------------------------    New Population of Offsprings    -------------------------")
    for i in new_population:
        print(i, "  ", new_population[i])


#   ########################################     Next Population Generation     ########################################
    elitists = tournament(chromosome_tab, 2)
    next_population[elitists[0][0]] = chromosome_tab[elitists[0][0]]
    next_population[elitists[1][0]] = chromosome_tab[elitists[1][0]]
    del chromosome_tab[elitists[0][0]]
    del chromosome_tab[elitists[1][0]]


#   ########################################     Next Population     ##################################################
    temp = copy.deepcopy(chromosome_tab)
    for item in new_population.keys():
        temp[item] = new_population[item]

    reminded_chromosomes = tournament(temp, 8)
    reminded_chr_dict = {}

    for i in range(len(reminded_chromosomes)):
        reminded_chr_dict[reminded_chromosomes[i][0]] = reminded_chromosomes[i][1]

    for item in reminded_chr_dict:
        if item in new_population.keys():
            next_population[item] = new_population[item]
        else:
            next_population[item] = chromosome_tab[item]

    chromosome_tab = next_population
    tournament1.clear()
    tournament2.clear()
    reminded_chromosomes.clear()
    new_population.clear()

    print("\n\n-------------------------           Next Generation          -------------------------")
    for i in next_population:
        print(i, "  ", next_population[i])
