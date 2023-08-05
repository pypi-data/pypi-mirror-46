# Copyright 2019 Geneea Analytics s.r.o.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Extracts entities form G3 results stored as json-per-line to a tsv
"""

import argparse
import json
import sys

from typing import Tuple, Iterable
from geneeanlpclient.g3.model import G3
from geneeanlpclient.g3.reader import fromDict


def getEntities(analysis: G3) -> Iterable[Tuple[str, str, str, str]]:
    for e in analysis.entities:
        yield analysis.docId, e.id, e.stdForm, e.type


def main(args):
    with open(args.input, encoding='utf8') if args.input else sys.stdin as reader, \
         open(args.output, 'w', encoding='utf8') if args.output else sys.stdout as writer:

        for rawAnalysis in map(json.loads, reader):
            analysis = fromDict(rawAnalysis)
            for docId, eId, eType, eStdForm in getEntities(analysis):
                print(docId, eType, eStdForm, sep='\t', file=writer)


if __name__ == '__main__':
    argparser = argparse.ArgumentParser()
    argparser.add_argument("-i", "--input", help="Input file, result of G3 API stored as json-per-line")
    argparser.add_argument("-o", "--output", help="The resulting tsv file; columns: docid, entity type, entity std form")
    main(argparser.parse_args())
