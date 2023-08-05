import json
from unittest import TestCase

from pathlib import Path

from geneeanlpclient.common.dictutil import JsonType
from geneeanlpclient.common.ud import UDep
from geneeanlpclient.g3.reader import fromDict
from geneeanlpclient.g3.writer import toDict

from tests.geneeanlpclient.g3.examples import EXAMPLE_PHENO


class TestRW(TestCase):

    @staticmethod
    def _replaceClauseByRoot(dictG3: JsonType) -> None:
        """
        Utility class to replace all 'clause' functions in tokens by 'root'. Readers replace clause by root.
        Clause is a deprecated non-UD function, equivalent to root.
        """

        for para in dictG3.get('paragraphs', []):
            for sentence in para.get('sentences', []):
                for token in sentence.get('tokens', []):
                    if token.get('fnc') == 'clause':
                        token['fnc'] = 'root'

    def test_read_write(self):
        self.maxDiff = None

        for exampleFile in Path('examples').glob('example*.json'):
            with exampleFile.open() as file:
                obj = fromDict(json.load(file))

            actual = toDict(obj)

            with exampleFile.open() as file:
                expected = json.load(file)
                if expected.get('itemSentiments') == {}:
                    del expected['itemSentiments']
                TestRW._replaceClauseByRoot(expected)

            self.assertDictEqual(expected, actual)

    def test_tokens(self):
        with open(EXAMPLE_PHENO, 'r') as file:
            obj = fromDict(json.load(file))

            token0 = obj.paragraphs[0].sentences[0].tokens[0]  # Angela

            self.assertEqual(token0.id, 't0')
            self.assertEqual(token0.text, 'Angela')
            self.assertEqual(token0.charSpan.start, 0)
            self.assertEqual(token0.charSpan.end, 6)
            self.assertEqual(token0.corrText, 'Angela')
            self.assertEqual(token0.corrCharSpan.start, 0)
            self.assertEqual(token0.corrCharSpan.end, 6)
            self.assertEqual(token0.deepLemma, 'Angela')
            self.assertEqual(token0.lemma, None)  # missing
            self.assertEqual(token0.morphTag, 'NNP')
            self.assertEqual(token0.fnc, UDep.COMPOUND)
            self.assertEqual(token0.feats, {"lemmaSrc": "THIRD_PARTY", "negated": "false"})

            self.assertEqual(token0.parent.text, 'Merkel')
            self.assertEqual(token0.children, [])
            self.assertEqual(token0.previous(), None)
            self.assertEqual(token0.next().text, 'Merkel')
