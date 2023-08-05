import unittest
import holmes_extractor as holmes
import os
from holmes_extractor.tests.testing_utils import HolmesInstanceManager

script_directory = os.path.dirname(os.path.realpath(__file__))
ontology = holmes.Ontology(os.sep.join((script_directory,'test_ontology.owl')))
coref_holmes_manager = HolmesInstanceManager(ontology).en_coref_lg_ontology
coref_holmes_manager.register_search_phrase("A dog chases a cat")
coref_holmes_manager.register_search_phrase("A big horse chases a cat")
coref_holmes_manager.register_search_phrase("A tiger chases a little cat")
coref_holmes_manager.register_search_phrase("A big lion chases a cat")
coref_holmes_manager.register_search_phrase("An ENTITYPERSON needs insurance")
coref_holmes_manager.register_search_phrase("University for four years")
coref_holmes_manager.register_search_phrase("A big company makes a loss")
coref_holmes_manager.register_search_phrase("A dog who chases rats chases mice")
coref_holmes_manager.register_search_phrase("A tired dog")
coref_holmes_manager.register_search_phrase("A panther chases a panther")
coref_holmes_manager.register_search_phrase("A leopard chases a leopard")
no_coref_holmes_manager = holmes.Manager(model='en_coref_lg', ontology=ontology,
        perform_coreference_resolution=False)
no_coref_holmes_manager.register_search_phrase("A dog chases a cat")
embeddings_coref_holmes_manager = holmes.Manager(model='en_coref_lg',
        overall_similarity_threshold=0.85)
embeddings_coref_holmes_manager.register_search_phrase('A man loves a woman')

