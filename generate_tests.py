from subprocess import Popen, PIPE
from random import random, seed, shuffle
from tqdm import tqdm
from pprint import pprint
import json
import time

SMALL_TEST_COUNT = 100
MEDIUM_TEST_COUNT = 50
LARGE_TEST_COUNT = 10
SEED = 1234
TEST_FILE = 'tests.json'

seed(SEED)

class Timer():
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.t0 = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print(f'{self.name}: {time.time() - self.t0:.2f}')

def generate_random_input(max_instances=20, max_elements=10**6, min_value=1, max_value=10**6):
    '''returns a string that is valid input'''
    instances = int(random() * (max_instances)) + 1
    test = f'{instances}'

    for _ in range(instances):
        size = int(random() * (max_elements)) + 1

        test += f'\n{size}'

        p = list(range(min_value, max_value+1))
        q = list(range(min_value, max_value+1))
        shuffle(p)
        shuffle(q)
        test += '\n' + '\n'.join(map(str, q[:size]))
        test += '\n' + '\n'.join(map(str, p[:size]))

    return test + '\n'

def shell(cmd, stdin=None):
    p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    out, err = p.communicate(input=stdin.encode() if stdin else None)
    return out.decode('utf8'), err.decode('utf8')

get_python = lambda testCase: shell('python3 points.py', stdin=testCase)
get_cpp = lambda testCase: shell('./Points', stdin=testCase)

print('Building:')
buildOutput, buildError = shell('make build')
if buildOutput:
    print(buildOutput)
if buildError:
    print('Error running `make build`:\n')
    print(buildError)
    exit()

tests = dict()

# manual tests
tests['given-test-0'] = {'input':'2\n4\n1\n10\n8\n6\n6\n2\n5\n1\n5\n9\n21\n1\n5\n18\n2\n4\n6\n10\n1\n', 'output':"4\n7\n"}

tests['edge-test-0'] = {'input':"1\n1\n1\n1\n", 'output':"0\n"}
tests['edge-test-1'] = {'input':"1\n3\n1\n2\n3\n3\n2\n1\n", 'output':"3\n"}
tests['edge-test-2'] = {'input':"1\n3\n1\n2\n3\n1\n2\n3\n", 'output':"0\n"}
tests['edge-test-3'] = {'input':"1\n3\n3\n2\n1\n1\n2\n3\n", 'output':"3\n"}

# random tests

for i in tqdm(range(SMALL_TEST_COUNT)):
    test = generate_random_input(max_instances=3, max_elements=10, max_value=10)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'small-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(MEDIUM_TEST_COUNT)):
    test = generate_random_input(max_instances=10, max_elements=300, max_value=300)
    python, p_err = get_python(test)
    cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        print(f'Input\n{test}')
        exit()
    tests[f'medium-test-{i}'] = {'input':test, 'output':python}

for i in tqdm(range(LARGE_TEST_COUNT)):
    test = generate_random_input(max_instances=5, max_elements=10**4)
    with Timer('python'):
        python, p_err = get_python(test)
    with Timer('c'):
        cpp, c_err1 = get_cpp(test)
    # print(python1)
    if python != cpp or len(python) < 1:
        print(f'Python\n{python}')
        print()
        print(f'Python error\n{p_err}')
        print()
        print(f'C++\n{cpp}')
        print()
        print(f'C++ error\n{c_err1}')
        print()
        # print(f'Input\n{test}')
        exit()
    tests[f'large-test-{i}'] = {'input':test, 'output':python}

# pprint(tests)
with open(TEST_FILE, 'w+') as f:
    json.dump(tests, f, indent=4)
