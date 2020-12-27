from timer import Timer
from os.path import exists, join
from os import makedirs


class Folder:
    DST = "run_"+str(Timer.start.strftime('%s'))
    DST_ALL = join(DST, "all")

    if not exists(DST_ALL):
        makedirs(DST_ALL)

    DST_ARC = join(DST, "archive")

    if not exists(DST_ARC):
        makedirs(DST_ARC)
