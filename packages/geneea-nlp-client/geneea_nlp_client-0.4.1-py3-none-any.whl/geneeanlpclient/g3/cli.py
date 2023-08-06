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
The command-line interface to Geneea NLP REST API v3.
"""
import json
import sys

from argparse import ArgumentParser

from geneeanlpclient import g3


def main(args):
    with open(args.inputFile, 'r', encoding='utf-8') if args.inputFile else sys.stdin as input, \
         open(args.outputFile, 'w', encoding='utf-8') if args.outputFile else sys.stdout as output, \
         g3.Client.create(userKey=args.userkey if args.userkey else None) as analyzer:

        requestBuilder = g3.Request.Builder()

        for idx, text in enumerate(input):
            analysis = analyzer.analyze(requestBuilder.build(id=str(idx), text=text))
            print(json.dumps(analysis, ensure_ascii=False), file=output)


if __name__ == '__main__':
    argparser = ArgumentParser()
    argparser.add_argument("-i", "--inputFile", default=None)
    argparser.add_argument("-o", "--outputFile", default=None)
    argparser.add_argument("-k", "--userkey", default=None)
    args = argparser.parse_args()

    main(args)
