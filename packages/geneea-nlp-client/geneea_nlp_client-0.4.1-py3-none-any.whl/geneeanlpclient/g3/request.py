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
    """ The linguistic analyses the G3 API can perform; `more detail <https://help.geneea.com/api_general/guide/analyses.html>`__"""
    ALL = 1
    """ Perform all analyses at once """
    ENTITIES = 2
    """ Recognize and standardize entities in text. `more detail <https://help.geneea.com/api_general/guide/entities.html>`__"""
    TAGS = 3
    """ Assign semantic tags to a document. `more detail <https://help.geneea.com/api_general/guide/tags.html>`__"""
    RELATIONS = 4
    """ Relations between entities and their attributes `more detail <https://help.geneea.com/api_general/guide/relations.html>`__"""
    SENTIMENT = 5
    """ Detect the emotions of the author contained in the text. `more detail <https://help.geneea.com/api_general/guide/sentiment.html>`__"""
    LANGUAGE = 6
    """ Detect the language the text is written in. `more detail <https://help.geneea.com/api_general/guide/language.html>`__"""

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
    """ Unique identifier of the document """
    title: Optional[str]
    """ The title or subject of the document, when available; mutually exclusive with the ``paraSpecs`` parameter """
    text: Optional[str]
    """ The main text of the document; mutually exclusive with the ``paraSpecs`` parameter """
    paraSpecs: Optional[List[ParaSpec]]
    """ The document paragraphs; mutually exclusive with `title` and `text` parameters. """
    analyses: Optional[Set[AnalysisType]]
    """ What analyses to return """
    htmlExtractor: Optional[str]
    """ Text extractor to be used when analyzing HTML document. """
    language: Optional[str]
    """ The language of the document as ISO 639-1; auto-detection will be used if omitted. """
    langDetectPrior: Optional[str]
    """ The language detection prior; e.g. ‘de,en’. """
    domain: Optional[str]
    """ The source domain from which the document originates. See the `available domains <https://help.geneea.com/api_general/guide/domains.html>`__. """
    textType: Optional[str]
    """ The type or genre of text; not supported in public workflows/domains yet. """
    referenceDate: Optional[str]
    """ Date to be used for the analysis as a reference; values: “NOW” or in format YYYY-MM-DD. """
    diacritization: Optional[str]
    """ Determines whether to perform text diacritization """
    returnMentions: bool
    """ Should entity/tag/relation mentions be returned? No mentions are returned if None. """
    returnItemSentiment: bool
    """ Should entity/mention/tag/relation etc. sentiment be returned? No sentiment is returned if None """
    custom: JsonType

    class Builder:

        def __init__(
            self, *,
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
            returnItemSentiment: bool = False,
            customConfig: JsonType = None
        ) -> None:
            """
            Create a builder with fields meant to be shared across requests

            :param analyses: What analyses to return.
            :type analyses: List[AnalysisType]
            :param htmlExtractor: Text extractor to be used when analyzing HTML document.
            :param language: The language of the document as ISO 639-1; auto-detection will be used if omitted.
            :param langDetectPrior: The language detection prior; e.g. ‘de,en’.
            :param domain: The source domain from which the document originates. See the `available domains <https://help.geneea.com/api_general/guide/domains.html>`__.
            :param textType: The type or genre of text; not supported in public workflows/domains yet.
            :param referenceDate: Date to be used for the analysis as a reference; values: “NOW” or in format YYYY-MM-DD.
            :param diacritization: Determines whether to perform text diacritization
            :param returnMentions: Should entity/tag/relation mentions be returned? No mentions are returned if None.
            :param returnItemSentiment: Should entity/mention/tag/relation etc. sentiment be returned? No sentiment is returned if None
            :return: The builder for fluent style chaining.
            """
            self.analyses = set(analyses) if analyses is not None else analyses
            self.htmlExtractor = htmlExtractor
            self.language = language
            self.langDetectPrior = langDetectPrior
            self.domain = domain
            self.textType = textType
            self.referenceDate = referenceDate
            self.diacritization = diacritization
            self.returnMentions = returnMentions
            self.returnItemSentiment = returnItemSentiment
            self.setCustomConfig(**(customConfig or {}))

        def setCustomConfig(self, **customConfig) -> 'Request.Builder':
            """
            Sets custom options to the request builder.

            :param customConfig: Any custom options passed to the G3 API endpoint
            :return: The builder for fluent style chaining.
            """
            keyOverlap = Request.STD_KEYS & set(customConfig.keys())
            if keyOverlap:
                raise ValueError(f'custom keys {keyOverlap} overlap with the standard request keys')
            self.customConfig = customConfig
            return self

        def build(self, *,
            id: str = None,
            title: str = None,
            text: str = None,
            paraSpecs: List[ParaSpec] = None,
            language: str = None,
            referenceDate: str = None,
            customConfig: JsonType = None
        ) -> 'Request':
            """
            Creates a new request object to be passed to the G3 client.

            :param id: Unique identifier of the document
            :param title: The title or subject of the document, when available; mutually exclusive with the ``paraSpecs`` parameter
            :param text: The main text of the document; mutually exclusive with the ``paraSpecs`` parameter
            :param paraSpecs: The document paragraphs; mutually exclusive with `title` and `text` parameters.
            :type  paraSpecs: List[ParaSpec]
            :param language: The language of the document as ISO 639-1; auto-detection will be used if None.
            :param referenceDate: Date to be used for the analysis as a reference; values: ``NOW`` or in format YYYY-MM-DD
            :param customConfig: Any custom options passed to the G3 API endpoint
            :return: Request object to be passed to the G3 client.
            :rtype: Request
            """
            if bool(text or title) == bool(paraSpecs):
                raise ValueError('You need to provide title/text or paraSpecs, but not both')

            if customConfig is not None and self.customConfig:
                customConfig = dict(self.customConfig).update(customConfig)

            return Request(
                id=id,
                title=title,
                text=text,
                paraSpecs=paraSpecs,
                analyses=self.analyses,
                htmlExtractor=self.htmlExtractor,
                language=language if language is not None else self.language,
                langDetectPrior=self.langDetectPrior,
                domain=self.domain,
                textType=self.textType,
                referenceDate=referenceDate if referenceDate is not None else self.referenceDate,
                diacritization=self.diacritization,
                returnMentions=self.returnMentions,
                returnItemSentiment=self.returnItemSentiment,
                custom=customConfig if customConfig is not None else self.customConfig
            )

    STD_KEYS = frozenset([
        'id', 'title', 'text', 'paraSpecs', 'analyses', 'htmlExtractor', 'language', 'langDetectPrior', 'domain',
        'textType', 'referenceDate', 'diacritization', 'returnMentions', 'returnItemSentiment'
    ])
    """ Standard keys used by the G3 request. """

    @staticmethod
    def fromDict(raw: JsonType) -> 'Request':
        """ Reads a request object from a json-like dictionary. """
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
        """ Converts the request object to a json-like dictionary. """
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
