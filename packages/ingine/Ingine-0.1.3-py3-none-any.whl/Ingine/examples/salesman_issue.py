import random as rnd
from Ingine import ga


rnd.seed(151685)

points = []

for i in range(22):
    points.append(tuple([rnd.randint(0, 100), rnd.randint(0, 100)]))


def create_individual(points):
    res = points
    rnd.shuffle(res)
    return res


def crossover(creature1, creature2):
    creatures = list(zip(creature1, creature2))
    creature = []
    for _ in creatures:
        choise = rnd.randint(0, 1)
        another = (choise + 1) % 2
        if _[choise] not in creature:
            creature.append(_[choise])
        else:
            creature.append(_[another])
    return creature, list(reversed(creature))


def mutate(creature):
    a = rnd.randint(0, len(creature)-1)
    b = rnd.randint(0, len(creature)-1)
    creature[a], creature[b] = creature[b], creature[a]


def selection(population):
    return rnd.choice(population)


def fitness(creature, data):
    def s(p1, p2):
        return sum([(a - b)**2 for a, b in zip(p1, p2)])

    res = sum([s(prev, current) for prev, current in zip(creature[:-1], creature[1:])])
    res += s(creature[0], creature[-1])

    return res


optimiser = ga.get_optimizer(points,
                             fitness,
                             20,
                             2000,
                             maximise_fitness = False,
                             create_individual = create_individual,
                             mutate = mutate,
                             crossover = crossover)

res = optimiser()[1]

from PIL import Image, ImageDraw

image = Image.new("L", (1000, 1000), (255, ))
draw = ImageDraw.Draw(image)

for x, y in res:
    draw.rectangle((x * 10, y * 10, (x + 1) * 10, (y + 1) * 10), fill = (0,))

coords = []

for prev, cur in zip(res[:-1], res[1:]):
    coords.append(prev[0]*10)
    coords.append(prev[1]*10)
    coords.append(cur[0]*10)
    coords.append(cur[1]*10)

coords.append(res[0][0]*10)
coords.append(res[0][1]*10)
coords.append(res[-1][0]*10)
coords.append(res[-1][1]*10)

draw.line(coords, (0,))

image.show()