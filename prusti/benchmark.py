#/usr/bin/python3

import csv
import glob
import os
import subprocess
import time
import re

ROOT = os.path.dirname(os.path.abspath(__file__))
TOML_FILE = os.path.join(ROOT, 'Prusti.toml')
LOG_FILE = os.path.join(ROOT, 'bench.csv')
MAKE_FLAGS = ["JAVA_HOME=/usr/lib/jvm/jdk-11.0.1/"]


def create_configuration_file():
    with open(TOML_FILE, 'w') as fp:
        fp.write(
'''
DUMP_DEBUG_INFO = false
DUMP_BORROWCK_INFO = false
CHECK_BINARY_OPERATIONS = false
''')


def build_project():
    subprocess.run(
        [
            "make",
            "build_release",
            ] + MAKE_FLAGS,
        cwd=ROOT,
        check=True,
    )


def get_benchmarks():
    rosetta_path = os.path.join(ROOT, 'tests/verify/pass/rosetta/')
    rosetta_glob = os.path.join(rosetta_path, '*.rs')
    rosetta_todo_glob = os.path.join(rosetta_path, 'todo', '*.rs')
    rosetta_stress_path = os.path.join(ROOT, 'prusti/tests/verify/todo/stress/rosetta/')
    rosetta_stress_glob = os.path.join(rosetta_stress_path, '*.rs')
    return (list(glob.glob(rosetta_glob)) +
            list(glob.glob(rosetta_todo_glob)) +
            list(glob.glob(rosetta_stress_glob)))


def run_benchmarks():
    benchmarks = get_benchmarks()
    with open(LOG_FILE, 'a') as fp:
        writer = csv.writer(fp)
        for benchmark in benchmarks:
            row = run_benchmark(benchmark)
            if row:
                writer.writerow(row)


def run_benchmark(file_path):
    if not 'Knigh' in file_path:
        return
    print(file_path)
    start_time = time.time()
    result = subprocess.run(
        [
            "make", "run_release",
            "LOG_LEVEL=prusti_viper=info",
            "RUN_FILE=" + file_path,
            ] + MAKE_FLAGS,
        cwd=ROOT,
        check=True,
        stderr=subprocess.PIPE,
    )
    end_time = time.time()
    duration = end_time - start_time
    match = re.search(
        b'^ INFO .+: prusti_viper::verifier: Verification complete \((.+) seconds\)$',
        result.stderr,
        re.MULTILINE)
    verification_time = float(match.group(1))
    return (file_path, start_time, end_time, duration, verification_time)

def main():
    create_configuration_file()
    build_project()
    run_benchmarks()


if __name__ == '__main__':
    main()