class CoreferenceEnglishMatchingTest(unittest.TestCase):

    def _check_word_match(self, match, word_match_index, document_token_index, extracted_word):
        word_match = match.word_matches[word_match_index]
        self.assertEqual(word_match.document_token.i, document_token_index)
        self.assertEqual(word_match.extracted_word, extracted_word)

    def test_simple_pronoun_coreference_same_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document("I saw a dog and it was chasing a cat.")
        matches = coref_holmes_manager.match()
        self._check_word_match(matches[0], 0, 3, 'dog')
        self._check_word_match(matches[0], 1, 7, 'chase')
        self._check_word_match(matches[0], 2, 9, 'cat')

    def test_perform_coreference_resolution_false(self):
        no_coref_holmes_manager.remove_all_documents()
        no_coref_holmes_manager.parse_and_register_document("I saw a dog and it was chasing a cat.")
        matches = no_coref_holmes_manager.match()
        self.assertEqual(len(matches), 0)

    def test_simple_pronoun_coreference_same_sentence_wrong_structure(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog and it was being chased by a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 0)

    def test_simple_pronoun_coreference_same_sentence_plural_antecedent(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw dogs and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 2, 'dog')

    def test_simple_pronoun_coreference_same_sentence_conjunction_in_antecedent_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog and a dog and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'dog')
        self._check_word_match(matches[1], 0, 6, 'dog')

    def test_simple_pronoun_coreference_same_sentence_conjunction_in_antecedent_left_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog and a horse and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'dog')

    def test_simple_pronoun_coreference_same_sentence_conjunction_in_antecedent_right_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a horse and a dog and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 6, 'dog')

    def test_simple_pronoun_coreference_same_sentence_conjunction_pronouns_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter and Jane, and he and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'Peter')
        self._check_word_match(matches[1], 0, 5, 'Jane')

    def test_simple_pronoun_coreference_same_sentence_conjunction_lefthand_is_pronoun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter, and he and Jane needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'Peter')
        self._check_word_match(matches[1], 0, 8, 'Jane')

    def test_simple_pronoun_coreference_same_sentence_conjunction_righthand_is_pronoun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Jane, and Peter and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 6, 'Peter')
        self._check_word_match(matches[1], 0, 3, 'Jane')

    def test_simple_pronoun_coreference_same_sentence_conjunction_lefthand_noun_not_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Jane, and a horse and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'Jane')

    def test_simple_pronoun_coreference_same_sentence_conjunction_righthand_noun_not_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter, and he and a horse needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'Peter')

    def test_simple_pronoun_coreference_diff_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document("I saw a cat. A dog was chasing it.")
        matches = coref_holmes_manager.match()
        self._check_word_match(matches[0], 0, 6, 'dog')
        self._check_word_match(matches[0], 1, 8, 'chase')
        self._check_word_match(matches[0], 2, 3, 'cat')

    def test_simple_pronoun_coreference_diff_sentence_wrong_structure(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog. It was being chased by a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 0)

    def test_simple_pronoun_coreference_diff_sentence_plural_antecedent(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw cats. They were being chased by a dog.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 2, 'cat')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_in_antecedent_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a cat and a cat. A dog was chasing them.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 2, 3, 'cat')
        self._check_word_match(matches[1], 2, 6, 'cat')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_in_antecedent_left_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a cat and a horse. A dog was chasing them.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 3, 'cat')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_in_antecedent_right_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a horse and a cat. They were being chased by a dog.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 6, 'cat')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_pronouns_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter and Jane. He and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'Peter')
        self._check_word_match(matches[1], 0, 5, 'Jane')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_lefthand_is_pronoun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter. He and Jane needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'Peter')
        self._check_word_match(matches[1], 0, 7, 'Jane')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_righthand_is_pronoun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Jane. Peter and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 5, 'Peter')
        self._check_word_match(matches[1], 0, 3, 'Jane')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_lefthand_noun_not_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Jane. A horse and she needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'Jane')

    def test_simple_pronoun_coreference_diff_sentence_conjunction_righthand_noun_not_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I talked to Peter. He and a horse needed insurance.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'Peter')

    def test_pronoun_coreferent_has_dependency_same_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and it was chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_plural_pronoun_coreferent_has_dependency_same_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw big horses and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 2, 'big')
        self._check_word_match(matches[0], 1, 3, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_same_sentence_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and a big horse and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')
        self._check_word_match(matches[1], 0, 7, 'big')
        self._check_word_match(matches[1], 1, 8, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_same_sentence_left_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and a little horse and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_same_sentence_right_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse and a big horse and they were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 7, 'big')
        self._check_word_match(matches[0], 1, 8, 'horse')

    def test_pronoun_coreferents_with_pronoun_conjunction_same_sentence_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse, and it and a big lion were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')
        self._check_word_match(matches[1], 0, 10, 'big')
        self._check_word_match(matches[1], 1, 11, 'lion')

    def test_pronoun_coreferents_with_pronoun_conjunction_same_sentence_pronoun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse, and it and a little horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_pronoun_coreferents_with_pronoun_conjunction_same_sentence_noun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse, and it and a big horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 10, 'big')
        self._check_word_match(matches[0], 1, 11, 'horse')

    def test_noun_coreferent_has_dependency_same_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and the horse was chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 7, 'horse')

    def test_plural_noun_coreferent_has_dependency_same_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw big horses and the horses were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 2, 'big')
        self._check_word_match(matches[0], 1, 6, 'horse')

    def test_noun_coreferents_with_pronoun_conjunction_same_sentence_noun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse, and the horse and a big horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 11, 'big')
        self._check_word_match(matches[0], 1, 12, 'horse')

    def test_pronoun_coreferent_has_dependency_diff_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. It was chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_plural_pronoun_coreferent_has_dependency_diff_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw big horses. They were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 2, 'big')
        self._check_word_match(matches[0], 1, 3, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_diff_sentence_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and a big horse. They were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')
        self._check_word_match(matches[1], 0, 7, 'big')
        self._check_word_match(matches[1], 1, 8, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_diff_sentence_left_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse and a little horse. They were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_pronoun_coreferents_with_dependency_conjunction_diff_sentence_right_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse and a big horse. They were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 7, 'big')
        self._check_word_match(matches[0], 1, 8, 'horse')

    def test_pronoun_coreferents_with_pronoun_conjunction_diff_sentence_both_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. It and a big lion were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')
        self._check_word_match(matches[1], 0, 9, 'big')
        self._check_word_match(matches[1], 1, 10, 'lion')

    def test_pronoun_coreferents_with_pronoun_conjunction_diff_sentence_pronoun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. It and a little horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 4, 'horse')

    def test_pronoun_coreferents_with_pronoun_conjunction_diff_sentence_noun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse. It and a big horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 9, 'big')
        self._check_word_match(matches[0], 1, 10, 'horse')

    def test_noun_coreferent_has_dependency_diff_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. The horse was chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 7, 'horse')

    def test_plural_noun_coreferent_has_dependency_diff_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw big horses. The horses were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 2, 'big')
        self._check_word_match(matches[0], 1, 6, 'horse')

    def test_noun_coreferents_with_pronoun_conjunction_diff_sentence_noun_matches(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little horse. The horse and a big horse were chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 10, 'big')
        self._check_word_match(matches[0], 1, 11, 'horse')

    def test_noun_coreferent_has_dependency_diff_sentence_relative_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. The horse who was chasing a cat was happy.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 7, 'horse')

    def test_pronoun_coreferent_has_dependency_three_sentences(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a horse. It was chasing a cat. It was big.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 13, 'big')
        self._check_word_match(matches[0], 1, 3, 'horse')

    def test_pronoun_coreferent_in_active_verbal_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog. It was thinking about chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'dog')
        self.assertTrue(matches[0].is_uncertain)

    def test_pronoun_coreferent_in_passive_verbal_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a cat. It was thinking about being chased by a dog.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 3, 'cat')
        self.assertTrue(matches[0].is_uncertain)

    def test_pronoun_coreferent_in_active_adjectival_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog. It was happy about chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'dog')
        self.assertTrue(matches[0].is_uncertain)

    def test_pronoun_coreferent_in_passive_adjectival_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a cat. It was happy about being chased by a dog.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 3, 'cat')
        self.assertTrue(matches[0].is_uncertain)

    def test_noun_coreferent_in_active_verbal_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. The horse was thinking about chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 7, 'horse')
        self.assertTrue(matches[0].is_uncertain)

    def test_noun_coreferent_in_passive_verbal_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little cat. The cat was thinking about being chased by a tiger.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 3, 'little')
        self._check_word_match(matches[0], 3, 7, 'cat')
        self.assertTrue(matches[0].is_uncertain)

    def test_noun_coreferent_in_active_adjectival_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a big horse. The horse was happy about chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'big')
        self._check_word_match(matches[0], 1, 7, 'horse')
        self.assertTrue(matches[0].is_uncertain)

    def test_noun_coreferent_in_passive_adjectival_governing_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a little cat. The cat was happy about being chased by a tiger.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 2, 3, 'little')
        self._check_word_match(matches[0], 3, 7, 'cat')
        self.assertTrue(matches[0].is_uncertain)

    def test_pronoun_coreferent_in_ambiguous_noun_or_verb_dependency(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We visited the university. Richard attended it for four years")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 3, 'university')
        self.assertTrue(matches[0].is_uncertain)

    def test_reflexive_pronoun_coreferent(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "The panther chased itself")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 1, 'panther')
        self._check_word_match(matches[0], 2, 1, 'panther')

    def test_reflexive_pronoun_coreferents_with_conjunction_same_noun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "The panther and the panther chased themselves")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 4)
        self._check_word_match(matches[0], 0, 1, 'panther')
        self._check_word_match(matches[0], 2, 1, 'panther')
        self._check_word_match(matches[1], 0, 4, 'panther')
        self._check_word_match(matches[1], 2, 1, 'panther')
        self._check_word_match(matches[2], 0, 1, 'panther')
        self._check_word_match(matches[2], 2, 4, 'panther')
        self._check_word_match(matches[3], 0, 4, 'panther')
        self._check_word_match(matches[3], 2, 4, 'panther')

    def test_reflexive_pronoun_coreferents_with_conjunction_diff_noun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "The panther and the leopard chased themselves")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 1, 'panther')
        self._check_word_match(matches[0], 2, 1, 'panther')
        self._check_word_match(matches[1], 0, 4, 'leopard')
        self._check_word_match(matches[1], 0, 4, 'leopard')

    def test_different_extracted_word_preceding_hyponym(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We discussed Peters plc. The big company was in difficulties. It had made a loss")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 1, 7, 'Peters plc')

    def test_different_extracted_word_preceding_individual(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We discussed Bakers plc. The big company was in difficulties. It had made a loss")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 1, 7, 'Bakers plc')

    def test_repeated_noun(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We saw a big dog. The dog was chasing a cat.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)
        self._check_word_match(matches[0], 0, 7, 'dog')

    def test_repeated_noun_match_first_mention(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We saw a tired dog. The dog was chasing a donkey.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 3, 'tired')
        self._check_word_match(matches[0], 1, 4, 'dog')
        self._check_word_match(matches[1], 0, 3, 'tired')
        self._check_word_match(matches[1], 1, 7, 'dog')

    def test_repeated_noun_match_both_mentions(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "We saw a tired dog. The tired dog was chasing a donkey.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 4)
        self._check_word_match(matches[0], 0, 3, 'tired')
        self._check_word_match(matches[0], 1, 4, 'dog')
        self._check_word_match(matches[1], 0, 7, 'tired')
        self._check_word_match(matches[1], 1, 4, 'dog')
        self._check_word_match(matches[2], 0, 3, 'tired')
        self._check_word_match(matches[2], 1, 8, 'dog')
        self._check_word_match(matches[3], 0, 7, 'tired')
        self._check_word_match(matches[3], 1, 8, 'dog')

    def test_mentions_following_structural_match(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "A big horse was chasing a cat. The big horse was happy.")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 0, 1, 'big')
        self._check_word_match(matches[0], 1, 2, 'horse')
        self._check_word_match(matches[1], 0, 9, 'big')
        self._check_word_match(matches[1], 1, 2, 'horse')

    def test_relative_clause(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a cat. The dog that had been chasing it was tired")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 2)
        self._check_word_match(matches[0], 2, 3, 'cat')

    def test_dictionary_sentences_one_sentence(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "A sentence. I saw a dog and it was chasing a cat. Another sentence.")
        matches = coref_holmes_manager.match_returning_dictionaries()
        self.assertEqual(matches[0]['sentences_within_document'],
                "I saw a dog and it was chasing a cat.")

    def test_dictionary_sentences_two_sentences(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "A sentence. I saw a dog.It was chasing a cat. Another sentence.")
        matches = coref_holmes_manager.match_returning_dictionaries()
        self.assertEqual(matches[0]['sentences_within_document'],
                "I saw a dog. It was chasing a cat.")

    def test_dictionary_sentences_three_sentences(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "A sentence. I saw a dog. I was happy.It was chasing a cat. Another sentence.")
        matches = coref_holmes_manager.match_returning_dictionaries()
        self.assertEqual(matches[0]['sentences_within_document'],
                "I saw a dog. I was happy. It was chasing a cat.")

    def test_dictionary_sentences_three_sentences_none_surrounding(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                "I saw a dog.I was happy. It was chasing a cat.")
        matches = coref_holmes_manager.match_returning_dictionaries()
        self.assertEqual(matches[0]['sentences_within_document'],
                "I saw a dog. I was happy. It was chasing a cat.")

    def test_no_loop_with_difficult_sentence(self):
        embeddings_coref_holmes_manager.remove_all_documents()
        embeddings_coref_holmes_manager.parse_and_register_document(
                """Her beautiful, noble child had been a dear angel, and possessed
                the kindest heart; he had loved her so much, and she had loved
                him in return; they had kissed and loved each other, and the
                boy had been her joy, her second life.""")
        matches = embeddings_coref_holmes_manager.match_returning_dictionaries()

    def test_maximum_mentions_difference(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                """There was a dog. He was happy. He was happy. He chased a cat.""")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 1)

    def test_over_maximum_mentions_difference(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                """There was a dog. He was happy. He was happy. He was happy. He chased a cat.""")
        matches = coref_holmes_manager.match()
        self.assertEqual(len(matches), 0)

    def test_involves_coreference_true(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                """I saw a dog. It was chasing a cat.""")
        matches = coref_holmes_manager.match()
        self.assertTrue(matches[0].involves_coreference)
        self.assertTrue(matches[0].word_matches[0].involves_coreference)
        self.assertFalse(matches[0].word_matches[1].involves_coreference)
        self.assertFalse(matches[0].word_matches[2].involves_coreference)

    def test_involves_coreference_false(self):
        coref_holmes_manager.remove_all_documents()
        coref_holmes_manager.parse_and_register_document(
                """A dog was chasing a cat.""")
        matches = coref_holmes_manager.match()
        self.assertFalse(matches[0].involves_coreference)
        self.assertFalse(matches[0].word_matches[0].involves_coreference)
        self.assertFalse(matches[0].word_matches[0].involves_coreference)
        self.assertFalse(matches[0].word_matches[0].involves_coreference)
