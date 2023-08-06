from unittest import TestCase

from geneeanlpclient.g3 import AnalysisType, Request
from tests.geneeanlpclient.g3.examples import example_req_js


class TestRequest(TestCase):

    def test_simple_build(self):
        req = Request.Builder().build(text='Unit Test')
        self.assertDictEqual(
            {'text': 'Unit Test'}, req.toDict()
        )

    def test_read_and_write(self):
        exampleReqDict = example_req_js()

        bldr = Request.Builder(
            analyses=[AnalysisType.ENTITIES, AnalysisType.SENTIMENT],
            domain='news',
            returnMentions=True,
            returnItemSentiment=True
        ).setCustomConfig(custom_key=['custom value'])

        builtReq = bldr.build(
            title='Angela Merkel in New Orleans',
            text='Angela Merkel left Germany. She move to New Orleans to learn jazz. That\'s amazing.'
        )

        exmapleReq = Request.fromDict(exampleReqDict)
        self.assertTupleEqual(exmapleReq, builtReq)
        self.assertDictEqual(exampleReqDict, exmapleReq.toDict())
