from typing import List, Optional
import random
from math import prod

from dataclasses import dataclass

@dataclass
class Environment:
    target: int
    nums: List[int]
    dims: int

@dataclass
class Citizen:
    gene: List[int]
    fitness: int


def get_nums() -> List[int]:
    return [int(l) for l in open("input.txt", "r").read().splitlines()]

def gene_fitness(env: Environment, citizen: List[int]) -> int:
    s = sum([env.nums[i] for i in citizen])
    return (env.target-s)**2

def clamp(env: Environment, i: int) -> int:
    return max(0, min(len(env.nums)-1, i))

def citizen(env: Environment) -> Citizen:
    gene = [random.choice(range(len(env.nums))) for _ in range(env.dims)]
    return Citizen(gene=gene, fitness=gene_fitness(env, gene))

def spontaneous_combustion(env: Environment, target_citizens: Optional[int]=None) -> List[Citizen]:
    l = len(env.nums)
    if target_citizens is None:
        target_citizens = (l**2)//1000
    return [citizen(env) for _ in range(target_citizens)]

def mutate_gene(env: Environment, citizen: Citizen) -> Citizen:
    mutation = [random.choice([-1, 0, 1]) for _ in range(env.dims)]
    new_gene = [clamp(env, i+j) for i,j in zip(citizen.gene, mutation)]
    return Citizen(new_gene, gene_fitness(env, new_gene))

def mutate(env: Environment, fit: List[Citizen]) -> List[Citizen]:
    return [mutate_gene(env, c) for c in fit]

def update_fitness(env: Environment, c: Citizen) -> Citizen:
    return Citizen(c.gene, fitness=gene_fitness(env, c.gene))

def by_fitness(env: Environment, population: List[Citizen]) -> List[Citizen]:
    return sorted([update_fitness(env, c) for c in population], key=lambda c: c.fitness)

def proliferate(env: Environment, population: List[Citizen]) -> List[Citizen]:
    l = len(population)
    one_quarter = l // 4
    fit = population[:one_quarter]
    population = fit + mutate(env, fit) + spontaneous_combustion(env, one_quarter*2)
    return by_fitness(env, population)

@dataclass
class Solution:
    product: int
    iterations: int

def solve(env: Environment) -> Solution:
    iterations = 0
    population = spontaneous_combustion(env)
    while population[0].fitness > 0:
        population = by_fitness(env, proliferate(env, population))
        iterations += 1
    return Solution(prod([env.nums[i] for i in population[0].gene]), iterations)

if __name__ == "__main__":
    print(solve(Environment(2020, get_nums(), 2)))
    print(solve(Environment(2020, get_nums(), 3)))
