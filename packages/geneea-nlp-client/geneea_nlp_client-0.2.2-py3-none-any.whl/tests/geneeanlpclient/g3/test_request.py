from unittest import TestCase

from geneeanlpclient.g3 import AnalysisType, Request
from tests.geneeanlpclient.g3.examples import example_req_js


class TestRequest(TestCase):

    def test_read_and_write(self):
        jsReq = example_req_js()

        bldr = Request.Builder()
        bldr.setConfig(
            analyses=[AnalysisType.ENTITIES, AnalysisType.SENTIMENT],
            domain='news',
            returnMentions=True,
            returnItemSentiment=True
        )
        bldr.setCustom({'custom_key': ['custom value']})
        expected = bldr.build(
            title='Angela Merkel in New Orleans',
            text='Angela Merkel left Germany. She move to New Orleans to learn jazz. That\'s amazing.'
        )

        req = Request.fromDict(jsReq)
        self.assertEqual(expected, req)
        self.assertEqual(jsReq, req.toDict())
