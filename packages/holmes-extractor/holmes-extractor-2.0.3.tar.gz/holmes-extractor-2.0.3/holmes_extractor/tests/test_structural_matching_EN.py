import unittest
import holmes_extractor as holmes
import os

script_directory = os.path.dirname(os.path.realpath(__file__))
ontology = holmes.Ontology(os.sep.join((script_directory,'test_ontology.owl')))
common_holmes_manager = holmes.Manager(model='en_core_web_lg', ontology=ontology)
common_holmes_manager.register_search_phrase("A dog chases a cat")
common_holmes_manager.register_search_phrase("The man was poor")
common_holmes_manager.register_search_phrase("The rich man")
common_holmes_manager.register_search_phrase("Someone eats a sandwich")
common_holmes_manager.register_search_phrase("A colleague's computer")
common_holmes_manager.register_search_phrase("An ENTITYPERSON opens an account")
common_holmes_manager.register_search_phrase("A dog eats a bone")
common_holmes_manager.register_search_phrase("Who fell asleep?")
common_holmes_manager.register_search_phrase("Who is sad?")
common_holmes_manager.register_search_phrase("Insurance for years")
common_holmes_manager.register_search_phrase("An employee needs insurance for the next five years")
common_holmes_manager.register_search_phrase("Somebody gives a file to an employee")
common_holmes_manager.register_search_phrase("Somebody gives a boss a file")
common_holmes_manager.register_search_phrase("Serendipity")
common_holmes_manager.register_search_phrase("Somebody eats at an office")
holmes_manager_with_variable_search_phrases = holmes.Manager(model='en_core_web_lg',
        ontology=ontology)
holmes_manager_with_embeddings = holmes.Manager(model='en_core_web_lg',
        overall_similarity_threshold=0.7)

