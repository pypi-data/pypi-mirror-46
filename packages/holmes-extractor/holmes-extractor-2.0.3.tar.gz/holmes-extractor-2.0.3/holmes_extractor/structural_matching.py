import copy
from .errors import *
from .semantics import SemanticDependency

class WordMatch:
    """A match between a searched phrase word and a document word.

    Properties:

    search_phrase_token -- the spaCy token from the search phrase.
    search_phrase_word -- the word that matched from the search phrase.
    document_token -- the spaCy token from the document.
    document_word -- the word that matched from the document.
    type -- *direct*, *entity*, *embedding* or *ontology*.
    similarity_measure -- for type *embedding*, the similarity between the two tokens,
        otherwise 1.0.
    is_negated -- *True* if this word match leads to a match of which it
      is a part being negated.
    is_uncertain -- *True* if this word match leads to a match of which it
      is a part being uncertain.
    structurally_matched_document_token -- the spaCy token from the document that matched
        the parent dependencies, which may be different from *document_token* if coreference
        resolution is active.
    involves_coreference -- *True* if *document_token* and *structurally_matched_document_token*
        are different.
    extracted_word -- within the coreference chain, the most specific term that corresponded to
      document_word in the ontology.
    depth -- the number of hyponym relationships linking *search_phrase_word* and
        *extracted_word*, or *0* if ontology-based matching is not active.
    """

    def __init__(self, search_phrase_token, search_phrase_word, document_token, document_word,
            type, similarity_measure, is_negated, is_uncertain,
            structurally_matched_document_token, extracted_word, depth):

        self.search_phrase_token = search_phrase_token
        self.search_phrase_word = search_phrase_word
        self.document_token = document_token
        self.document_word = document_word
        self.type = type
        self.similarity_measure = similarity_measure
        self.is_negated = is_negated
        self.is_uncertain = is_uncertain
        self.structurally_matched_document_token = structurally_matched_document_token
        self.extracted_word = extracted_word
        self.depth = depth

    @property
    def involves_coreference(self):
        return self.document_token != self.structurally_matched_document_token

class Match:
    """A match between a search phrase and a document.

    Properties:

    word_matches -- a list of *WordMatch* objects.
    is_negated -- *True* if this match is negated.
    is_uncertain -- *True* if this match is uncertain.
    involves_coreference -- *True* if this match was found using coreference resolution.
    search_phrase_label -- the label of the search phrase that matched.
    document_label -- the label of the document that matched.
    from_single_word_phraselet -- *True* if this is a match against a single-word
        phraselet.
    overall_similarity_measure -- the overall similarity of the match, or *1.0* if the embedding
        strategy was not involved in the match.
    index_within_document -- the index of the document token that matched the search phrase
        root token.
    """

    def __init__(self, search_phrase_label, document_label, from_single_word_phraselet):
        self.word_matches = []
        self.is_negated = False
        self.is_uncertain = False
        self.search_phrase_label = search_phrase_label
        self.document_label = document_label
        self.from_single_word_phraselet = from_single_word_phraselet
        self.index_within_document = None

    @property
    def involves_coreference(self):
        for word_match in self.word_matches:
            if word_match.involves_coreference:
                return True
        return False

    def __copy__(self):
        match_to_return = Match(self.search_phrase_label, self.document_label,
                self.from_single_word_phraselet)
        match_to_return.word_matches = self.word_matches.copy()
        match_to_return.is_negated = self.is_negated
        match_to_return.is_uncertain = self.is_uncertain
        match_to_return.index_within_document = self.index_within_document
        return match_to_return

class SerializedPhraselet:
    """A serialized topic matching phraselet.

        Parameters:

        label -- the phraselet label.
        template_label -- the value of 'PhraseletTemplate.label'.
        parent_word -- the parent word, or the word for single-word phraselets.
        child_word -- the child word, or 'None' for single-word phraselets.
    """

    def __init__(self, label, template_label, parent_word, child_word):
        self.label = label
        self.template_label = template_label
        self.parent_word = parent_word
        self.child_word = child_word

    def __eq__(self, other):
        return type(other) == SerializedPhraselet and \
                self.template_label == other.template_label and \
                self.parent_word == other.parent_word and \
                self.child_word == other.child_word

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.template_label, self.parent_word, self.child_word))


