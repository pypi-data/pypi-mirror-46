import unittest
import holmes_extractor as holmes
from holmes_extractor.extensive_matching import TopicMatcher
import os

script_directory = os.path.dirname(os.path.realpath(__file__))
ontology = holmes.Ontology(os.sep.join((script_directory,'test_ontology.owl')))
holmes_manager = holmes.Manager(model='en_coref_lg', ontology=ontology,
        overall_similarity_threshold=0.85)
holmes_manager_embedding_on_root = holmes.Manager(model='en_coref_lg', ontology=ontology,
        overall_similarity_threshold=0.72, embedding_based_matching_on_root_words=True)

class EnglishTopicMatchingTest(unittest.TestCase):

    def _check_equals(self, text_to_match, document_text, highest_score, embedding_on_root = False):
        if embedding_on_root:
            manager = holmes_manager_embedding_on_root
        else:
            manager = holmes_manager
        manager.remove_all_documents()
        manager.parse_and_register_document(document_text)
        topic_matches = manager.topic_match_documents_against(text_to_match, relation_score=20,
                single_word_score=10)
        self.assertEqual(int(topic_matches[0].score), highest_score)

    def test_direct_matching(self):
        self._check_equals("A plant grows", "A plant grows", 29)

    def test_direct_matching_nonsense_word(self):
        self._check_equals("My friend visited gegwghg", "Peter visited gegwghg", 29)

    def test_coref_matching(self):
        self._check_equals("A plant grows", "I saw a plant. It was growing", 29)

    def test_entity_matching(self):
        self._check_equals("My friend visited ENTITYGPE", "Peter visited Paris", 29)

    def test_entitynoun_matching(self):
        self._check_equals("My friend visited ENTITYNOUN", "Peter visited a city", 20)

    def test_ontology_matching(self):
        self._check_equals("I saw an animal", "Somebody saw a cat", 29)

    def test_ontology_matching_word_only(self):
        self._check_equals("I saw an animal", "Somebody chased a cat", 10)

    def test_embedding_matching_not_root(self):
        self._check_equals("I saw a king", "Somebody saw a queen", 20)

    def test_embedding_matching_root(self):
        self._check_equals("I saw a king", "Somebody saw a queen", 29, True)

    def test_embedding_matching_root_word_only(self):
        self._check_equals("king", "queen", 10, True)

    def test_matching_only_adjective(self):
        self._check_equals("nice", "nice", 10, False)

    def test_matching_only_adjective_where_noun(self):
        self._check_equals("nice place", "nice", 10, False)

    def test_stopwords(self):
        self._check_equals("The donkey has a roof", "The donkey has a roof", 19, False)

    def test_stopwords_control(self):
        self._check_equals("The donkey gets a roof", "The donkey gets a roof", 82, False)

    def test_indexes(self):
        holmes_manager.remove_all_documents()
        holmes_manager.parse_and_register_document(
                "This is an irrelevant sentence. I think a plant grows.")
        topic_matches = holmes_manager.topic_match_documents_against("A plant grows")
        self.assertEqual(topic_matches[0].sentences_start_index, 6)
        self.assertEqual(topic_matches[0].sentences_end_index, 11)
        self.assertEqual(topic_matches[0].start_index, 9)
        self.assertEqual(topic_matches[0].end_index, 10)
        self.assertEqual(topic_matches[0].relative_start_index, 3)
        self.assertEqual(topic_matches[0].relative_end_index, 4)

    def test_additional_phraselets(self):
        holmes_manager.remove_all_documents()
        holmes_manager.remove_all_search_phrases()
        holmes_manager.parse_and_register_document(
                "Peter visited Paris and a dog chased a cat. Beef and lamb and pork.")
        doc = holmes_manager.semantic_analyzer.parse("My friend visited ENTITYGPE")
        holmes_manager.structural_matcher.register_phraselets(doc,
                replace_with_hypernym_ancestors=False,
                match_all_words=False,
                returning_serialized_phraselets=False)
        holmes_manager.structural_matcher.register_search_phrase("A dog chases a cat", None, True)
        holmes_manager.structural_matcher.register_search_phrase("beef", None, True)
        holmes_manager.structural_matcher.register_search_phrase("lamb", None, True)
        position_sorted_structural_matches = \
                sorted(holmes_manager.structural_matcher.match(), key=lambda match:
                (match.document_label, match.index_within_document))
        topic_matcher = TopicMatcher(holmes_manager,
                maximum_activation_distance=75,
                relation_score=20,
                single_word_score=5,
                overlapping_relation_multiplier=1.5,
                overlap_memory_size=10,
                maximum_activation_value=1000,
                sideways_match_extent=100,
                number_of_results=1)
        score_sorted_structural_matches = topic_matcher.perform_activation_scoring(
                position_sorted_structural_matches)
        topic_matches = topic_matcher.get_topic_matches(score_sorted_structural_matches,
                position_sorted_structural_matches)
        self.assertEqual(topic_matches[0].start_index, 1)
        self.assertEqual(topic_matches[0].end_index, 12)

    def test_phraselets_removed(self):
        holmes_manager.remove_all_documents()
        holmes_manager.remove_all_search_phrases()
        holmes_manager.parse_and_register_document(
                "Peter visited Paris and a dog chased a cat. Beef and lamb and pork.")
        doc = holmes_manager.semantic_analyzer.parse(
                "My friend visited ENTITYGPE and ate some pork")
        holmes_manager.structural_matcher.register_phraselets(doc,
                replace_with_hypernym_ancestors=False,
                match_all_words=False,
                returning_serialized_phraselets=False)
        holmes_manager.remove_all_search_phrases_with_label("word: pork")
        position_sorted_structural_matches = \
                sorted(holmes_manager.structural_matcher.match(), key=lambda match:
                (match.document_label, match.index_within_document))
        topic_matcher = TopicMatcher(holmes_manager,
                maximum_activation_distance=75,
                relation_score=20,
                single_word_score=5,
                overlapping_relation_multiplier=1.5,
                overlap_memory_size=10,
                maximum_activation_value=1000,
                sideways_match_extent=100,
                number_of_results=1)
        score_sorted_structural_matches = topic_matcher.perform_activation_scoring(
                position_sorted_structural_matches)
        topic_matches = topic_matcher.get_topic_matches(score_sorted_structural_matches,
                position_sorted_structural_matches)
        self.assertEqual(topic_matches[0].start_index, 1)
        self.assertEqual(topic_matches[0].end_index, 2)

    def test_phraselets_removed_control_case(self):
        holmes_manager.remove_all_documents()
        holmes_manager.remove_all_search_phrases()
        holmes_manager.parse_and_register_document(
                "Peter visited Paris and a dog chased a cat. Beef and lamb and pork.")
        doc = holmes_manager.semantic_analyzer.parse(
                "My friend visited ENTITYGPE and ate some pork")
        holmes_manager.structural_matcher.register_phraselets(doc,
                replace_with_hypernym_ancestors=False,
                match_all_words=False,
                returning_serialized_phraselets=False)
        position_sorted_structural_matches = \
                sorted(holmes_manager.structural_matcher.match(), key=lambda match:
                (match.document_label, match.index_within_document))
        topic_matcher = TopicMatcher(holmes_manager,
                maximum_activation_distance=75,
                relation_score=20,
                single_word_score=5,
                overlapping_relation_multiplier=1.5,
                overlap_memory_size=10,
                maximum_activation_value=1000,
                sideways_match_extent=100,
                number_of_results=1)
        score_sorted_structural_matches = topic_matcher.perform_activation_scoring(
                position_sorted_structural_matches)
        topic_matches = topic_matcher.get_topic_matches(score_sorted_structural_matches,
                position_sorted_structural_matches)
        self.assertEqual(topic_matches[0].start_index, 1)
        self.assertEqual(topic_matches[0].end_index, 14)