class EnglishStructuralMatchingTest(unittest.TestCase):

    def _get_matches(self, common_holmes_manager, text):
        common_holmes_manager.remove_all_documents()
        common_holmes_manager.parse_and_register_document(document_text=text)
        return common_holmes_manager.match()

    def test_direct_matching(self):
        matches = self._get_matches(common_holmes_manager, "The dog chased the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_negated)

    def test_matching_within_large_sentence_with_negation(self):
        matches = self._get_matches(common_holmes_manager, "We discussed various things. Although it had never been claimed that a dog had ever chased a cat, it was nonetheless true. This had always been a difficult topic.")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_negated)

    def test_nouns_inverted(self):
        matches = self._get_matches(common_holmes_manager, "The cat chased the dog")
        self.assertEqual(len(matches), 0)

    def test_different_object(self):
        matches = self._get_matches(common_holmes_manager, "The dog chased the horse")
        self.assertEqual(len(matches), 0)

    def test_verb_negation(self):
        matches = self._get_matches(common_holmes_manager, "The dog did not chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_negated)

    def test_noun_phrase_negation(self):
        matches = self._get_matches(common_holmes_manager, "No dog chased any cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_negated)

    def test_irrelevant_negation(self):
        matches = self._get_matches(common_holmes_manager, "The dog who was not old chased the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_negated)

    def test_adjective_swapping(self):
        matches = self._get_matches(common_holmes_manager, "The poor man")
        self.assertEqual(len(matches), 1)
        matches = self._get_matches(common_holmes_manager, "The man was rich")
        self.assertEqual(len(matches), 1)

    def test_adjective_swapping_with_conjunction(self):
        matches = self._get_matches(common_holmes_manager, "The poor and poor man")
        self.assertEqual(len(matches), 2)
        self.assertFalse(matches[0].is_uncertain)
        self.assertFalse(matches[1].is_uncertain)
        matches = self._get_matches(common_holmes_manager, "The man was rich and rich")
        self.assertEqual(len(matches), 2)

    def test_conjunction_with_and(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog and the dog chased a cat and another cat")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertFalse(text_match.is_uncertain)

    def test_conjunction_with_or(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog or the dog chased a cat and another cat")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertTrue(text_match.is_uncertain)

    def test_threeway_conjunction_with_or(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog, the dog or the dog chased a cat and another cat")
        for text_match in matches:
            self.assertTrue(text_match.is_uncertain)

    def test_generic_pronoun(self):
        matches = self._get_matches(common_holmes_manager, "A sandwich was eaten")
        self.assertEqual(len(matches), 1)

    def test_active(self):
        matches = self._get_matches(common_holmes_manager, "The dog will chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)
        matches = self._get_matches(common_holmes_manager, "The dog used to chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_passive(self):
        matches = self._get_matches(common_holmes_manager, "The cat is chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)
        matches = self._get_matches(common_holmes_manager, "The cat will be chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)
        matches = self._get_matches(common_holmes_manager,
                "The cat was going to be chased by the dog")
        self.assertEqual(len(matches), 1)
        matches = self._get_matches(common_holmes_manager,
                "The cat always used to be chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_was_going_to_active(self):
        matches = self._get_matches(common_holmes_manager, "The dog was going to chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_was_going_to_passive(self):
        matches = self._get_matches(common_holmes_manager,
                "The cat was going to be chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_active_complement_without_object(self):
        matches = self._get_matches(common_holmes_manager, "The dog decided to chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_active_complement_with_object(self):
        matches = self._get_matches(common_holmes_manager, "He told the dog to chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_passive_complement_without_object(self):
        matches = self._get_matches(common_holmes_manager, "The sandwich decided to be eaten")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_passive_complement_with_object(self):
        matches = self._get_matches(common_holmes_manager,
                "He told the cat to be chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_relative_clause_without_pronoun(self):
        matches = self._get_matches(common_holmes_manager, "The cat the dog chased was scared")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_relative_clause_without_pronoun_inverted(self):
        matches = self._get_matches(common_holmes_manager, "The dog the cat chased was scared")
        self.assertEqual(len(matches), 0)

    def test_subjective_relative_clause_with_pronoun(self):
        matches = self._get_matches(common_holmes_manager, "The dog who chased the cat came home")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_subjective_relative_clause_with_pronoun_and_conjunction(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog who chased the cat and cat came home")
        self.assertEqual(len(matches), 2)
        self.assertFalse(matches[0].is_uncertain)
        self.assertFalse(matches[1].is_uncertain)

    def test_objective_relative_clause_with_wh_pronoun(self):
        matches = self._get_matches(common_holmes_manager, "The cat who the dog chased came home")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_objective_relative_clause_with_that_pronoun(self):
        matches = self._get_matches(common_holmes_manager, "The cat that the dog chased came home")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_whose_clause(self):
        matches = self._get_matches(common_holmes_manager,
                "The colleague whose computer I repaired last week has gone home")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_whose_clause_with_conjunction_of_possessor(self):
        matches = self._get_matches(common_holmes_manager,
                "The colleague and colleague whose computer I repaired last week have gone home")
        self.assertEqual(len(matches), 2)
        self.assertTrue(matches[0].is_uncertain)
        self.assertFalse(matches[1].is_uncertain)

    def test_whose_clause_with_conjunction_of_possessed(self):
        matches = self._get_matches(common_holmes_manager,
                "The colleague whose computer and computer I repaired last week has gone home")
        self.assertEqual(len(matches), 2)
        self.assertFalse(matches[0].is_uncertain)
        self.assertFalse(matches[1].is_uncertain)

    def test_phrasal_verb(self):
        matches = self._get_matches(common_holmes_manager, "Richard Hudson took out an account")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_modal_verb(self):
        matches = self._get_matches(common_holmes_manager, "The dog could chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_active_participle(self):
        matches = self._get_matches(common_holmes_manager, "The dog chasing the cat was a problem")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_passive_participle(self):
        matches = self._get_matches(common_holmes_manager,
                "He talked about the cat chased by the dog")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_active_participle(self):
        matches = self._get_matches(common_holmes_manager, "The dog chasing the cat was a problem")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_gerund_with_of(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog's chasing of the cat was a problem")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_gerund_with_by(self):
        matches = self._get_matches(common_holmes_manager,
                "The cat's chasing by the dog was a problem")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_objective_modifying_adverbial_phrase(self):
        matches = self._get_matches(common_holmes_manager, "The cat-chasing dog and dog came home")
        self.assertEqual(len(matches), 2)
        self.assertFalse(matches[0].is_uncertain)
        self.assertTrue(matches[1].is_uncertain)

    def test_objective_modifying_adverbial_phrase_with_inversion(self):
        matches = self._get_matches(common_holmes_manager, "The dog-chasing cat and cat came home")
        self.assertEqual(len(matches), 0)

    def test_subjective_modifying_adverbial_phrase(self):
        matches = self._get_matches(common_holmes_manager, "The dog-chased cat and cat came home")
        self.assertEqual(len(matches), 2)
        self.assertFalse(matches[0].is_uncertain)
        self.assertTrue(matches[1].is_uncertain)

    def test_subjective_modifying_adverbial_phrase_with_inversion(self):
        matches = self._get_matches(common_holmes_manager, "The cat-chased dog and dog came home")
        self.assertEqual(len(matches), 0)

    def test_adjective_prepositional_complement_with_conjunction_active(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog and the lion were worried about chasing a cat and a mouse")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_adjective_prepositional_complement_with_conjunction_passive(self):
        matches = self._get_matches(common_holmes_manager,
                "The cat and the mouse were worried about being chased by a dog and a lion")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_verb_prepositional_complement_with_conjunction_active(self):
        matches = self._get_matches(common_holmes_manager,
                "The dog and the lion were thinking about chasing a cat and a mouse")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_verb_prepositional_complement_with_conjunction_passive(self):
        matches = self._get_matches(common_holmes_manager,
                "The cat and the mouse were thinking about being chased by a dog and a lion")
        self.assertEqual(len(matches), 1)
        self.assertTrue(matches[0].is_uncertain)

    def test_passive_search_phrase_with_active_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "A cat was chased by a dog")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog will chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_passive_search_phrase_with_active_conjunction_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "A cat was chased by a dog")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog and the dog have chased a cat and a cat")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertFalse(text_match.is_uncertain)

    def test_passive_search_phrase_with_passive_conjunction_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "A cat was chased by a dog")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The cat and the cat will be chased by a dog and a dog")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertFalse(text_match.is_uncertain)

    def test_passive_search_phrase_with_negated_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "A cat was chased by a dog")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog never chased the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)
        self.assertTrue(matches[0].is_negated)

    def test_question_search_phrase_with_active_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "Why do dogs chase cats?")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog will chase the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)

    def test_question_search_phrase_with_active_conjunction_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "Why do dogs chase cats?")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog and the dog have chased a cat and a cat")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertFalse(text_match.is_uncertain)

    def test_question_search_phrase_with_passive_conjunction_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "Why do dogs chase cats?")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The cat and the cat will be chased by a dog and a dog")
        self.assertEqual(len(matches), 4)
        for text_match in matches:
            self.assertFalse(text_match.is_uncertain)

    def test_question_search_phrase_with_negated_searched_sentence(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "Why do dogs chase cats?")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "The dog never chased the cat")
        self.assertEqual(len(matches), 1)
        self.assertFalse(matches[0].is_uncertain)
        self.assertTrue(matches[0].is_negated)

    def test_coherent_matching_1(self):
        holmes_manager_with_embeddings.register_search_phrase("Farmers go into the mountains")
        matches = self._get_matches(holmes_manager_with_embeddings,
                "In Norway the peasants go into the mountains")
        self.assertEqual(len(matches), 1) # 2 if coherent matching not working properly

    def test_coherent_matching_2(self):
        matches = self._get_matches(common_holmes_manager,
                "It was quite early when she kissed her old grandmother, who was still asleep.")
        self.assertEqual(len(matches), 1) # error if coherent matching not working properly

    def test_original_search_phrase_root_not_matchable(self):
        matches = self._get_matches(common_holmes_manager, "The man was very sad.")
        self.assertEqual(len(matches), 1) # error if coherent matching not working properly

    def test_entitynoun_as_root_node(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "An ENTITYNOUN")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "Dogs, cats, lions and elephants")
        self.assertEqual(len(matches), 4)

    def test_entitynoun_as_non_root_node(self):
        holmes_manager_with_variable_search_phrases.remove_all_search_phrases()
        holmes_manager_with_variable_search_phrases.register_search_phrase(
                "I saw an ENTITYNOUN")
        matches = self._get_matches(holmes_manager_with_variable_search_phrases,
                "I saw a dog and a cat")
        self.assertEqual(len(matches), 2)

    def test_matching_additional_preposition_dependency_on_noun(self):
        matches = self._get_matches(common_holmes_manager,
                "An employee needs insurance for the next five years")
        self.assertEqual(len(matches), 2)
        for match in matches:
            if len(match.word_matches) == 7:
                self.assertFalse(match.is_uncertain)
            else:
                self.assertTrue(match.is_uncertain)

    def test_dative_prepositional_phrase_in_document_dative_noun_phrase_in_search_phrase_1(self):
        matches = self._get_matches(common_holmes_manager,
                "The file was given to the boss and the boss")
        self.assertEqual(len(matches), 2)

    def test_dative_prepositional_phrase_in_document_dative_noun_phrase_in_search_phrase_2(self):
        matches = self._get_matches(common_holmes_manager,
                "The file was given to the boss and to the boss")
        self.assertEqual(len(matches), 2)

    def test_dative_noun_phrase_in_document_dative_prepositional_phrase_in_search_phrase(self):
        matches = self._get_matches(common_holmes_manager,
                "Somebody gave the employee the file")
        self.assertEqual(len(matches), 1)

    def test_matching_single_word(self):
        matches = self._get_matches(common_holmes_manager,
                "serendipity")
        self.assertEqual(len(matches), 1)

    def test_matching_displaced_preposition_simple(self):
        matches = self._get_matches(common_holmes_manager,
                "The office you ate your roll at was new")
        self.assertEqual(len(matches), 1)

    def test_matching_displaced_preposition_with_conjunction(self):
        matches = self._get_matches(common_holmes_manager,
                "The office and the office that you ate your roll at were new")
        self.assertEqual(len(matches), 2)
