import json
import os

from geneeanlpclient.g3.reader import fromDict

EXAMPLE = os.path.join(os.path.dirname(__file__), 'examples', 'example.json')
EXAMPLE_PHENO = os.path.join(os.path.dirname(__file__), 'examples', 'example_Pheno.json')
EXAMPLE_F2 = os.path.join(os.path.dirname(__file__), 'examples', 'F2_example.json')


def example_obj():
    with open(EXAMPLE, 'r') as file:
        return fromDict(json.load(file))


def example_pheno_obj():
    with open(EXAMPLE_PHENO, 'r') as file:
        return fromDict(json.load(file))


def example_f2_obj():
    with open(EXAMPLE_F2, 'r') as file:
        return fromDict(json.load(file))
