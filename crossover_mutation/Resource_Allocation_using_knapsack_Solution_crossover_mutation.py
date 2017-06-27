# 
############################################################################
# Resource Allocation problem solution using Gentic Algorithm              #
############################################################################
#
# Author: Srikanth Tiyyagura  <srikanth.tiyyagura@ucdconncect.ie>
#
############################################################################
# Built using GIT Python Code on Genetic Algorithms                        #
############################################################################
#
# Below code was coded by reusing code available under Apache License 2.0   
# at the GIT Source Link: https://github.com/handcraftsman/
# GeneticAlgorithmsWithPython/blob/master/ch09/knapsackTests.py
#
# Code Author: Clinton Sheppard <fluentcoder@gmail.com>
# Copyright (c) 2016 Clinton Sheppard
############################################################################

import datetime
import random
from random import randrange
import unittest
import math
import genetic


def get_fitness(genes, geneGroupCount, maxGeneGroupSize):
    
    groupFitness ={}
    
    #Split the genes as per the groups
    for eachGroup in range(geneGroupCount):
        startIndex = eachGroup *  maxGeneGroupSize
        endIndex = startIndex + maxGeneGroupSize
        if(endIndex <= len(genes)):
            geneSet = genes[startIndex:endIndex] 
        else:
            geneSet = genes[startIndex:] 
        
        peopleRoleDt ={}
        workRoleDt ={}
        
        #Check for any duplicates using dictionary
        for eachGene in geneSet:
            if eachGene.WorkRole in workRoleDt:
                workRoleDt[eachGene.WorkRole] += 1
            else:
                workRoleDt[eachGene.WorkRole] = 1

            if eachGene.PeopleRole in peopleRoleDt:
                peopleRoleDt[eachGene.PeopleRole] += 1
            else:
                peopleRoleDt[eachGene.PeopleRole] = 1

        
        fitnessVal=0
        
        # Multiple by 3 for each value in dictionary
        for key,value in peopleRoleDt.items():
            fitnessVal += value ** 3
        
        
        for key,value in workRoleDt.items():
            fitnessVal += value ** 3
        
        groupFitness[eachGroup] =fitnessVal
        
    return Fitness(groupFitness, geneGroupCount)


def display(candidate, startTime):
    timeDiff = datetime.datetime.now() - startTime
    print("{}; Age - {}; Time - {}".format(
        candidate.Fitness,
        candidate.Age,
        timeDiff))

    
def mutate(genes,  maxGeneGroupSize):
    count = random.randint(1, maxGeneGroupSize)
    
    while count > 0:
        count -= 1
        index = random.randint(0,len(genes)-1)
        gene = genes[index]
        genes.remove(gene)
        genes.insert(randrange(len(genes)+1),gene)
    return genes

class ResourceAllocationTests(unittest.TestCase):

    def test_group(self, maxGeneCount = 500, maxGeneGroupSize=7):
        
        #population creation
        geneset =[]
  
        for eachGene in range(maxGeneCount):
            workRole = random.randint(1,6)
            peopleRole = random.randint(1,6)
            gene=Resource(eachGene+1,workRole,peopleRole)
            geneset.append(gene)
            
            
        #Groups 
        geneGroupCount = math.ceil(maxGeneCount/maxGeneGroupSize)
                   
        startTime = datetime.datetime.now()

        def fnDisplay(candidate):
            display(candidate, startTime)

        def fnGetFitness(genes, geneGroupCount, maxGeneGroupSize):
            return get_fitness(genes, geneGroupCount, maxGeneGroupSize)

        def fnMutate(genes, maxGeneGroupSize):
            return mutate(genes, maxGeneGroupSize)

        opFitness ={}
        for x in range(geneGroupCount):
            opFitness[x] = x+2*maxGeneGroupSize

        
        optimalFitness = Fitness(opFitness, geneGroupCount )
        
        print("Optimal:", optimalFitness)
        
        best = genetic.get_best(fnGetFitness, maxGeneCount, maxGeneGroupSize, optimalFitness, geneset,
                                fnDisplay, custom_mutate=fnMutate, maxAge=100000)
        
#        print("Genes: ",best.Genes, "Group Count:", geneGroupCount)
        
        self.assertTrue(not optimalFitness < best.Fitness)

    def test_benchmark(self):
        genetic.Benchmark.run(lambda: self.test_group())


class Fitness:
    def __init__(self, groupFitness, groupCount):
        self.GroupFitness = groupFitness
        self.GroupCount = groupCount
        self.AvgGroupFitness = sum(self.GroupFitness.values()) / self.GroupCount 
        

    def __gt__(self, other):
        if ( self.AvgGroupFitness != other.AvgGroupFitness):    
            return self.AvgGroupFitness > other.AvgGroupFitness
        return self.AvgGroupFitness == other.AvgGroupFitness
    
    def __lt__(self, other):
        if ( self.AvgGroupFitness != other.AvgGroupFitness):
            return self.AvgGroupFitness < other.AvgGroupFitness
        return self.AvgGroupFitness == other.AvgGroupFitness
    

    def __str__(self):
        return " AvgGroupFitness - {}".format(
            self.AvgGroupFitness)

class Resource:
    def __init__(self, name, workRole, peopleRole):
        self.Name = name
        self.WorkRole = workRole
        self.PeopleRole = peopleRole
    
    def __str__(self):
        return "Name:  %s workRole: %s peopleRole: %s \n " % (self.Name, self.WorkRole \
                                                          ,self.PeopleRole)
        
    def __repr__(self):
        return str(self)
    
if __name__ == '__main__':
    unittest.main()
