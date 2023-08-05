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

from enum import Enum
from operator import attrgetter
from typing import Iterable, NamedTuple, List, Optional, Set

from geneeanlpclient.common.dictutil import DictBuilder, JsonType


class ParaSpec(NamedTuple):
    type: str
    """ Type of the paragraphs, typically one of Paragraph.TYPE_TITLE, Paragraph.TYPE_LEAD, Paragraph.TYPE_TEXT; 
    possibly Paragraph.TYPE_SECTION_HEADING  """
    text: str
    """ Text of the paragraph """


class AnalysisType(Enum):
    ALL = 1
    ENTITIES = 2
    TAGS = 3
    RELATIONS = 4
    SENTIMENT = 5
    LANGUAGE = 6

    def __str__(self):
        return self.name.lower()

    @staticmethod
    def parse(val: str) -> 'AnalysisType':
        val = val.strip().upper()
        for a in AnalysisType:
            if val == a.name:
                return a
        raise ValueError(f'invalid analysis type "{val}"')


class Request(NamedTuple):
    id: Optional[str]
    title: Optional[str]
    text: Optional[str]
    paraSpecs: Optional[List[ParaSpec]]
    analyses: Optional[Set[AnalysisType]]
    htmlExtractor: Optional[str]
    language: Optional[str]
    langDetectPrior: Optional[str]
    domain: Optional[str]
    textType: Optional[str]
    referenceDate: Optional[str]
    diacritization: Optional[str]
    returnMentions: bool
    returnItemSentiment: bool
    custom: JsonType

    class Builder:
        def setConfig(self, *,
            analyses: Iterable[AnalysisType] = None,
            htmlExtractor: str = None,
            language: str = None,
            langDetectPrior: str = None,
            domain: str = None,
            textType: str = None,
            referenceDate: str = None,
            # date the time references (e.g., next Tuesday) will be resolved to; formatted as YYYY-MM-DD
            diacritization: str = None,
            returnMentions: bool = False,
            returnItemSentiment: bool = False
        ) -> 'Request.Builder':
            self.analyses = set(analyses) if analyses else None
            self.htmlExtractor = htmlExtractor
            self.language = language
            self.langDetectPrior = langDetectPrior
            self.domain = domain
            self.textType = textType
            self.referenceDate = referenceDate
            self.diacritization = diacritization
            self.returnMentions = returnMentions
            self.returnItemSentiment = returnItemSentiment
            self.custom = {}
            return self

        def setCustom(self, custom: JsonType) -> 'Request.Builder':
            keyOverlap = Request.STD_KEYS & set(custom.keys())
            if keyOverlap:
                raise ValueError(f'custom keys {keyOverlap} do overlap with the STD keys')
            self.custom = custom
            return self

        def build(self, *,
            id: str = None,
            title: str = None,
            text: str = None,
            paraSpecs: List[ParaSpec] = None,
            language: str = None,
            referenceDate: str = None,
            custom: JsonType = None
        ) -> 'Request':
            if bool(text or title) == bool(paraSpecs):
                raise ValueError('You need to provide title/text or paraSpecs, but not both')

            return Request(
                id=id,
                title=title,
                text=text,
                paraSpecs=paraSpecs,
                analyses=self.analyses,
                htmlExtractor=self.htmlExtractor,
                language=language if language else self.language,
                langDetectPrior=self.langDetectPrior,
                domain=self.domain,
                textType=self.textType,
                referenceDate=referenceDate if referenceDate else self.referenceDate,
                diacritization=self.diacritization,
                returnMentions=self.returnMentions,
                returnItemSentiment=self.returnItemSentiment,
                custom=custom if custom else self.custom
            )

    STD_KEYS = frozenset([
        'id', 'title', 'text', 'paraSpecs', 'analyses', 'htmlExtractor', 'language', 'langDetectPrior', 'domain',
        'textType', 'referenceDate', 'diacritization', 'returnMentions', 'returnItemSentiment'
    ])

    @staticmethod
    def fromDict(raw: JsonType) -> 'Request':
        custom = {key: raw[key] for key in (raw.keys() - Request.STD_KEYS)}

        title, text = raw.get('title'), raw.get('text')
        paraSpecs = raw.get('paraSpecs')
        if bool(text or title) == bool(paraSpecs):
            raise ValueError('You need to provide title/text or paraSpecs, but not both')

        if 'analyses' in raw:
            analyses = set(AnalysisType.parse(a) for a in raw['analyses'])
        else:
            analyses = None

        return Request(
            id=raw.get('id'),
            title=title,
            text=text,
            paraSpecs=[ParaSpec(p['type'], p['text']) for p in paraSpecs] if paraSpecs else None,
            analyses=analyses,
            htmlExtractor=raw.get('htmlExtractor'),
            language=raw.get('language'),
            langDetectPrior=raw.get('langDetectPrior'),
            domain=raw.get('domain'),
            textType=raw.get('textType'),
            referenceDate=raw.get('referenceDate'),
            diacritization=raw.get('diacritization'),
            returnMentions=raw.get('returnMentions', False),
            returnItemSentiment=raw.get('returnItemSentiment', False),
            custom=custom
        )

    def toDict(self) -> JsonType:
        builder = DictBuilder({})
        builder.addIfNotNone('id', self.id)
        if self.paraSpecs:
            builder['paraSpecs'] = [{'type': p.type, 'text': p.text} for p in self.paraSpecs]
        else:
            builder.addIfNotNone('title', self.title)
            builder.addIfNotNone('text', self.text)
        if self.analyses:
            builder['analyses'] = [str(a) for a in sorted(self.analyses, key=attrgetter('value'))]
        builder.addIfNotNone('htmlExtractor', self.htmlExtractor)
        builder.addIfNotNone('language', self.language)
        builder.addIfNotNone('langDetectPrior', self.langDetectPrior)
        builder.addIfNotNone('domain', self.domain)
        builder.addIfNotNone('textType', self.textType)
        builder.addIfNotNone('referenceDate', self.referenceDate)
        builder.addIfNotNone('diacritization', self.diacritization)
        if self.returnMentions:
            builder['returnMentions'] = True
        if self.returnItemSentiment:
            builder['returnItemSentiment'] = True
        return {
            **builder.build(),
            **self.custom
        }
