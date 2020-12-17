import json

from core.archive_impl import SmartArchive
from self_driving.beamng_config import BeamNGConfig
from self_driving.beamng_problem import BeamNGProblem
from core.config import Config
from core.folder_storage import SeedStorage


config = BeamNGConfig()
problem = BeamNGProblem(config, SmartArchive(config.ARCHIVE_THRESHOLD))

if __name__ == '__main__':
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
