import json

from core.archive_impl import SmartArchive
from self_driving.beamng_config import BeamNGConfig
from self_driving.beamng_problem import BeamNGProblem
from core.config import Config
from core.folder_storage import SeedStorage
import os, glob, json
from random import shuffle, choice
from shutil import copy
from core.seed_pool_impl import SeedPoolFolder, SeedPoolRandom
from self_driving.edit_distance_polyline import iterative_levenshtein

config = BeamNGConfig()
problem = BeamNGProblem(config, SmartArchive(config.ARCHIVE_THRESHOLD))

def get_spine(member):
    spine = json.loads(open(member).read())['sample_nodes']
    return spine

def get_min_distance_from_set(ind, solution):
    distances = list()
    ind_spine = get_spine(ind)
    for road in solution:
        road_spine = get_spine(road)
        distances.append(iterative_levenshtein(ind_spine, road_spine))
    distances.sort()
    return distances[0]


def initial_pool_generator():
    good_members_found = 0
    attempts = 0
    storage = SeedStorage('prova_roads')

    while good_members_found < 40:
        path = storage.get_path_by_index(good_members_found + 1)
        if path.exists():
            print('member already exists', path)
            good_members_found += 1
            continue
        attempts += 1
        print(f'attempts {attempts} good {good_members_found} looking for {path}')
        member = problem.generate_random_member()
        member.evaluate()
        if member.distance_to_boundary <= 0:
            continue
        member = problem.member_class().from_dict(member.to_dict())
        member.config = config
        member.problem = problem
        member.clear_evaluation()

        member.distance_to_boundary = None
        good_members_found += 1
        path.write_text(json.dumps(member.to_dict()))

    return path

def initial_population_generator(path):

    all_roads = [filename for filename in glob.glob(path)]
    #all_roads += [filename for filename in glob.glob(path2)]

    shuffle(all_roads)

    roads = all_roads[:40]

    starting_point = choice(roads)

    original_set = list()
    original_set.append(starting_point)

    popsize = 12

    i = 0
    while i < popsize-1:
        max_dist = 0
        for ind in roads:
            dist = get_min_distance_from_set(ind, original_set)
            if dist > max_dist:
                max_dist = dist
                best_ind = ind
        original_set.append(best_ind)
        i += 1

    base = config.seed_folder
    seed_pool = SeedPoolFolder(problem, config.seed_folder)
    if not os.path.exists(seed_pool.path):
        os.makedirs(base)
    for index, road in enumerate(original_set):
        dst = os.path.join(base,'seed'+str(index)+'.json')
        copy(road,dst)

if __name__ == '__main__':
    path = initial_pool_generator()
    initial_population_generator(path)