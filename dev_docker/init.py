import os
import os.path
from multiprocessing import Process
import subprocess


def go_up(path, n):
    return os.path.abspath(os.path.join(*([path] + ['..']*n)))

def get_the_file_path():
    return os.path.abspath(os.path.dirname(__file__))

DEV_DOCKER_PATH = get_the_file_path()

BASE_PATH = go_up(DEV_DOCKER_PATH, 1)


def main():
    os.chdir(DEV_DOCKER_PATH)

    os.system('sudo docker build -t db - < db')

    os.system('sudo docker build -t db_client - < db_client')



    os.chdir(BASE_PATH)

    os.system('cp %s/web ./Dockerfile' % DEV_DOCKER_PATH)
    os.system('sudo docker build -t web .')


if __name__ == '__main__':
    main()