class StructuralMatcher:
    """The class responsible for matching search phrases with documents."""

    def __init__(self, semantic_analyzer, ontology, overall_similarity_threshold,
            embedding_based_matching_on_root_words, perform_coreference_resolution,
            output_document_matching_message_to_console=False):
        """Args:

        semantic_analyzer -- the *SemanticAnalyzer* object to use in generating search phrase
            representations
        ontology -- optionally, an *Ontology* object to use in matching
        overall_similarity_threshold -- if embedding-based matching is to be activated, a float
            value between 0 and 1. A match between a search phrase and a document is then valid
            if the geometric mean of all the similarities between search phrase tokens and
            document tokens is this value or greater. If this value is set to 1.0,
            embedding-based matching is deactivated.
        embedding_based_matching_on_root_words -- determines whether or not embedding-based
            matching should be attempted on search-phrase root tokens, which has a considerable
            performance hit. Defaults to *False*.
        perform_coreference_resolution -- *True*, if coreference resolution should be performed.
        output_document_matching_message_to_console -- *True* if a status message should be written
            to the console when a document is matched.
        """
        self.semantic_analyzer = semantic_analyzer
        self.ontology = ontology
        self.overall_similarity_threshold = overall_similarity_threshold
        self.embedding_based_matching_on_root_words = embedding_based_matching_on_root_words
        self.search_phrase_labels = set()
        self.search_phrases = []
        # Dict from document labels to *_RegisteredDocument* objects
        self._registered_documents = {}
        self.perform_coreference_resolution = perform_coreference_resolution
        self.output_document_matching_message_to_console = \
                output_document_matching_message_to_console

    class _SearchPhrase:

        def __init__(self, doc, matchable_tokens, root_token,
                matchable_non_entity_tokens_to_lexemes, single_token_similarity_threshold, label,
                ontology, topic_match_phraselet):
            """Args:

            doc -- the Holmes document created for the search phrase
            matchable_tokens -- a list of tokens all of which must have counterparts in the
                document to produce a match
            root_token -- the token at which recursive matching starts
            matchable_non_entity_tokens_to_lexemes -- dictionary from token indexes to *Lexeme*
                objects. Only used when embedding matching is active.
            single_token_similarity_threshold -- the lowest similarity value that a single token
                within this search phrase could have with a matching document token to achieve
                the overall matching threshold for a match.
            label -- a label for the search phrase.
            ontology -- a reference to the ontology held by the outer *StructuralMatcher* object.
            topic_match_phraselet -- 'True' if a topic match phraselet, otherwise 'False'.
            """
            self.doc = doc
            self.matchable_tokens = matchable_tokens
            self.root_token = root_token
            self.matchable_non_entity_tokens_to_lexemes = matchable_non_entity_tokens_to_lexemes
            self.single_token_similarity_threshold = single_token_similarity_threshold
            self.label = label
            self.ontology = ontology
            self.topic_match_phraselet = topic_match_phraselet

    class _RegisteredDocument:
        """Args:

        doc -- the Holmes document
        words_to_token_indexes_dict -- a dictionary from words to the token indexes
            where each word occurs in the document
        """

        def __init__(self, doc, words_to_token_indexes_dict):
            self.doc = doc
            self.words_to_token_indexes_dict = words_to_token_indexes_dict

    class _MultiwordSpan:

        def __init__(self, text, lemma, tokens):
            """Args:

            text -- the raw text representation of the multiword span
            lemma - the lemma representation of the multiword span
            tokens -- a list of tokens that make up the multiword span
            """
            self.text = text
            self.lemma = lemma
            self.tokens = tokens

    def _words_matching_root_token(self, search_phrase):
        """ Generator over all words that match the root token of the search phrase,
            taking any ontology into account.
        """
        yield search_phrase.root_token._.holmes.lemma
        if not search_phrase.topic_match_phraselet:
            yield search_phrase.root_token.text.lower()
        if self.ontology != None and not \
                self._is_entity_search_phrase_token(search_phrase.root_token,
                        search_phrase.topic_match_phraselet):
            ontology_matching_strings = set()
            ontology_matching_strings.update(self.ontology.get_words_matching_lower_case(
                    search_phrase.root_token._.holmes.lemma))
            if not search_phrase.topic_match_phraselet:
                ontology_matching_strings.update(self.ontology.get_words_matching_lower_case(
                        search_phrase.root_token.text.lower()))
            for working_word in ontology_matching_strings:
                yield working_word

    def _multiword_spans_with_head_token(self, token):
        """Generator over *_MultwordSpan* objects with *token* at their head. Dependent phrases
            are only returned for nouns at present because e.g. for verbs the whole sentence
            would be returned.
        """

        if not token.pos_ in self.semantic_analyzer.noun_pos:
            return
        pointer = token.left_edge.i
        while pointer <= token.right_edge.i:
            if token.doc[pointer].pos_ in self.semantic_analyzer.noun_pos \
                    and token.doc[pointer].dep_ in self.semantic_analyzer.noun_kernel_dep:
                working_text = ''
                working_lemma = ''
                working_tokens = []
                inner_pointer = pointer
                while inner_pointer <= token.right_edge.i and \
                        token.doc[inner_pointer].pos_ in self.semantic_analyzer.noun_pos:
                    working_text = ' '.join((working_text, token.doc[inner_pointer].text))
                    working_lemma = ' '.join((working_lemma,
                            token.doc[inner_pointer]._.holmes.lemma))
                    working_tokens.append(token.doc[inner_pointer])
                    inner_pointer += 1
                if pointer + 1 < inner_pointer:
                    yield self._MultiwordSpan(working_text.strip(), working_lemma.strip(),
                            working_tokens)
            pointer += 1

    def remove_all_search_phrases(self):
        self.search_phrases = []
        self.search_phrase_labels = set()

    def remove_all_search_phrases_with_label(self, label):
        self.search_phrases = [search_phrase for search_phrase in self.search_phrases if
                search_phrase.label != label]
        if label in self.search_phrase_labels:
            self.search_phrase_labels.remove(label)

    def register_search_phrase(self, search_phrase_text, label, topic_match_phraselet=False):
        search_phrase_doc = self.semantic_analyzer.parse(search_phrase_text)
        self._internal_register_search_phrase(search_phrase_text, search_phrase_doc, label,
                topic_match_phraselet)

    def register_phraselet_doc(self, phraselet_doc, label):
        if label not in self.search_phrase_labels:
            self._internal_register_search_phrase('topic match phraselet', phraselet_doc, label,
                    True)

    def register_phraselets(self, doc, *, replace_with_hypernym_ancestors,
            match_all_words, returning_serialized_phraselets):
        """ Generates and registers topic matching phraselets extracted from a matching text.

        Properties:

        doc -- the Holmes-parsed document
        replace_with_hypernym_ancestors -- if 'True', all words present in the ontology
            are replaced with their most general (highest) ancestors.
        match_all_words -- if 'True', word phraselets are generated for all matchable words
            rather than just for words whose tags match the phraselet template.
        """

        def get_word_from_token(token):
            if token.text[:6] == 'ENTITY':
                return token.text
                # keep the text, because the lemma will be lowercase
            word = token._.holmes.lemma
            # the normal situation
            if self.ontology != None and not self.ontology.contains(word) and \
                    self.ontology.contains(token.text.lower()):
                word = token.text.lower()
                # ontology contains text but not lemma, so stick to text
            return word

        def process_single_word_phraselet_templates(token, checking_tags):
            for phraselet_template in (phraselet_template for phraselet_template in
                    self.semantic_analyzer.phraselet_templates if
                    phraselet_template.single_word() and token._.holmes.is_matchable):
                if not checking_tags or token.tag_ in phraselet_template.parent_tags:
                    phraselet_doc = self.semantic_analyzer.parse(
                        phraselet_template.template_sentence)
                    word = get_word_from_token(token)
                    if self.ontology != None and replace_with_hypernym_ancestors:
                        word = self.ontology.get_most_general_hypernym_ancestor(word)
                    phraselet_doc[phraselet_template.parent_index]._.holmes.lemma = word
                    phraselet_label = ''.join((phraselet_template.label, ': ', word))
                    if word not in self.semantic_analyzer.phraselet_stop_lemmas and word != \
                            'ENTITYNOUN':
                            # ENTITYNOUN has to be excluded as single word although it is still
                            # permitted as the child of a relation phraselet template
                        self.register_phraselet_doc(phraselet_doc, phraselet_label)
                        if returning_serialized_phraselets:
                            serialized_phraselets.append(SerializedPhraselet(
                                    phraselet_label, phraselet_template.label, word, None))

        if returning_serialized_phraselets:
            serialized_phraselets = []
        self._redefine_multiwords_on_head_tokens(doc)
        for token in doc:
            if match_all_words:
                process_single_word_phraselet_templates(token, False)
                continue
            if self.perform_coreference_resolution:
                parents = self.semantic_analyzer.token_and_coreference_chain_indexes(token)
            else:
                parents = [token.i]
            for parent in parents:
                for dependency in doc[parent]._.holmes.children:
                    if self.perform_coreference_resolution:
                        children = self.semantic_analyzer.token_and_coreference_chain_indexes(
                                dependency.child_token(doc))
                    else:
                        children = [dependency.child_token(doc).i]
                    for child in children:
                        for phraselet_template in (phraselet_template for phraselet_template in
                                self.semantic_analyzer.phraselet_templates if not
                                phraselet_template.single_word()):
                            if dependency.label in \
                                    phraselet_template.reverse_matching_dependency_labels and \
                                    doc[parent].tag_ in phraselet_template.parent_tags and \
                                    doc[child].tag_ in phraselet_template.child_tags and \
                                    doc[parent]._.holmes.is_matchable and \
                                    doc[child]._.holmes.is_matchable:
                                phraselet_doc = self.semantic_analyzer.parse(
                                        phraselet_template.template_sentence)
                                parent_word = get_word_from_token(doc[parent])
                                if self.ontology != None and replace_with_hypernym_ancestors:
                                    parent_word = \
                                            self.ontology.get_most_general_hypernym_ancestor(
                                            parent_word)
                                child_word = get_word_from_token(doc[child])
                                if self.ontology != None and replace_with_hypernym_ancestors:
                                    child_word = \
                                            self.ontology.get_most_general_hypernym_ancestor(
                                            child_word)
                                phraselet_doc[phraselet_template.parent_index]._.holmes.lemma = \
                                        parent_word
                                phraselet_doc[phraselet_template.child_index]._.holmes.lemma = \
                                        child_word
                                phraselet_label = ''.join((phraselet_template.label, ': ',
                                        parent_word, '-', child_word))
                                if parent_word not in \
                                        self.semantic_analyzer.phraselet_stop_lemmas and \
                                        child_word not in \
                                        self.semantic_analyzer.phraselet_stop_lemmas:
                                    self.register_phraselet_doc(phraselet_doc, phraselet_label)
                                    if returning_serialized_phraselets:
                                        serialized_phraselets.append(SerializedPhraselet(
                                                phraselet_label, phraselet_template.label,
                                                parent_word, child_word))
            process_single_word_phraselet_templates(token, True)
        if len(self.list_search_phrase_labels()) == 0 and not match_all_words:
            for token in doc:
                process_single_word_phraselet_templates(token, False)
        if returning_serialized_phraselets:
            return serialized_phraselets

    def register_serialized_phraselets(self, serialized_phraselets):
        """ Re-registers serialized topic matching phraselets. """

        def register_serialized_phraselet(serialized_phraselet):
            for phraselet_template in self.semantic_analyzer.phraselet_templates:
                if serialized_phraselet.template_label == phraselet_template.label:
                    phraselet_doc = self.semantic_analyzer.parse(
                            phraselet_template.template_sentence)
                    phraselet_doc[phraselet_template.parent_index]._.holmes.lemma = \
                            serialized_phraselet.parent_word
                    if serialized_phraselet.child_word != None:
                        phraselet_doc[phraselet_template.child_index]._.holmes.lemma = \
                                serialized_phraselet.child_word
                        phraselet_label = ''.join((phraselet_template.label, ': ',
                                serialized_phraselet.parent_word, '-',
                                serialized_phraselet.child_word))
                    else:
                        phraselet_label = ''.join((phraselet_template.label, ': ',
                                serialized_phraselet.parent_word))
                    self.register_phraselet_doc(phraselet_doc, phraselet_label)
                    return
            raise RuntimeError(' '.join(('Phraselet template', serialized_phraselet.template_label,
                    'not found.')))

        for serialized_phraselet in serialized_phraselets:
            register_serialized_phraselet(serialized_phraselet)

    def _redefine_multiwords_on_head_tokens(self, doc):
        if self.ontology != None:
            for token in doc:
                for multiword_span in self._multiword_spans_with_head_token(token):
                    if self.ontology.contains_multiword(multiword_span.lemma) or \
                            self.ontology.contains_multiword(multiword_span.text):
                        if self.ontology.contains_multiword(multiword_span.lemma):
                            token._.holmes.lemma = multiword_span.lemma
                        else:
                            token._.holmes.lemma = multiword_span.text
                        # mark the dependent tokens as grammatical and non-matchable
                        for multiword_token in (
                                multiword_token for multiword_token in multiword_span.tokens
                                if multiword_token.i != token.i):
                            multiword_token._.holmes.children = [SemanticDependency(
                                    multiword_token.i, 0 - (token.i + 1), None)]
                            multiword_token._.holmes.is_matchable = False

    def _internal_register_search_phrase(self, search_phrase_text, search_phrase_doc,
            label, topic_match_phraselet):

        def replace_grammatical_root_token_recursively(token):
            """Where the syntactic root of a search phrase document is a grammatical token or is
                marked as non-matchable, loop through the semantic dependencies to find the
                semantic root.
            """
            for dependency in token._.holmes.children:
                if dependency.child_index < 0:
                    return replace_grammatical_root_token_recursively(
                            token.doc[(0 - dependency.child_index) - 1])
            if not token._.holmes.is_matchable:
                for dependency in token._.holmes.children:
                    if dependency.child_index >= 0 and \
                            dependency.child_token(token.doc)._.holmes.is_matchable:
                        return replace_grammatical_root_token_recursively(
                                token.doc[dependency.child_index])
            return token

        if not topic_match_phraselet:
            self._redefine_multiwords_on_head_tokens(search_phrase_doc)
            # where a multiword exists as an ontology entry, the multiword should be used for
            # matching rather than the individual words. Not relevant for topic matching
            # phraselets because the multiword will already have been set as the Holmes
            # lemma of the word.

        for token in search_phrase_doc:
            if len(token._.holmes.righthand_siblings) > 0:
                # SearchPhrases may not themselves contain conjunctions like 'and'
                # because then the matching becomes too complicated
                raise SearchPhraseContainsConjunctionError(search_phrase_text)
            if token._.holmes.is_negated:
                # SearchPhrases may not themselves contain negation
                # because then the matching becomes too complicated
                raise SearchPhraseContainsNegationError(search_phrase_text)
            if self.perform_coreference_resolution and token.pos_ == 'PRON' and \
                    self.semantic_analyzer.is_involved_in_coreference(token):
                # SearchPhrases may not themselves contain coreferring pronouns
                # because then the matching becomes too complicated
                raise SearchPhraseContainsCoreferringPronounError(search_phrase_text)

        root_tokens = []
        tokens_to_match = []
        matchable_non_entity_tokens_to_lexemes = {}
        for token in search_phrase_doc:
            # check whether grammatical token
            if token._.holmes.is_matchable and not (len(token._.holmes.children) > 0 and
                    token._.holmes.children[0].child_index < 0):
                tokens_to_match.append(token)
                if self.ontology != None:
                    self.ontology.add_to_dictionary(token._.holmes.lemma)
                    if not topic_match_phraselet:
                        self.ontology.add_to_dictionary(token.text)
                if self.overall_similarity_threshold < 1.0 and not \
                        self._is_entity_search_phrase_token(token, topic_match_phraselet):
                    if not topic_match_phraselet:
                        matchable_non_entity_tokens_to_lexemes[token.i] = \
                                self.semantic_analyzer.nlp.vocab[token.lemma_]
                    else:
                        matchable_non_entity_tokens_to_lexemes[token.i] = \
                                self.semantic_analyzer.nlp.vocab[token._.holmes.lemma]
            if token.dep_ == 'ROOT': # syntactic root
                root_tokens.append(replace_grammatical_root_token_recursively(token))
        if len(tokens_to_match) == 0:
            raise SearchPhraseWithoutMatchableWordsError(search_phrase_text)
        if len(root_tokens) > 1:
            raise SearchPhraseContainsMultipleClausesError(search_phrase_text)
        single_token_similarity_threshold = 1.0
        if self.overall_similarity_threshold < 1.0 and \
                len(matchable_non_entity_tokens_to_lexemes) > 0:
            single_token_similarity_threshold = \
                    self.overall_similarity_threshold ** len(matchable_non_entity_tokens_to_lexemes)
        if len(root_tokens) == 1:
            self.search_phrases.append(self._SearchPhrase(search_phrase_doc, tokens_to_match,
                    root_tokens[0], matchable_non_entity_tokens_to_lexemes,
                    single_token_similarity_threshold, label, self.ontology,
                    topic_match_phraselet))
            self.search_phrase_labels.add(label)

    def list_search_phrase_labels(self):
        return sorted(self.search_phrase_labels)

    def register_document(self, parsed_document, label):

        def add_dict_entry(dict, word, token_index):
            if word in dict.keys():
                if token_index not in dict[word]:
                    dict[word].append(token_index)
            else:
                dict[word] = [token_index]

        def get_multiword(token):
            for multiword_span in self._multiword_spans_with_head_token(token):
                if self.ontology.contains_multiword(multiword_span.text):
                    return multiword_span.text.lower()
            return None

        if label in self._registered_documents.keys():
            raise DuplicateDocumentError(label)
        words_to_token_indexes_dict = {}
        for token in parsed_document:
            if self.ontology != None:
                multiword = get_multiword(token)
                if multiword != None:
                    add_dict_entry(words_to_token_indexes_dict, multiword, token.i)
                    continue
            add_dict_entry(words_to_token_indexes_dict, token._.holmes.lemma, token.i)
            add_dict_entry(words_to_token_indexes_dict, token.text.lower(), token.i)

            # parent check is necessary so we only find multiword entities once per
            # search phrase. sibling_marker_deps applies to siblings which would
            # otherwise be excluded because the main sibling would normally also match the
            # entity root word.
            if len(token.ent_type_) > 0 and (token.dep_ == 'ROOT' or
                    token.dep_ in self.semantic_analyzer.sibling_marker_deps
                    or token.ent_type_ != token.head.ent_type_):
                entity_label = ''.join(('ENTITY', token.ent_type_))
                add_dict_entry(words_to_token_indexes_dict, entity_label, token.i)
        self._registered_documents[label] = self._RegisteredDocument(parsed_document,
                words_to_token_indexes_dict)

    def remove_document(self, label):
        self._registered_documents.pop(label)

    def remove_all_documents(self):
        self._registered_documents = {}

    def document_labels(self):
        """Returns a list of the labels of the currently registered documents."""
        return self._registered_documents.keys()

    def get_document(self, label):
        if label in self._registered_documents.keys():
            return self._registered_documents[label].doc
        else:
            return None

    def _match_recursively(self, *, search_phrase, search_phrase_token, document, document_token,
        search_phrase_tokens_to_word_matches, search_phrase_and_document_visited_table,
        is_uncertain, structurally_matched_document_token):
        """Called whenever matching is attempted between a search phrase token and a document
            token."""

        def handle_match(search_phrase_word, document_word, match_type, depth,
                similarity_measure=1.0):
            """Most of the variables are set from the outer call.

            Args:

            search_phrase_word -- the textual representation of the search phrase word that matched.
            document_word -- the textual representation of the document word that matched.
            match_type -- *direct*, *entity*, *embedding* or *ontology*
            similarity_measure -- the similarity between the two tokens. Defaults to 1.0 if the
                match did not involve embeddings.
            """
            for dependency in (dependency for
                    dependency in search_phrase_token._.holmes.children
                    if dependency.child_token(search_phrase_token.doc)._.holmes.is_matchable):
                at_least_one_document_dependency_tried = False
                at_least_one_document_dependency_matched = False
                # Loop through this token and any tokens linked to it by coreference
                if self.perform_coreference_resolution:
                    parents = self.semantic_analyzer.token_and_coreference_chain_indexes(
                            document_token)
                else:
                    parents = [document_token.i]
                for working_document_parent_index in parents:
                    working_document_parent = document_token.doc[working_document_parent_index]
                    # Loop through the dependencies from each token
                    for document_dependency in (document_dependency for
                            document_dependency in working_document_parent._.holmes.children
                            if self.semantic_analyzer.dependency_labels_match(
                            search_phrase_dependency_label= dependency.label,
                            document_dependency_label = document_dependency.label)):
                        document_child = document_dependency.child_token(document_token.doc)
                        # wherever a dependency is found, loop through any tokens linked
                        # to the child by coreference
                        if self.perform_coreference_resolution:
                            children = self.semantic_analyzer.token_and_coreference_chain_indexes(
                                    document_child)
                        else:
                            children = [document_child.i]
                        for document_dependency_child_index in (working_index for working_index in
                                children if working_index not in
                                search_phrase_and_document_visited_table[dependency.child_index]):
                            at_least_one_document_dependency_tried = True
                            if self._match_recursively(
                                    search_phrase=search_phrase,
                                    search_phrase_token=dependency.child_token(
                                            search_phrase_token.doc),
                                    document=document,
                                    document_token=document_token.doc[
                                            document_dependency_child_index],
                                    search_phrase_tokens_to_word_matches=
                                            search_phrase_tokens_to_word_matches,
                                    search_phrase_and_document_visited_table=
                                            search_phrase_and_document_visited_table,
                                    is_uncertain=(document_dependency.is_uncertain and not
                                            dependency.is_uncertain),
                                    structurally_matched_document_token=document_child):
                                at_least_one_document_dependency_matched = True
                if at_least_one_document_dependency_tried and not \
                        at_least_one_document_dependency_matched:
                    return
            # store this search sentence token as matching the search_phrase token
            search_phrase_tokens_to_word_matches[search_phrase_token.i].append(WordMatch(
                    search_phrase_token, search_phrase_word, document_token,
                    document_word, match_type, similarity_measure, is_negated, is_uncertain,
                    structurally_matched_document_token, document_word, depth))

        search_phrase_and_document_visited_table[search_phrase_token.i].add(document_token.i)
        is_negated = document_token._.holmes.is_negated
        if document_token._.holmes.is_uncertain:
            is_uncertain = True

        search_phrase_word_text = search_phrase_token.text.lower()
        search_phrase_word_lemma = search_phrase_token._.holmes.lemma
        document_word_text = document_token.text.lower()
        document_word_lemma = document_token._.holmes.lemma

        if self._is_entity_search_phrase_token(search_phrase_token,
                search_phrase.topic_match_phraselet):
            if self._entity_search_phrase_token_matches(search_phrase_token,
                    search_phrase.topic_match_phraselet, document_token):
                for multiword_span in self._multiword_spans_with_head_token(document_token):
                    for working_token in multiword_span.tokens:
                        if not self._entity_search_phrase_token_matches(
                                search_phrase_token, search_phrase.topic_match_phraselet,
                                document_token):
                            continue
                    for working_token in multiword_span.tokens:
                        search_phrase_and_document_visited_table[search_phrase_token.i].add(
                                working_token.i)
                    handle_match(search_phrase_token.text, multiword_span.text, 'entity', 0)
                    return True
                search_phrase_and_document_visited_table[search_phrase_token.i].add(
                        document_token.i)
                handle_match(search_phrase_token.text, document_token.text, 'entity', 0)
                return True
            return False

        if search_phrase_word_lemma == document_word_text:
            handle_match(search_phrase_word_lemma, document_word_text, 'direct', 0)
            return True
        if search_phrase_word_lemma == document_word_lemma:
            handle_match(search_phrase_word_lemma, document_word_lemma, 'direct', 0)
            return True
        if self.ontology != None:
            entry = self.ontology.matches(search_phrase_word_lemma, document_word_text)
            if entry != None:
                handle_match(search_phrase_word_lemma, entry.word, 'ontology',
                        entry.depth)
                return True
            entry = self.ontology.matches(search_phrase_word_lemma, document_word_lemma)
            if entry != None:
                handle_match(search_phrase_word_lemma, entry.word, 'ontology',
                        entry.depth)
                return True

        if not search_phrase.topic_match_phraselet and \
                search_phrase_token._.holmes.lemma == search_phrase_token.lemma_:
            # search_phrase word is not multiword, phrasal or separable verb
            if len(search_phrase_word_lemma.split()) == 1:
                if search_phrase_word_text == document_word_text:
                    handle_match(search_phrase_token.text, document_token.text, 'direct', 0)
                    return True
                if search_phrase_word_text == document_word_lemma:
                    handle_match(search_phrase_token.text, document_word_lemma, 'direct', 0)
                    return True
            if self.ontology != None:
                entry = self.ontology.matches(search_phrase_word_text, document_word_text)
                if entry != None:
                    handle_match(search_phrase_token.text, entry.word, 'ontology',
                            entry.depth)
                    return True
                entry = self.ontology.matches(search_phrase_word_text, document_word_lemma)
                if entry != None:
                    handle_match(search_phrase_token.text, entry.word, 'ontology',
                            entry.depth)
                    return True

        # multiword matches
        if self.ontology != None:
            for multiword_span in self._multiword_spans_with_head_token(document_token):
                if search_phrase_word_lemma == multiword_span.text.lower():
                    for working_token in multiword_span.tokens:
                        search_phrase_and_document_visited_table[search_phrase_token.i].add(
                                working_token.i)
                        handle_match(search_phrase_word_lemma, multiword_span.text, 'ontology',
                                0)
                        return True
                entry = self.ontology.matches(search_phrase_word_lemma, multiword_span.text.lower())
                if entry != None:
                    for working_token in multiword_span.tokens:
                        search_phrase_and_document_visited_table[search_phrase_token.i].add(
                                working_token.i)
                    handle_match(search_phrase_word_lemma, entry.word, 'ontology',
                            entry.depth)
                    return True
                if not search_phrase.topic_match_phraselet:
                    entry = self.ontology.matches(search_phrase_word_text,
                            multiword_span.text.lower())
                    if entry != None:
                        for working_token in multiword_span.tokens:
                            search_phrase_and_document_visited_table[search_phrase_token.i].add(
                                    working_token.i)
                        handle_match(search_phrase_token.text, entry.word, 'ontology',
                                entry.depth)
                        return True

        if search_phrase_token.i in search_phrase.matchable_non_entity_tokens_to_lexemes.keys():
            similarity_measure = search_phrase.matchable_non_entity_tokens_to_lexemes[
                    search_phrase_token.i].similarity(document_token)
            if similarity_measure > search_phrase.single_token_similarity_threshold:
                if not search_phrase.topic_match_phraselet:
                    search_phrase_word_to_use = search_phrase_token.lemma_
                else:
                    search_phrase_word_to_use = search_phrase_token._.holmes.lemma
                handle_match(search_phrase_word_to_use, document_token.lemma_, 'embedding', 0,
                        similarity_measure = similarity_measure)
                return True
        return False

    def _is_entity_search_phrase_token(self, search_phrase_token, topic_match_phraselet):
        if topic_match_phraselet:
            word_to_check = search_phrase_token._.holmes.lemma
        else:
            word_to_check = search_phrase_token.text
        return word_to_check[:6] == 'ENTITY'

    def _is_entitynoun_search_phrase_token(self, search_phrase_token, topic_match_phraselet):
        if topic_match_phraselet:
            word_to_check = search_phrase_token._.holmes.lemma
        else:
            word_to_check = search_phrase_token.text
        return word_to_check == 'ENTITYNOUN'

    def _entity_search_phrase_token_matches(self, search_phrase_token, topic_match_phraselet,
            document_token):
        if topic_match_phraselet:
            word_to_check = search_phrase_token._.holmes.lemma
        else:
            word_to_check = search_phrase_token.text
        return (document_token.ent_type_ == word_to_check[6:] and
                len(document_token._.holmes.lemma.strip()) > 0) or \
                (word_to_check == 'ENTITYNOUN' and
                document_token.pos_ in self.semantic_analyzer.noun_pos)
                # len(document_token._.holmes.lemma.strip()) > 0: in German spaCy sometimes
                # classifies whitespace as entities.

    def _build_matches(self, *, search_phrase, document, search_phrase_tokens_to_word_matches,
            document_label):
        """Investigate possible matches when recursion is complete."""

        def get_mention_index_within_coref_cluster(cluster, token):
            """Get the index of the mention within *cluster* in which *token* occurs."""
            counter = -1
            for mention in cluster.mentions:
                counter += 1
                if token.i >= mention.start and token.i <= mention.end:
                    return counter
            return counter

        def filter_word_matches_based_on_coreference_resolution(word_matches):
            """ When coreference resolution is active, additional matches are sometimes
                returned that are filtered out again using this method.
            """
            dict = {}
            # Find the structurally matching document tokens for this list of word matches
            for word_match in word_matches:
                structurally_matched_document_token_index = \
                    word_match.structurally_matched_document_token.i
                if structurally_matched_document_token_index in dict.keys():
                    dict[structurally_matched_document_token_index].append(word_match)
                else:
                    dict[structurally_matched_document_token_index] = [word_match]
            new_word_matches = []
            for structurally_matched_document_token_index in dict.keys():
                # For each structural token, find the best matching coreference mention
                relevant_word_matches = dict[structurally_matched_document_token_index]
                structurally_matched_document_token = \
                        relevant_word_matches[0].document_token.doc[
                        structurally_matched_document_token_index]
                already_added_document_token_indexes = set()
                if structurally_matched_document_token._.in_coref:
                    # There can potentially be multiple clusters.
                    for cluster in structurally_matched_document_token._.coref_clusters:
                        structural_index = get_mention_index_within_coref_cluster(
                            cluster, structurally_matched_document_token)
                        working_index = -1
                        for relevant_word_match in relevant_word_matches:
                            this_index = get_mention_index_within_coref_cluster(
                                    cluster, relevant_word_match.document_token)
                            # The best mention should be as close to the structural
                            # index as possible and preferably not after it.
                            if working_index == -1 or\
                                    (working_index > structural_index and
                                    this_index <= structural_index) or\
                                    (working_index > structural_index and
                                    this_index > structural_index and
                                    this_index < working_index) or\
                                    (abs(structural_index - this_index) <
                                    abs(structural_index - working_index)):
                                working_index = this_index
                        # Filter out any matches from mentions other than the best mention
                        for relevant_word_match in relevant_word_matches:
                            if get_mention_index_within_coref_cluster(
                                    cluster, relevant_word_match.document_token) == working_index \
                                    and relevant_word_match.document_token.i not in \
                                    already_added_document_token_indexes:
                                        already_added_document_token_indexes.add(
                                                relevant_word_match.document_token.i)
                                        new_word_matches.append(relevant_word_match)
                else:
                    new_word_matches.extend(relevant_word_matches)
            return new_word_matches

        def revise_extracted_words_based_on_coreference_resolution(word_matches):
            """ When coreference resolution and ontology-based matching are both active,
                there may be a more specific piece of information elsewhere in the coreference
                chain of a token that has been matched, in which case this piece of information
                should be recorded in *word_match.extracted_word*.
            """
            for word_match in (word_match for word_match in word_matches if word_match.type
                    in ('direct', 'ontology')):
                working_entries = []
                # First loop through getting ontology entries for all mentions in the cluster
                for cluster in word_match.document_token._.coref_clusters:
                    for mention in cluster.mentions:
                        mention_root_token = mention.root
                        working_entries.append(
                                self.ontology.matches(
                                word_match.search_phrase_token._.holmes.lemma,
                                mention_root_token._.holmes.lemma))
                        working_entries.append(
                                self.ontology.matches(
                                word_match.search_phrase_token._.holmes.lemma,
                                mention_root_token.text.lower()))
                        working_entries.append(
                                self.ontology.matches(
                                word_match.search_phrase_token.text.lower(),
                                mention_root_token._.holmes.lemma))
                        working_entries.append(
                                self.ontology.matches(
                                word_match.search_phrase_token.text.lower(),
                                mention_root_token.text.lower()))
                        for multiword_span in self._multiword_spans_with_head_token(
                                mention_root_token):
                            working_entries.append(
                                    self.ontology.matches(
                                    word_match.search_phrase_token.text.lower(),
                                    multiword_span.text))
                            working_entries.append(
                                    self.ontology.matches(
                                    word_match.search_phrase_token._.holmes.lemma,
                                    multiword_span.lemma))
                            working_entries.append(
                                    self.ontology.matches(
                                    word_match.search_phrase_token.text.lower(),
                                    multiword_span.text))
                            working_entries.append(
                                    self.ontology.matches(
                                    word_match.search_phrase_token._.holmes.lemma,
                                    multiword_span.lemma))
                # Now loop through the ontology entries to see if any are more specific than
                # the current value of *extracted_word*.
                for working_entry in working_entries:
                    if working_entry == None:
                        continue
                    if working_entry.is_individual:
                        word_match.extracted_word = working_entry.word
                        break
                    elif working_entry.depth > word_match.depth:
                        word_match.extracted_word = working_entry.word
            return word_matches

        def match_already_contains_structurally_matched_document_token(match, document_token):
            """Ensure that the same document token does not match multiple search phrase tokens."""
            for word_match in match.word_matches:
                if document_token.i == word_match.structurally_matched_document_token.i:
                    return True
            return False

        def check_match_is_coherent_recursively(this_document_token,
                not_yet_traversed_document_token_indexes, traversed_token_indexes):
            """Ensure that the document tokens within a match form a coherent structure linked
                by semantic dependencies. In some rare situations involving embeddings, matches
                can be returned from the recursive matching logic where this is not the case.
            """
            if self.perform_coreference_resolution:
                parents = self.semantic_analyzer.token_and_coreference_chain_indexes(
                        this_document_token)
            else:
                parents = [this_document_token.i]
            for parent_document_index in (parent_index for parent_index in
                    parents if parent_index not in traversed_token_indexes):
                parent_document_token = this_document_token.doc[parent_document_index]
                if parent_document_token.i in not_yet_traversed_document_token_indexes:
                    not_yet_traversed_document_token_indexes.remove(
                        parent_document_token.i)
                traversed_token_indexes.append(parent_document_token.i)
                for dependency in parent_document_token._.holmes.children:
                    child_document_token = dependency.child_token(parent_document_token.doc)
                    if self.perform_coreference_resolution:
                        children = self.semantic_analyzer.token_and_coreference_chain_indexes(
                                child_document_token)
                    else:
                        children = [child_document_token.i]
                    for child_document_index in (child_index for child_index in
                            children if child_index in not_yet_traversed_document_token_indexes
                            and child_index not in traversed_token_indexes):
                        child_document_token = this_document_token.doc[
                                child_document_index]
                        check_match_is_coherent_recursively(child_document_token,
                                not_yet_traversed_document_token_indexes,
                                traversed_token_indexes)

        matches = [Match(search_phrase.label, document_label,
                search_phrase.topic_match_phraselet and len(search_phrase.doc) == 1)]
        for search_phrase_token in search_phrase.matchable_tokens:
            word_matches = search_phrase_tokens_to_word_matches[search_phrase_token.i]
            if len(word_matches) == 0:
                # if there is any search phrase token without a matching document token,
                # we have no match and can return
                return []
            if self.perform_coreference_resolution and \
                    word_matches[0].document_token.doc._.has_coref:
                word_matches = filter_word_matches_based_on_coreference_resolution(word_matches)
                if self.ontology != None:
                    word_matches = revise_extracted_words_based_on_coreference_resolution(
                            word_matches)
            # handle any conjunction by distributing the matches amongst separate match objects
            working_matches = []
            for word_match in word_matches:
                for match in matches:
                    working_match = copy.copy(match)
                    if not match_already_contains_structurally_matched_document_token(working_match,
                            word_match.structurally_matched_document_token):
                        working_match.word_matches.append(word_match)
                        if word_match.is_negated:
                            working_match.is_negated = True
                        if word_match.is_uncertain:
                            working_match.is_uncertain = True
                        if search_phrase_token.i == search_phrase.root_token.i:
                            working_match.index_within_document = word_match.document_token.i
                        working_matches.append(working_match)
            matches = working_matches

        matches_to_return = []
        # now carry out the coherence check
        for match in matches:
            not_yet_traversed_document_token_indexes = set(
                    word_match.document_token.i for word_match in match.word_matches)
            for document_token_matching_root in (word_match.document_token
                    for word_match in match.word_matches
                    if word_match.search_phrase_token.i == search_phrase.root_token.i):
                check_match_is_coherent_recursively(
                        document_token_matching_root, not_yet_traversed_document_token_indexes, [])
                if len(not_yet_traversed_document_token_indexes) == 0:
                    not_normalized_overall_similarity_measure = 1.0
                    for word_match in match.word_matches:
                        not_normalized_overall_similarity_measure *= word_match.similarity_measure
                    if not_normalized_overall_similarity_measure < 1.0:
                        overall_similarity_measure = \
                                round(not_normalized_overall_similarity_measure ** \
                                (1 / len(search_phrase.matchable_non_entity_tokens_to_lexemes)), 8)
                    else:
                        overall_similarity_measure = 1.0
                    if overall_similarity_measure == 1.0 or \
                            overall_similarity_measure >= self.overall_similarity_threshold:
                        match.overall_similarity_measure = str(
                            overall_similarity_measure)
                        matches_to_return.append(match)
        return matches_to_return

    def _get_matches_starting_at_root_word_match(self, search_phrase, document,
            document_token, document_label):
        """Begin recursive matching where a search phrase root token has matched a document
            token.
        """

        matches_to_return = []
        # array of arrays where each entry corresponds to a search_phrase token and is itself an
        # array of WordMatch instances
        search_phrase_tokens_to_word_matches = [[] for token in search_phrase.doc]
        # array of sets to guard against endless looping during recursion. Each set
        # corresponds to the search phrase token with its index and contains the indexes within
        # the document of tokens to which a match to that search phrase token has been attempted.
        search_phrase_and_document_visited_table = [set() for token in search_phrase.doc]
        self._match_recursively(
                search_phrase=search_phrase,
                search_phrase_token=search_phrase.root_token,
                document=document,
                document_token=document_token,
                search_phrase_tokens_to_word_matches=search_phrase_tokens_to_word_matches,
                search_phrase_and_document_visited_table=search_phrase_and_document_visited_table,
                is_uncertain=document_token._.holmes.is_uncertain,
                structurally_matched_document_token=document_token)
        working_matches = self._build_matches(
                search_phrase=search_phrase,
                document=document,
                search_phrase_tokens_to_word_matches=search_phrase_tokens_to_word_matches,
                document_label=document_label)
        matches_to_return.extend(working_matches)
        return matches_to_return

    def match(self):
        """Finds and returns matches between the search phrases and the documents
        managed by this object.
        """
        if len(self._registered_documents) == 0:
            raise NoSearchedDocumentError(
                'At least one searched document is required to match.')
        if len(self.search_phrases) == 0:
            raise NoSearchPhraseError('At least one search_phrase is required to match.')
        matches = []
        for document_label, registered_document in self._registered_documents.items():
            doc = registered_document.doc
            if self.output_document_matching_message_to_console:
                print('Processing document', document_label)
            # Dictionary used to improve performance when embedding-based matching for root tokens
            # is active and there are multiple search phrases with the same root token word: the
            # same indexes in the document will then match all the search phrase root tokens.
            root_lexeme_to_indexes_to_match_dict = {}
            for search_phrase in self.search_phrases:
                if search_phrase.topic_match_phraselet and len(search_phrase.doc) == 1 and not \
                        self.embedding_based_matching_on_root_words:
                    # We are only matching a single word without embedding, so to improve
                    # performance we avoid entering the subgraph matching code.
                    for word_matching_root_token in self._words_matching_root_token(
                            search_phrase):
                        if word_matching_root_token in \
                                registered_document.words_to_token_indexes_dict.keys():
                            for index in registered_document.words_to_token_indexes_dict[
                                    word_matching_root_token]:
                                minimal_match = Match(search_phrase.label, document_label, True)
                                minimal_match.index_within_document = index
                                matches.append(minimal_match)
                    continue
                if self._is_entitynoun_search_phrase_token(search_phrase.root_token,
                        search_phrase.topic_match_phraselet):
                    for token in doc:
                        if token.pos_ in self.semantic_analyzer.noun_pos:
                            matches.extend(self._get_matches_starting_at_root_word_match(
                                    search_phrase, doc, token, document_label))
                    continue
                else:
                    matched_indexes_set = set()
                    if self._is_entity_search_phrase_token(search_phrase.root_token,
                        search_phrase.topic_match_phraselet):
                        if search_phrase.root_token.text in \
                                registered_document.words_to_token_indexes_dict.keys():
                            matched_indexes_set.update(
                                    registered_document.words_to_token_indexes_dict[
                                    search_phrase.root_token.text])
                    else:
                        for word_matching_root_token in self._words_matching_root_token(
                                search_phrase):
                            if word_matching_root_token in \
                                    registered_document.words_to_token_indexes_dict.keys():
                                matched_indexes_set.update(
                                        registered_document.words_to_token_indexes_dict[
                                        word_matching_root_token])
                if self.embedding_based_matching_on_root_words and not \
                        self._is_entity_search_phrase_token(search_phrase.root_token,
                                search_phrase.topic_match_phraselet):
                    if not search_phrase.topic_match_phraselet:
                        root_token_lemma_to_use = search_phrase.root_token.lemma_
                    else:
                        root_token_lemma_to_use = search_phrase.root_token._.holmes.lemma
                    if root_token_lemma_to_use in root_lexeme_to_indexes_to_match_dict:
                        matched_indexes_set.update(root_lexeme_to_indexes_to_match_dict[
                                root_token_lemma_to_use])
                    else:
                        working_indexes_to_match_for_cache_set = set()
                        for document_word in registered_document.words_to_token_indexes_dict.keys():
                            indexes_to_match = registered_document.words_to_token_indexes_dict[
                                    document_word]
                            similarity_measure = \
                                    search_phrase.matchable_non_entity_tokens_to_lexemes[
                                    search_phrase.root_token.i].similarity(
                                    doc[indexes_to_match[0]])
                            if similarity_measure >= \
                                    search_phrase.single_token_similarity_threshold:
                                matched_indexes_set.update(indexes_to_match)
                                working_indexes_to_match_for_cache_set.update(indexes_to_match)
                        root_lexeme_to_indexes_to_match_dict[root_token_lemma_to_use] = \
                                working_indexes_to_match_for_cache_set
                for index_to_match in sorted(matched_indexes_set):
                    matches.extend(self._get_matches_starting_at_root_word_match(
                            search_phrase, doc, doc[index_to_match], document_label))
        return matches
