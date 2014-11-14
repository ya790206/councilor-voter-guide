import os
import os.path
from multiprocessing import Process
import subprocess
import time


def go_up(path, n):
    return os.path.abspath(os.path.join(*([path] + ['..']*n)))

def get_the_file_path():
    return os.path.abspath(os.path.dirname(__file__))

DEV_DOCKER_PATH = get_the_file_path()

BASE_PATH = go_up(DEV_DOCKER_PATH, 1)


def main():

    os.chdir(DEV_DOCKER_PATH)
    os.system("sudo docker run --rm --link db:db -t db_client /bin/bash -c 'createdb -h db -U docker voter_guider'")

    os.system("sudo docker run --link db:db -v `pwd`/../voter_guide/:/data -t db_client /bin/bash -c 'pg_restore --verbose --clean --no-acl --no-owner -h db -U docker -d voter_guider /data/local_db.dump'")


if __name__ == '__main__':
    main()


