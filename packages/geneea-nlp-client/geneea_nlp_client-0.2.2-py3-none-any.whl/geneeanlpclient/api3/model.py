# coding=utf-8

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
Objects encapsulating the result of full analysis.
Basic objects:
* X3 - analysis of a single document
* Paragraph, Sentence
* Entity, EntityMention
* Tag
* Relation, Argument
* objects related to tokens and tecto tokens:
    * _Node - abstract base class for Token and TectoToken with support for labeled ordered tree
    * TokenUtils - general utility classes for manipulating lists of tokens and tectotokens
    * Tree - class encapsulating ordered rooted trees of tokens or tecto tokens
    * TreeBuilder - builder for syntactic and tecto trees (tokens and tecto tokens should not be constructed directly)
    * Token - surface token (basic unit of morphology and surface syntax)
    * TokenSupport - list of tokens within a sentence (used for EntityMention, TectoTokens, etc)
    * TectoToken - tectogrammatical token (basic unit of deep syntax)

TODO
* check if text of paragraph, sentence, token is before or after correction
"""

from abc import ABC
from itertools import chain
from typing import Any, TypeVar, Generic, Union, Optional, List, Callable, Iterable, Dict, Mapping, Sequence, NamedTuple

from geneea.analyzer import ud
from geneea.analyzer.common import CharSpan, isSequential


class Sentiment(NamedTuple):
    """ Class encapsulating sentiment of a document, sentence or relation. """
    mean: float
    """ Average sentiment. """
    label: Optional[str]
    """ Human readable label describing the average sentiment. """
    positive: Optional[float]
    """ Average sentiment of positive items. """
    negative: Optional[float]
    """ Average sentiment of negative items. """


class Language(NamedTuple):
    detected: str
    """ Language of document as detected. """
    analysis: str
    """ Language of the workflow used for analysis. """


Node = TypeVar('Node', bound='_Node')


class _Node(ABC, Generic[Node]):
    """
    This is an implementation class, used as a super class of Token and Tectotoken.
    We use the word token to refer to both tokens and tecto-tokens.
    In general, we assume that any tree can be non-projective  (i.e. generate by context-sensitive grammar).

    All nodes in the tree should be of the same type: either all Tokens or all TectoTokens.
    Unfortunately, Python does not support Self type, so when returning a node or nodes, we cannot mark them as of type
    Self. We pass the concrete type via the generic type Node. When returning nodes we annotate them as being of the
    type Node and ignore the warnings that the are of the type _Node[Node] and not Node.
    """

    def __init__(self, *,
            idx: int,
            fnc: Union[str, ud.Dep]) -> None:
        self._idx = idx
        """ Zero-based index of the token within the sentence. """
        self.fnc = fnc
        """ Label of the dependency edge. """
        self._parent: Optional[Node] = None
        """ Tokens that this token depends on. None for the root. """
        self._children: List[Node] = []
        """ Tokens that depend of this token, ordered by word-order. """
        self.sentence: 'Sentence' = None
        """ Sentence this token belongs to. """

    @property
    def parent(self) -> Optional[Node]:
        """ Dependency parent of this token. None if this token is the root of the sentence. """
        return self._parent

    @property
    def children(self) -> List[Node]:
        """ Dependents of this token ordered by word-order. """
        return self._children

    @property
    def idx(self) -> int:
        """ Zero-based index of this token reflecting its word-order position within the sentence. """
        return self._idx

    @property
    def isLeaf(self) -> bool:
        """ Check whether this token is a leaf (i.e has no dependents). """
        return len(self._children) == 0

    @property
    def isRoot(self) -> bool:
        """ Check whether this token is the root of the sentence. """
        return self._parent is None

    def coverage(self, reflexive=True, ordered=True) -> List[Node]:
        """
        All tokens dominated by this token.
        @param reflexive: whether this token itself is included
        @param ordered: whether should the result be ordered by word order
        @return: coverage of this token
        """
        chunks = [c.coverage(ordered=False) for c in self._children]

        if reflexive:
            chunks += [[self]]

        tokens = list(chain.from_iterable(chunks))

        if ordered:
            tokens = sorted(tokens, key=lambda t: t._idx)

        return tokens

    @property
    def isContinuous(self) -> bool:
        """
        Checks if the phrase dominated by this token is continuous.
        """
        cov = self.coverage()
        return (cov[-1]._idx - cov[0]._idx) == len(cov) - 1  # indices must form a continuous sequence.

    @property
    def leftChildren(self) -> List[Node]:
        """
        Children of this token that precede it.
        """
        return [c for c in self._children if c._idx < self._idx]

    @property
    def rightChildren(self) -> List[Node]:
        """
        Children of this token that follow it.
        """
        return [c for c in self._children if c._idx > self._idx]

    @property
    def depth(self) -> int:
        """
        Depth of this token in the dependency tree.
        @return  distance, i.e. number of dependency edges, from the root of the sentence
        """
        if self._parent:
            return self._parent.depth + 1
        else:
            return 0

    def inOrder(self) -> Iterable[Node]:
        """
        In-order iterator over the subtree of this token.
        """
        for c in self.leftChildren:
            yield from c.inOrder()

        yield self

        for c in self.rightChildren:
            yield from c.inOrder()

    def filteredInOrder(self, skipPredicate: Callable[[Node], bool], includeFilteredRoot=True) -> Iterable[Node]:
        """
        In-order iterator over the subtree of this token which optionally skips some subtrees.
        @param skipPredicate: when this predicate is true on any token, the token's subtree is not traversed
        @param includeFilteredRoot: if true the tokens on which skipPredicate function returns true are included in the result;
        otherwise they are not
        """
        if skipPredicate(self):
            if includeFilteredRoot:
                yield self
        else:
            for c in self.leftChildren:
                yield from c.filteredInOrder(skipPredicate, includeFilteredRoot)

            yield self

            for c in self.rightChildren:
                yield from c.filteredInOrder(skipPredicate, includeFilteredRoot)

    def preOrder(self) -> Iterable[Node]:
        """
        Pre-order iterator over the subtree of this token.
        """
        yield self

        for c in self._children:
            yield from c.preOrder()

    def filteredPreOrder(self, skipPredicate: Callable[[Node], bool], includeFilteredRoot=True) -> Iterable[Node]:
        """
        Pre-order iterator over the subtree of this token which optionally skips some subtrees.
        @param skipPredicate: when this predicate is true on any token, the token's subtree is not traversed
        @param includeFilteredRoot: if true the tokens on which skipPredicate function returns true are included in the result;
        """
        if skipPredicate(self):
            if includeFilteredRoot:
                yield self
        else:
            yield self

            for c in self._children:
                yield from c.filteredPreOrder(skipPredicate, includeFilteredRoot)

    def toSimpleString(self) -> str:
        """ Converts the token to a default non-recursive string; overriden in subclasses """
        return str(self.idx)

    def toTreeString(self, printToken: Callable[[Node], str]) -> str:
        """
        Parenthesised representation of this tree.
        @param printToken: function printing individual tokens
        @return: string representation of the tree rooted in this token
        """
        if self._children:
            childrenStr = ','.join([c.toTreeString(printToken) for c in self._children])
            return printToken(self) + '(' + childrenStr + ')'
        else:
            return printToken(self)

    def toIndentTreeString(self, printToken: Callable[[Node], str], indentStr: str='   ', depth: int=0) -> str:
        """
        Indented representation of this tree.
        @param printToken: function printing individual tokens
        @param indentStr: string used to indent each level from the previous one
        @param depth: indentation level to start with
        @return: string representation of the tree rooted in this token
        """
        if self._children:
            childrenStr = '\n'.join([c.toIndentTreeString(printToken, indentStr=indentStr, depth=depth + 1) for c in self._children])
            childrenStr = f'\n{childrenStr}\n'
        else:
            childrenStr = ''

        return depth*indentStr + printToken(self) + childrenStr

    def toSimpleTreeString(self) -> str:
        """
        Simple representation of this tree using toSimpleString to convert individual nodes.
        """
        return self.toTreeString(lambda t: t.toSimpleString())

    def toSimpleIndentTreeString(self) -> str:
        """
        Simple indented representation of this tree using toSimpleString to convert individual nodes.
        """
        return self.toIndentTreeString(lambda t: t.toSimpleString())


class TokenUtils:
    @staticmethod
    def sorted(tokens: Sequence[Node]) -> Sequence[Node]:
        """
        Orders a list of tokens by word-order (i.e. their sentence index).
        Requires the tokens to be from the same sentence (not checked).
        @return: sorted list of tokens
        """
        return sorted(tokens, key=lambda t: t.idx)

    @staticmethod
    def isSorted(tokens: Sequence[Node]) -> bool:
        """
        Checks if a list of tokens is sorted by word-order (i.e. their sentence index).
        Requires the tokens to be from the same sentence (not checked).
        """
        return all(tokens[i].idx < tokens[i+1].idx for i in range(len(tokens)-1))

    @staticmethod
    def isFromSameSentence(tokens: Sequence[Node]) -> bool:
        """
        Checks if all the tokens come from the same sentence.
        @return: true if the list of tokens is empty, all they are all within the same sentence, false otherwise.
        """
        return all(tokens[i].sentence == tokens[i+1].sentence for i in range(len(tokens)-1))

    @staticmethod
    def isContinuous(tokens: Sequence[Node]) -> bool:
        """
        Checks if the tokens form a continuous sequence.
        Assumes the tokens to be sorted and from the same sentence (not checked).
        @return: true if the list is continuous, false otherwise.
        """
        return isSequential([t.idx for t in tokens])

    @staticmethod
    def toSimpleString(tokens: Sequence[Node], quote: bool=False) -> str:
        """
        Utility method for creating strings with a simplified token list.
        @param tokens: tokens to print
        @param quote: surround each node string with single quotes; useful for __repr__ string
        """
        if quote:
            return '[' + ', '.join('\'' + c.toSimpleString() + '\'' for c in tokens) + ']'
        else:
            return '[' + ', '.join(c.toSimpleString() for c in tokens) + ']'


class Tree(Generic[Node]):
    def __init__(self,
            root: Node,
            tokens: Sequence[Node]) -> None:
        self.root = root
        self.tokens = tokens


class TreeBuilder(Generic[Node]):
    """ Builder creating a dependency tree out of tokens. """

    def __init__(self) -> None:
        self._nodes: List[Node] = []
        self._deps: Dict[int, int] = {}

    def addNode(self, node: Node) -> 'TreeBuilder[Node]':
        """
        Record a single token as a node of the tree.
        @param node: token to add. Its index must be correct, parent and children fields are ignored.
        @return: the builder to allow chained calls
        """
        self._nodes.append(node)
        return self

    def addNodes(self, nodes: Iterable[Node]) -> 'TreeBuilder[Node]':
        """
        Record a collection of tokens as nodes of the tree.
        @param nodes: tokens to add. Their index must be correct, parent and children fields are ignored.
        @return: the builder to allow chained calls
        """
        self._nodes.extend(nodes)
        return self

    def addDependency(self, childIdx: int, parentIdx: int) -> 'TreeBuilder[Node]':
        """
        Record a dependency edge. The tokens connected by the edge might be added later.
        @param childIdx: index of the child token (note: tokens are indexed within their sentences)
        @param parentIdx: index of the parent token (note: tokens are indexed within their sentences)
        @return: the builder to allow chained calls
        """
        if childIdx < 0:
            raise ValueError(f'Negative node index {childIdx}.')
        if parentIdx < 0:
            raise ValueError(f'Negative node index {parentIdx}.')
        if childIdx == parentIdx:
            raise ValueError(f'Dependency edge cannot be reflexive.')
        if childIdx in self._deps and self._deps[childIdx] != parentIdx:
            raise ValueError(f'Node {childIdx} has multiple parents.')

        self._deps[childIdx] = parentIdx
        return self

    def addDummyDependecies(self):
        """ All nodes are hanged to the first one. """
        if self._deps:
            raise ValueError('Dummy dependencies cannot be added when other dependencies have been specified.')
        if not self._nodes:
            return

        self._nodes.sort(key=lambda t: t._idx)
        for n in self._nodes[1:]:
            self.addDependency(n.idx, 0)

    def _fillParents(self):
        maxIdx = len(self._nodes) - 1
        for c, p in self._deps.items():
            if maxIdx < c:
                raise ValueError(f'The child of the dependency edge {c} -> {p} is out of range (max={maxIdx}).')
            if maxIdx < p:
                raise ValueError(f'The parent of the dependency edge {c} -> {p} is out of range (max={maxIdx}).')

            self._nodes[c]._parent = self._nodes[p]

    def _findRoot(self):
        roots = [n for n in self._nodes if not n.parent]

        if len(roots) == 0:
            raise ValueError('No root.')
        if len(roots) > 1:
            raise ValueError('Multiple roots.')

        return roots[0]

    def _fillChildren(self):
        for n in self._nodes:
            n._children = [c for c in self._nodes if c._parent == n]

    def build(self) -> Optional[Tree[Node]]:
        if not self._nodes:
            return None

        """ Creates an ordered dependency tree  based on the contents this builder. """
        self._nodes = sorted(self._nodes, key=lambda t: t._idx)

        if not isSequential([n.idx for n in self._nodes]) or self._nodes[0].idx != 0:
            raise ValueError(f'Indexes are not sequential.')

        self._fillParents()
        root = self._findRoot()  # exactly one root check; addDependency checks for multiple parents => tree
        self._fillChildren()

        return Tree[Node](tokens=self._nodes, root=root)


class Token(_Node):
    """
    A token including basic morphological and syntactic information.
    A token is similar to a word, but includes punctuation.
    Tokens have an zero-based index reflecting their position within their sentence.
    """

    def __init__(self, *,
            idx: int,
            text: str,
            charSpan: CharSpan,
            deepLemma: str,
            surfaceLemma: str,
            lemmaInfo: List[str],
            pos: ud.Pos,
            feats: ud.UFeats,
            morphTag: str,
            fnc: str
    ) -> None:
        _Node.__init__(self, idx=idx, fnc=fnc)
        self.text = text
        """ Text of this token (after correction) """  # TODO check if it after, before or in the middle of correction
        self.charSpan = charSpan
        """ character span within the paragraph """
        self.deepLemma = deepLemma
        """ lemma of the token e.g. bezpecny """
        self.surfaceLemma = surfaceLemma
        """ simple lemma of the token, e.g.nejnebezpecnejsi (in Cz, includes negation and grade) """
        self.lemmaInfo = lemmaInfo
        """ lemma info: semantic flags describing the word e.g. ;G for geographical names, 
            contains UNKNOWN if the lemma is not known """
        self.pos = pos
        """ Google universal tagset (coming soon) """
        self.feats = feats
        """ universal features """
        self.morphTag = morphTag
        """ morphological tag, e.g. AAMS1-...., VBD, ... """

    def __repr__(self) -> str:
        return ('Token('
            f'idx={self.idx!r}, fnc={self.fnc!r}, text={self.text!r}, fnc={self.charSpan!r}, '
            f'deepLemma={self.deepLemma!r}, surfaceLemma={self.surfaceLemma!r}, lemmaInfo={self.lemmaInfo!r}, '
            f'pos={self.pos!r}, morphTag={self.morphTag!r}, '
            f'children={TokenUtils.toSimpleString(self.children, quote=True)}, '
            f'parent={self.parent.toSimpleString() if self.parent else -1!r})')

    @property
    def isUnknown(self):
        """
        The token is unknown to the lemmatizer. The lemma provided is the same as the token itself.
        """
        return 'UNKNOWN' in self.lemmaInfo

    def offsetToken(self, offset: int) -> Optional['Token']:
        """
        Token following or preceding this token within the sentence
        @param offset: relative offset. The following tokens have a positive offset,
            preceding a negative one. The ext token has offset = 1.
        @return the token at the relative offset or None if the offset is invalid
        """
        tokens = self.sentence.tokens
        if 0 <= self.idx + offset < len(tokens):
            return tokens[self.idx + offset]
        else:
            return None

    def previous(self) -> Optional['Token']:
        """
        The previous token or None if this token is sentence initial.
        """
        return self.offsetToken(-1)

    def next(self) -> Optional['Token']:
        """
        The next token or None if this token is sentence final.
        """
        return self.offsetToken(1)

    def toSimpleString(self) -> str:
        """ Converts the token to a default non-recursive string: index + text """
        return self.toStringITx()

    def toStringITx(self) -> str:
        """ Converts the token to a non-recursive string: index + text """
        return f'{self.idx}:{self.text}'

    def toStringITxF(self) -> str:
        """ Converts the token to a non-recursive string: index + text + function """
        return f'{self.idx}:{self.text}:{self.fnc}'


class TokenSupport(NamedTuple):
    """
    Tokens within a single sentence; ordered by word-order; non-empty, continuous or discontinuous.
    Do not construct directly, use TokenSupport.of
    """
    tokens: Sequence[Token]
    """ The tokens of this support. """
    isContinuous: bool
    """ Is this support a continuous sequence of tokens, i.e. a token span? """

    @staticmethod
    def of(tokens: Sequence[Token]) -> 'TokenSupport':
        """
        Creates a TokenSupport object from a list of tokens.
        @param tokens: non-empty list of tokens (might not be sorted)
        """
        if not tokens:
            raise ValueError("Tokens cannot be None or empty")
        if not TokenUtils.isFromSameSentence(tokens):
            raise ValueError("Tokens are not from the same sentence.")
        tokens = TokenUtils.sorted(tokens)
        isContinuous = TokenUtils.isContinuous(tokens)
        return TokenSupport(tokens, isContinuous)

    def __repr__(self) -> str:
        return f'TokenSupport(tokens={TokenUtils.toSimpleString(self.tokens, quote=True)}, isContinuous={self.isContinuous})'

    def spans(self) -> Iterable['TokenSupport']:
        """
        Breaks this token support into continuous sub-sequences of tokens.
        @return: series of token supports together equivalent to this token support
        """
        if self.isContinuous:
            yield self
        else:
            start = 0
            prev = self.tokens[0]
            for i in range(1, len(self.tokens)):
                cur = self.tokens[i]
                if prev.idx + 1 != cur.idx:
                    yield TokenSupport(self.tokens[start:i], isContinuous=True)
                    start = i
                prev = cur

            yield TokenSupport(self.tokens[start:], isContinuous=True)

    @property
    def sentence(self) -> 'Sentence':
        return self.tokens[0].sentence

    def len(self) -> 'int':
        """ Number of covered tokens. """
        return len(self.tokens)

    def __len__(self) -> int:
        """ Number of covered tokens. """
        return len(self.tokens)

    @property
    def first(self) -> Token:
        """ The first token. """
        return self.tokens[0]

    @property
    def last(self) -> Token:
        """ The last token. """
        return self.tokens[-1]

    @property
    def charSpan(self) -> CharSpan:
        """ The character span between the first and last token relative to the enclosing sentence;
        for discontinuous support this includes intervening gaps. """
        return CharSpan(self.firstCharIdx, self.lastCharIdx)

    @property
    def firstCharIdx(self) -> int:
        """ Index of the first character within the enclosing sentence. """
        return self.first.charSpan.start

    @property
    def lastCharIdx(self) -> int:
        """ Index of the last character within the enclosing sentence. """
        return self.last.charSpan.end

    def texts(self) -> List[str]:
        """ The coverage texts of each of the continuous spans, ordered by word-order."""
        return [s.text for s in self.spans()]

    @property
    def text(self) -> str:
        """
        Substring of a full text as denoted by this support (before correction).
        For discontinuous supports, the result includes the intervening gaps.
        From `' '.join(tokenSupport.texts())` differs in correctly reflecting whitespace in the original text.
        """
        return self.charSpan.extractText(self.sentence.text)


class TectoToken(_Node['TectoToken']):
    """
    A tecto token, i.e. a tectogrammatical abstraction of a word (e.g. 'did not sleep' are three tokens but a single
    tecto-token)
    Tecto tokens have an zero-based index reflecting their position within their sentence.
    """

    def __init__(self, *,
            idx: int,
            fnc: str,
            lemma: str,
            features: Dict[str, str],
            tokens: TokenSupport,
            entityMention: Optional['EntityMention'] = None,
            entity: Optional['Entity'] = None) -> None:
        _Node.__init__(self, idx=idx, fnc=fnc)
        self.lemma = lemma
        """ Tecto lemma  """
        self.features = features
        """ Grammatical and other features of the tecto token """
        self.tokens = tokens
        """ Surface tokens associated with this tecto token; ordered by word-order """
        self.entityMention = entityMention
        """ Entity mention associated with this tecto token; None if there is no such entity. """
        self.entity = entity
        """ Entity associated with this tecto token; None if there is no such entity. For F2, not in X3 """

    def __repr__(self):
        return ('TectoToken('
            f'idx={self.idx!r}, fnc={self.fnc!r}, text={self.lemma!r}, '
            f'features={self.features!r}, '
            f'tokens={self.tokens!r}, '
            f'entityMention={self.entityMention!r}, entity={self.entity!r}, '
            f'children={TokenUtils.toSimpleString(self.children, quote=True)}, '
            f'parent={self.parent.toSimpleString() if self.parent else -1!r})')

    def toSimpleString(self) -> str:
        """ Converts the tecto token to a default non-recursive string: index + lemma """
        return self.toStringIL()

    def toStringIL(self) -> str:
        """ Converts the tecto token to a non-recursive string: index + lemma """
        return f'{self.idx}:{self.lemma}'

    def toStringILF(self) -> str:
        """ Converts the tecto token to a non-recursive string: index + lemma + function """
        return f'{self.idx}:{self.lemma}:{self.fnc}'


class EntityMention:

    def __init__(self, *,
            text: str,
            lemma: Optional[List[str]],
            tokens: TokenSupport,
            sentiment: Optional[float]) -> None:
        self.text = text
        """ The form of this entity mention, as it occurs in the text. """
        self.lemma = lemma
        """ Lemma of this entity (potentially multiword lemma), i.e. base form of the entity expression. 
            Note: Not supported yet. """
        self.tokens: TokenSupport = tokens
        """ Tokens of this entity mention. """
        self.sentiment = sentiment
        """ Sentiment of this mention. Note: Not supported yet. """

    @property
    def sentence(self) -> 'Sentence':
        """
        Sentence containing this entity mention.
        "Entity mention belongs to maximally one sentence; artificial mentions without tokens belong to no sentence.
        """
        return self.tokens.sentence

    @property
    def isContinuous(self) -> bool:
        return self.tokens.isContinuous

    def __repr__(self):
        return ('EntityMention('
            f'text={self.text!r}, lemma={self.lemma!r}, '
            f'tokens={self.tokens!r}, sentiment={self.sentiment!r})')


class Entity:
    def __init__(self, *,
            uid: str=None,
            stdForm: str,
            entityType: str,
            weight: float=None,
            features: Dict[str, str],
            mentions: List[EntityMention]) -> None:
        self.uid = uid
        """ Knowledge-base id """
        self.stdForm = stdForm
        """ Standard form of this entity """
        self.type = entityType
        """ Basic type of this entity (e.g. person, location, ...)"""
        self.weight = weight
        """ Entity relevance, relative to the document. Not supported in F2. """
        self.features = features
        """ Any features/properites derived from KB ID, returned for convenience (e.g. Timex in HR format, customer id, ...)"""
        self.mentions = mentions
        """ Actual occurrences of this entity in the text """

    def __repr__(self):
        return ('Entity('
            f'uid={self.uid!r}, stdForm={self.stdForm!r}, '
            f'type={self.type!r}, weight={self.weight!r}, '
            f'features={self.features!r}, mentions={self.mentions!r})')

    def __hash__(self):
        return hash((self.uid, self.stdForm, self.type))


class Tag:
    TYPE_TOPIC = 'topic'
    """ Type of the tag with the main topic of the document in F2 """
    TYPE_TOPIC_DISTRIBUTION = 'topic.distribution'
    """ Type of the tags with the topic distribution of the document in F2 """

    def __init__(self, *,
            uid: Optional[str],
            text: str,
            tagType: str,
            relevance: float,
            features: Mapping[str, str],
            mentions: List[EntityMention]) -> None:
        self.uid = uid
        self.text = text
        self.type = tagType
        self.relevance = relevance
        self.features = features
        self.mentions = mentions

    def __repr__(self):
        return ('Tag('
            f'uid={self.uid!r}, text={self.text!r}, '
            f'type={self.type!r}, weight={self.relevance!r}, '
            f'features={self.features!r}, mentions={self.mentions!r})')


class Argument(NamedTuple):
    name: str
    type: str
    """ subj, obj """
    entity: Entity
    """ The entity corresponding to this argument, if any. None if the argument is not an entity. """


class Relation:
    TYPE_ATTR = 'attr'
    """ Attribute relation (e.g. `good(pizza)` for _good pizza_, _pizza is good_), the attribute is  """
    TYPE_RELATION = 'relation'
    """ Verbal relation (e.g. `eat(pizza)` for _eat a pizza._"""
    TYPE_EXTERNAL = 'external'
    """ Relation where at least one argument is outside of the the document (e.g. between `pizza` in the document and 
    `food` item in the knowledgebase) """

    def __init__(self,
            stdForm: Optional[str],
            name: str,
            relationType: str,
            args: List[Argument],
            negation: bool,
            features: Mapping[str, str],
            tectoTokens: List[TectoToken],
            sentiment: Sentiment) -> None:
        self.stdForm = stdForm
        """ Human readable representation of the relation, e.g. `eat-not(SUBJ:John, DOBJ:pizza)`.
            Note: not supported yet. """
        self.name = name
        """ Predicate of the relation, e.g. `eat` for _eat a pizza_ or `good` for _a good pizza_ """
        self.type = relationType
        """ One of Relation.TYPE_ATTR, Relation.TYPE_RELATION, Relation.TYPE_EXTERNAL """
        self.args = args
        """ Arguments of the relation (subject, possibly an object). """
        self.negation = negation
        """ Flag marking negated relation. """
        self.features = features
        """ Any features of the relation e.g. [modality: can] """
        self.tectoTokens = tectoTokens
        """ Tecto-tokens of all the mentions of the relations (restricted to its head). """
        self.sentiment = sentiment
        """ Sentiment of the sentences the relation occurs in. """

    def __repr__(self):
        return ('Relation('
            f'stdForm={self.stdForm!r}, name={self.name!r}, '
            f'type={self.type!r}, args={self.args!r}'
            f'negation={self.negation!r}, features={self.features!r}'
            f'tectoTokens={TokenUtils.toSimpleString(self.tectoTokens, quote=True)}, '
            f'sentiment={self.sentiment!r})')


class Sentence:
    """ A single sentence with its morphological, syntactical, deep-syntactical and sentimental analysis """
    def __init__(self, *,
            charSpan: CharSpan,
            root: Token,
            tokens: List[Token],
            tectoRoot: TectoToken,
            tectoTokens: List[TectoToken],
            sentiment: Sentiment) -> None:
        self.paragraph: 'Paragraph' = None
        """ the paragraph containing this sentence """
        self.charSpan = charSpan
        """ text span within the paragraph """
        self.root = root
        """ Token which is the root of the syntactic structure of the sentence """
        self.tokens = tokens
        """ All tokens of the sentence ordered by word-order """
        self.tectoRoot = tectoRoot
        """ Tecto token which is the root of the tecto structure of the sentence """
        self.tectoTokens = tectoTokens
        """ All tecto tokens of the sentence; TODO are they ordered in any way?? """
        self.sentiment = sentiment
        """ Sentiment of the sentence """

    @property
    def text(self):
        """ text of the sentence (before correction) """
        return self.charSpan.extractText(self.paragraph.text)

    def __repr__(self):
        return ('Sentence('
            f'charSpan={self.charSpan!r}, '
            f'root={self.root.toSimpleString()!r}, '
            f'tokens={TokenUtils.toSimpleString(self.tokens, quote=True)}, '
            f'tectoRoot={self.tectoRoot.toSimpleString()!r}, '
            f'tectoTokens={TokenUtils.toSimpleString(self.tectoTokens, quote=True)}, '
            f'sentiment={self.sentiment!r})')


class Paragraph:
    TYPE_TITLE = 'title'
    """ Type of a paragraph representing a title of the whole document. Also used for email subjects. """
    TYPE_LEAD = 'lead'
    """ Type of a paragraph representing a lead (perex) of the whole document """
    TYPE_TEXT = 'text'
    """ Type of a paragraph containing regular text (for now this is used for the whole body of the document) """
    TYPE_SECTION_HEADING = 'section_heading'
    """ Type of a paragraph representing a section/chapter heading (not used yet) """

    def __init__(self, *,
            paraType: str,
            idx: int,
            text: str,
            sentences: List[Sentence]) -> None:
        self.container: X3 = None
        """ the full analysis object containing this paragraph """
        self.type = paraType
        """ title, section heading, lead, body text, etc. For now, it is simply the segment type: title, lead, body"""
        self.idx = idx
        """ zero-based index of the paragraph within the document """
        self.text = text
        """ text of the paragraph before correction """
        self.sentences = sentences
        """ the sentences within this paragraph """

    @property
    def tokens(self) -> Iterable[Token]:
        """
        Tokens across all sentences.
        """
        for s in self.sentences:
            for t in s.tokens:
                yield t

    @property
    def tectoTokens(self) -> Iterable[TectoToken]:
        """
        Tecto tokens across all sentences.
        """
        for s in self.sentences:
            for t in s.tectoTokens:
                yield t

    def __repr__(self):
        return ('Paragraph('
                f'paraType={self.type!r}, idx={self.idx!r}, '
                f'text={self.text!r}, '
                f'sentence={self.sentences!r})')


class X3:
    def __init__(self, *,
            docId: Optional[str],
            language: Language,
            sentiment: Sentiment,
            paragraphs: List[Paragraph],
            entities: List[Entity],
            tags: List[Tag],
            relations: List[Relation],
            metadata: Mapping[str, Any]) -> None:
        self.docId = docId
        """ Document id """
        self.language = language
        """ Language of the document and analysis. """
        self.sentiment = sentiment
        """ Sentiment of the document. """
        self.paragraphs = paragraphs
        """ The paragraphs within the document. For F2, these are segments. """
        self.entities = entities
        """ The entities in the document. """
        self.tags = tags
        """ The tags of the document. """
        self.relations = relations
        """ The relations in the document. """
        self.metadata = metadata
        """The extra non-NLP type of information related to analysis."""
        # self.debugInfo: str #

    def __repr__(self):
        return ('X3('
                f'docId={self.docId!r}, language={self.language!r}, sentiment={self.sentiment!r}, '
                f'paragraphs={self.paragraphs!r}, entities={self.entities!r}, tags={self.tags!r}, '
                f'relations={self.relations!r}, metadata={self.metadata!r})')

    @property
    def sentences(self) -> Iterable[Sentence]:
        """
        Sentences across all paragraphs.
        """
        for p in self.paragraphs:
            for s in p.sentences:
                yield s

    @property
    def tokens(self) -> Iterable[Token]:
        """
        Tokens across all paragraphs.
        """
        for s in self.sentences:
            for t in s.tokens:
                yield t

    @property
    def tectoTokens(self) -> Iterable[TectoToken]:
        """
        Tecto tokens across all paragraphs.
        """
        for s in self.sentences:
            for t in s.tectoTokens:
                yield t

    def getParaByType(self, paraType: str) -> Optional[Paragraph]:
        """
        Returns a paragraph with the specified type.
        Throws a ValueError if there are more than one, and return None if there are none.
        This is intended for legacy paragraphs corresponding to title/lead/text segments.
        """
        paras = [p for p in self.paragraphs if p.type == paraType]
        if len(paras) > 1:
            raise ValueError(f'Multiple paragraphs with the type {paraType}')
        return paras[0] if paras else None

    def title(self) -> Optional[Paragraph]:
        """
        Returns the title paragraph if present, None if not, and throws a ValueError if there are multiple title paragraphs.
        """
        return self.getParaByType(Paragraph.TYPE_TITLE)

    def lead(self) -> Optional[Paragraph]:
        """
        Returns the lead paragraph if present, None if not, and throws a ValueError if there are multiple title paragraphs.
        """
        return self.getParaByType(Paragraph.TYPE_LEAD)

    def text(self) -> Optional[Paragraph]:
        """
        Returns the text paragraph if present, None if not, and throws a ValueError if there are multiple title paragraphs.
        """
        return self.getParaByType(Paragraph.TYPE_TEXT)

