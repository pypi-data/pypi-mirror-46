import unittest
from holmes_extractor.semantics import SemanticAnalyzerFactory

analyzer = SemanticAnalyzerFactory().semantic_analyzer(model='de_core_news_sm', debug=False)

class GermanSemanticAnalyzerTest(unittest.TestCase):

    def test_initialize_semantic_dependencies(self):
        doc = analyzer.parse("Der Hund jagte die Katze.")
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '1:sb; 4:oa')
        self.assertEqual(doc[0]._.holmes.string_representation_of_children(), '')
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(), '')
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '')

    def test_one_righthand_sibling_with_and_conjunction(self):
        doc = analyzer.parse("Der Hund und der Löwe jagten die Katze")
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [4])
        self.assertFalse(doc[1]._.holmes.is_involved_in_or_conjunction)
        self.assertFalse(doc[4]._.holmes.is_involved_in_or_conjunction)
        self.assertEqual(doc[4]._.holmes.righthand_siblings, [])

    def test_many_righthand_siblings_with_and_conjunction(self):
        doc = analyzer.parse("Der Hund, der Hund und der Löwe jagten die Katze")
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [4, 7])
        self.assertFalse(doc[1]._.holmes.is_involved_in_or_conjunction)
        self.assertFalse(doc[4]._.holmes.is_involved_in_or_conjunction)
        self.assertFalse(doc[7]._.holmes.is_involved_in_or_conjunction)
        self.assertEqual(doc[4]._.holmes.righthand_siblings, [])
        self.assertEqual(doc[7]._.holmes.righthand_siblings, [])

    def test_one_righthand_sibling_with_or_conjunction(self):
        doc = analyzer.parse("Der Hund oder der Löwe jagten die Katze")
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [4])
        self.assertTrue(doc[1]._.holmes.is_involved_in_or_conjunction)
        self.assertTrue(doc[4]._.holmes.is_involved_in_or_conjunction)
        self.assertEqual(doc[4]._.holmes.righthand_siblings, [])

    def test_many_righthand_siblings_with_or_conjunction(self):
        doc = analyzer.parse("Die Maus, der Hund oder der Löwe jagten die Katze")
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [4, 7])
        self.assertTrue(doc[1]._.holmes.is_involved_in_or_conjunction)
        self.assertTrue(doc[4]._.holmes.is_involved_in_or_conjunction)
        self.assertTrue(doc[7]._.holmes.is_involved_in_or_conjunction)
        self.assertEqual(doc[4]._.holmes.righthand_siblings, [])
        self.assertEqual(doc[7]._.holmes.righthand_siblings, [])

    def test_righthand_siblings_of_semantic_children_two(self):
        doc = analyzer.parse("Der große und starke Hund kam heim")
        self.assertEqual(doc[4]._.holmes.string_representation_of_children(), '1:nk; 3:nk')
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [3])

    def test_righthand_siblings_of_semantic_children_many(self):
        doc = analyzer.parse("Der große, starke und scharfe Hund kam heim")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:nk; 3:nk; 5:nk')
        self.assertEqual(doc[1]._.holmes.righthand_siblings, [3,5])
        self.assertEqual(doc[3]._.holmes.righthand_siblings, [])

    def test_semantic_children_of_righthand_siblings_two(self):
        doc = analyzer.parse("Der große Hund und Löwe")
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '1:nk; 3:cd')
        self.assertEqual(doc[2]._.holmes.righthand_siblings, [4])
        self.assertEqual(doc[4]._.holmes.string_representation_of_children(), '1:nk')

    def test_semantic_children_of_righthand_siblings_many(self):
        doc = analyzer.parse("Der große Hund, Löwe und Elefant")
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '1:nk; 4:cj')
        self.assertEqual(doc[4]._.holmes.string_representation_of_children(), '1:nk; 5:cd')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:nk')

    def test_predicative_adjective(self):
        doc = analyzer.parse("Der Hund war groß")
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(), '3:nk')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-2:None')

    def test_predicative_adjective_with_conjunction(self):
        doc = analyzer.parse("Der Hund und die Katze waren groß und stark")
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(), '2:cd; 6:nk; 8:nk')
        self.assertEqual(doc[4]._.holmes.string_representation_of_children(), '6:nk; 8:nk')

    def test_negator_negation_within_clause(self):
        doc = analyzer.parse("Der Hund jagte die Katze nicht")
        self.assertEqual(doc[2]._.holmes.is_negated, True)

    def test_operator_negation_within_clause(self):
        doc = analyzer.parse("Kein Hund hat irgendeine Katze gejagt")
        self.assertEqual(doc[1]._.holmes.is_negated, True)
        self.assertEqual(doc[2]._.holmes.is_negated, False)

    def test_negator_negation_within_parent_clause(self):
        doc = analyzer.parse("Er meinte nicht, dass der Hund die Katze gejagt hätte")
        self.assertEqual(doc[9]._.holmes.is_negated, True)

    def test_operator_negation_within_parent_clause(self):
        doc = analyzer.parse("Keiner behauptete, dass der Hund die Katze jagte")
        self.assertEqual(doc[5]._.holmes.is_negated, True)

    def test_negator_negation_within_child_clause(self):
        doc = analyzer.parse("Der Hund jagte die Katze, die nicht glücklich war")
        self.assertEqual(doc[2]._.holmes.is_negated, False)

    def test_operator_negation_within_child_clause(self):
        doc = analyzer.parse("Der Hund jagte die Katze die es keinem erzählte")
        self.assertEqual(doc[2]._.holmes.is_negated, False)

    def test_dass_clause(self):
        doc = analyzer.parse("Er ist zuversichtlich, dass der Hund die Katze jagen wird")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(), '4:cp; 6:sb; 8:oa')

    def test_active_perfect(self):
        doc = analyzer.parse("Der Hund hat die Katze gejagt")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb; 4:oa')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-6:None')

    def test_active_pluperfect(self):
        doc = analyzer.parse("Der Hund hatte die Katze gejagt")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb; 4:oa')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-6:None')

    def test_active_future(self):
        doc = analyzer.parse("Der Hund wird die Katze jagen")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb; 4:oa')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-6:None')

    def test_active_future_perfect(self):
        doc = analyzer.parse("Der Hund wird die Katze gejagt haben")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb; 4:oa')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-7:None')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '-6:None')

    def test_von_passive_perfect(self):
        doc = analyzer.parse("Die Katze ist vom Hund gejagt worden")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa; 4:sb')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-7:None')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '-6:None')

    def test_von_passive_pluperfect(self):
        doc = analyzer.parse("Die Katze war vom Hund gejagt worden")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa; 4:sb')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-7:None')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '-6:None')

    def test_von_passive_future(self):
        doc = analyzer.parse("Die Katze wird vom Hund gejagt werden")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa; 4:sb')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-7:None')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '-6:None')

    def test_von_passive_future_perfect(self):
        doc = analyzer.parse("Die Katze wird vom Hund gejagt worden sein")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa; 4:sb')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-8:None')
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '-6:None')
        self.assertEqual(doc[7]._.holmes.string_representation_of_children(), '-7:None')

    def test_complex_tense_noun_conjunction_active(self):
        doc = analyzer.parse("Der Hund und der Löwe haben die Katze und die Maus gejagt")
        self.assertEqual(doc[11]._.holmes.string_representation_of_children(),
                '1:sb; 4:sb; 7:oa; 10:oa')

    def test_complex_tense_noun_conjunction_passive(self):
        doc = analyzer.parse("Die Katze und die Maus werden vom Hund und Löwen gejagt werden")
        self.assertEqual(doc[10]._.holmes.string_representation_of_children(),
                '1:oa; 4:oa; 7:sb; 9:sb')

    def test_complex_tense_verb_conjunction_active(self):
        doc = analyzer.parse("Der Hund wird die Katze gejagt und gefressen haben")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb; 4:oa; 6:cd')
        self.assertEqual(doc[7]._.holmes.string_representation_of_children(), '1:sb; 4:oa')

    def test_complex_tense_verb_conjunction_passive(self):
        doc = analyzer.parse("Die Katze wird vom Hund gejagt und gefressen werden")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa; 4:sb; 6:cd')
        self.assertEqual(doc[7]._.holmes.string_representation_of_children(), '1:oa; 4:sb')

    def test_conjunction_everywhere_active(self):
        doc = analyzer.parse(
                "Der Hund und der Löwe werden die Katze und die Maus jagen und fressen")
        self.assertEqual(doc[11]._.holmes.string_representation_of_children(),
                '1:sb; 4:sb; 7:oa; 10:oa; 12:cd')
        self.assertEqual(doc[13]._.holmes.string_representation_of_children(),
                '1:sb; 4:sb; 7:oa; 10:oa')

    def test_conjunction_everywhere_passive(self):
        doc = analyzer.parse(
                "Die Katze und die Maus werden durch den Hund und den Löwen gejagt und gefressen werden")
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:oa; 4:oa; 8:sb; 11:sb; 13:cd')
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:oa; 4:oa; 8:sb; 11:sb')

    def test_simple_modal_verb_active(self):
        doc = analyzer.parse("Der Hund soll die Katze jagen")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:sb(U); 4:oa(U)')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-6:None')

    def test_simple_modal_verb_passive(self):
        doc = analyzer.parse("Die Katze kann vom Hund gejagt werden")
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '1:oa(U); 4:sb(U)')
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(), '-7:None')

    def test_negated_modal_verb(self):
        doc = analyzer.parse("Der Hund soll die Katze nicht jagen")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:oa(U); 5:ng(U)')
        self.assertTrue(doc[6]._.holmes.is_negated)

    def test_modal_verb_with_conjunction(self):
        doc = analyzer.parse("Der Hund und der Löwe können die Katze und die Maus jagen")
        self.assertEqual(doc[11]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 7:oa(U); 10:oa(U)')
        self.assertEqual(doc[5]._.holmes.string_representation_of_children(), '-12:None')

    def test_relative_pronoun_nominative(self):
        doc = analyzer.parse("Der Hund, der die Katze jagte, war müde")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:sb; 5:oa')

    def test_relative_pronoun_welcher(self):
        doc = analyzer.parse("Der Hund, welcher die Katze jagte, war müde")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:sb; 5:oa')

    def test_relative_pronoun_nominative_with_conjunction(self):
        doc = analyzer.parse("Der Hund, der die Katze und die Maus jagte, war müde")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(), '1:sb; 5:oa; 8:oa')

    def test_relative_pronoun_nominative_with_passive(self):
        doc = analyzer.parse("Die Katze, die vom Hund gejagt wurde, war müde")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:oa; 5:sb')

    def test_relative_pronoun_accusative(self):
        doc = analyzer.parse("Der Bär, den der Hund jagte, war müde")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:oa; 5:sb')

    def test_relative_pronoun_conjunction_everywhere_active(self):
        doc = analyzer.parse(
                "Der Hund, der Elefant und der Bär, die die Katze und die Maus gejagt und gefressen haben, waren müde")
        self.assertEqual(doc[15]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 7:sb; 11:oa; 14:oa; 16:cd')
        self.assertEqual(doc[17]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 7:sb; 11:oa; 14:oa')

    def test_relative_pronoun_conjunction_everywhere_passive(self):
        doc = analyzer.parse(
                "Die Katze, die Maus und der Vogel, die vom Bären, Löwen und Hund gejagt und gefressen worden sind, waren tot")
        self.assertEqual(doc[16]._.holmes.string_representation_of_children(),
                '1:oa(U); 4:oa(U); 7:oa; 11:sb; 13:sb; 15:sb; 17:cd')
        self.assertEqual(doc[18]._.holmes.string_representation_of_children(),
                '1:oa(U); 4:oa(U); 7:oa; 11:sb; 13:sb; 15:sb')

    def test_separable_verb(self):
        doc = analyzer.parse("Er nimmt die Situation auf")
        self.assertEqual(doc[1]._.holmes.lemma, 'aufnehmen')
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(), '0:sb; 3:oa')

    def test_separable_verb_in_main_clause_but_infinitive_in_dependent_clause(self):
        doc = analyzer.parse("Der Mitarbeiter hatte vor, dies zu tun")
        self.assertEqual(doc[7]._.holmes.lemma, 'tun')

    def test_separable_verb_in_main_clause_but_separable_infinitive_in_dependent_clause(self):
        doc = analyzer.parse("Der Mitarbeiter hatte vor, eine Versicherung abzuschließen")
        self.assertEqual(doc[7]._.holmes.lemma, 'abschließen')

    def test_apprart(self):
        doc = analyzer.parse("Er geht zur Party")
        self.assertEqual(doc[2].lemma_, 'zur')
        self.assertEqual(doc[2]._.holmes.lemma, 'zu')

    def test_von_phrase(self):
        doc = analyzer.parse("Der Abschluss von einer Versicherung")
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(), '2:mnr; 4:nk')

    def test_von_phrase_with_conjunction(self):
        doc = analyzer.parse(
                "Der Abschluss und Aufrechterhaltung von einer Versicherung und einem Vertrag")
        self.assertEqual(doc[1]._.holmes.string_representation_of_children(),
                '2:cd; 4:mnr; 6:nk; 9:nk')
        self.assertEqual(doc[3]._.holmes.string_representation_of_children(),
                '4:mnr; 6:nk; 9:nk')

    def test_subjective_zu_clause_complement_simple_active(self):
        doc = analyzer.parse("Der Hund überlegte, eine Katze zu jagen")
        self.assertEqual(doc[7]._.holmes.string_representation_of_children(), '1:sb(U); 5:oa; 6:pm')

    def test_subjective_zu_clause_complement_with_conjunction_active(self):
        doc = analyzer.parse(
                "Der Hund und der Löwe entschlossen sich, eine Katze und eine Maus zu jagen")
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 9:oa; 12:oa; 13:pm')

    def test_subjective_zu_clause_complement_with_relative_clause_active(self):
        doc = analyzer.parse("Der Hund, der überlegte, eine Katze zu jagen, kam nach Hause")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(), '1:sb(U); 7:oa; 8:pm')

    def test_adjective_complement_simple_active(self):
        doc = analyzer.parse("Der Hund war darüber froh, eine Katze zu jagen")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(), '1:sb(U); 7:oa; 8:pm')

    def test_adjective_complement_with_conjunction_active(self):
        doc = analyzer.parse("Der Hund war darüber besorgt, eine Katze und eine Maus zu jagen")
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:sb(U); 7:oa; 10:oa; 11:pm')

    def test_objective_zu_clause_complement_simple_active(self):
        doc = analyzer.parse("Der Löwe bat den Hund, eine Katze zu jagen")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(), '4:sb(U); 7:oa; 8:pm')

    def test_objective_zu_clause_complement_with_conjunction_active(self):
        doc = analyzer.parse(
                "Der Elefant schlag dem Hund und dem Löwen vor, eine Katze und eine Maus zu jagen")
        self.assertEqual(doc[16]._.holmes.string_representation_of_children(),
                '4:sb(U); 7:sb(U); 11:oa; 14:oa; 15:pm')

    def test_passive_governing_clause_zu_clause_complement_simple_active(self):
        doc = analyzer.parse("Der Hund wurde gebeten, eine Katze zu jagen")
        self.assertEqual(doc[8]._.holmes.string_representation_of_children(), '1:sb(U); 6:oa; 7:pm')

    def test_passive_governing_clause_zu_clause_complement_with_conjunction_active(self):
        doc = analyzer.parse(
                "Dem Hund und dem Löwen wurde vorgeschlagen, eine Katze und eine Maus zu jagen")
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 9:oa; 12:oa; 13:pm')

    def test_um_zu_clause_complement_simple_active(self):
        doc = analyzer.parse("Der Löwe benutzte den Hund, um eine Katze zu jagen")
        self.assertEqual(doc[10]._.holmes.string_representation_of_children(),
                '1:sb(U); 6:cp; 8:oa; 9:pm')

    def test_um_zu_clause_complement_with_conjunction_active(self):
        doc = analyzer.parse(
                "Der Elefant benutzte den Hund und den Löwen, um eine Katze und eine Maus zu jagen")
        self.assertEqual(doc[16]._.holmes.string_representation_of_children(),
                '1:sb(U); 9:cp; 11:oa; 14:oa; 15:pm')

    def test_verb_complement_simple_passive(self):
        doc = analyzer.parse("Die Katze dachte darüber nach, von einem Hund gejagt zu werden")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(),
                '1:oa(U); 8:sb; 10:pm')

    def test_verb_complement_with_conjunction_passive(self):
        doc = analyzer.parse(
                "Die Katze und die Maus dachten darüber nach, von einem Hund und einem Löwen gejagt zu werden")
        self.assertEqual(doc[15]._.holmes.string_representation_of_children(),
                '1:oa(U); 4:oa(U); 11:sb; 14:sb; 16:pm')

    def test_adjective_complement_simple_passive(self):
        doc = analyzer.parse("Die Katze war darüber froh, von einem Hund gejagt zu werden")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(),
                '1:oa(U); 8:sb; 10:pm')

    def test_adjective_complement_with_conjunction_passive(self):
        doc = analyzer.parse(
                "Die Katze war darüber froh, von einem Hund und einem Löwen gejagt zu werden")
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:oa(U); 8:sb; 11:sb; 13:pm')

    def test_subjective_zu_clause_complement_simple_passive(self):
        doc = analyzer.parse("Die Katze entschied, vom Hund gejagt zu werden")
        self.assertEqual(doc[6]._.holmes.string_representation_of_children(), '1:oa(U); 5:sb; 7:pm')

    def test_subjective_zu_clause_complement_with_conjunction_passive(self):
        doc = analyzer.parse(
                "Die Katze und die Maus entschlossen sich, vom Hund und Löwen gejagt zu werden")
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:oa(U); 4:oa(U); 9:sb; 11:sb; 13:pm')

    def test_objective_zu_clause_complement_simple_passive(self):
        doc = analyzer.parse("Der Löwe bat die Katze, vom Hund gejagt zu werden")
        self.assertEqual(doc[8]._.holmes.string_representation_of_children(), '4:oa(U); 7:sb; 9:pm')

    def test_objective_zu_clause_complement_with_conjunction_passive(self):
        doc = analyzer.parse(
                "Der Elefant schlag der Katze und der Maus vor, vom Hund und Löwen gejagt zu werden")
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '4:oa(U); 7:oa(U); 11:sb; 13:sb; 15:pm')

    def test_passive_governing_clause_zu_clause_complement_simple_passive(self):
        doc = analyzer.parse("Die Katze wurde gebeten, von einem Hund gejagt zu werden")
        self.assertEqual(doc[8]._.holmes.string_representation_of_children(), '1:oa(U); 7:sb; 9:pm')

    def test_passive_governing_clause_zu_clause_complement_with_conjunction_active(self):
        doc = analyzer.parse(
                "Der Katze und der Maus wurde vorgeschlagen, von einem Löwen und einem Hund gejagt zu werden")
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:oa(U); 4:oa(U); 10:sb; 13:sb; 15:pm')

    def test_um_zu_clause_complement_simple_passive(self):
        doc = analyzer.parse("Der Löwe benutzte die Katze, um vom Hund gejagt zu werden")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(),
                '1:oa(U); 6:cp; 8:sb; 10:pm')

    def test_um_zu_clause_complement_with_conjunction_passive(self):
        doc = analyzer.parse(
                "Der Elefant benutzte die Katze und die Maus, um vom Hund und Löwen gejagt zu werden")
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:oa(U); 9:cp; 11:sb; 13:sb; 15:pm')

    def test_verb_complement_with_conjunction_of_dependent_verb(self):
        doc = analyzer.parse("Die Katze und die Maus haben entschieden, zu singen und zu schreien")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 8:pm; 10:cd')
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 11:pm')

    def test_subjective_zu_clause_complement_with_conjunction_of_dependent_verb(self):
        doc = analyzer.parse("Die Katze und die Maus entschlossen sich, zu singen und zu schreien")
        self.assertEqual(doc[9]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 8:pm; 10:cd')
        self.assertEqual(doc[12]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 11:pm')

    def test_objective_zu_clause_complement_with_conjunction_of_dependent_verb(self):
        doc = analyzer.parse("Die Katze und die Maus baten den Löwen, zu singen und zu schreien")
        self.assertEqual(doc[10]._.holmes.string_representation_of_children(),
                '7:sb(U); 9:pm; 11:cd')
        self.assertEqual(doc[13]._.holmes.string_representation_of_children(),
                '7:sb(U); 12:pm')

    def test_um_zu_clause_complement_with_conjunction_of_dependent_verb(self):
        doc = analyzer.parse(
                "Die Katze und die Maus benutzen den Löwen, um zu singen und zu schreien")
        self.assertEqual(doc[11]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 9:cp; 10:pm; 12:cd')
        self.assertEqual(doc[14]._.holmes.string_representation_of_children(),
                '1:sb(U); 4:sb(U); 9:cp; 13:pm')

    def test_single_preposition_dependency_added_to_verb(self):
        doc = analyzer.parse(
                "Der Mitarbeiter braucht eine Versicherung für die nächsten fünf Jahre")
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(),
                '1:sb; 4:oa; 5:moposs(U)')

    def test_multiple_preposition_dependencies_added_to_noun(self):
        doc = analyzer.parse(
                "Der Mitarbeiter braucht eine Versicherung für die nächsten fünf Jahre und in Europa")
        self.assertEqual(doc[2]._.holmes.string_representation_of_children(),
                '1:sb; 4:oa; 5:moposs(U); 11:moposs(U)')

    def test_no_exception_thrown_when_preposition_dependency_is_righthand_sibling(self):
        doc = analyzer.parse(
                "Diese Funktionalität erreichen Sie über Datei/Konfiguration für C")

    def test_phrase_in_parentheses_no_exception_thrown(self):
        doc = analyzer.parse(
                "Die Tilgung beginnt in der Auszahlungsphase (d.h. mit der zweiten Auszahlung)")

    def test_von_preposition_in_von_clause_unmatchable(self):
        doc = analyzer.parse(
                "Die Kündigung von einer Versicherung")
        self.assertFalse(doc[2]._.holmes.is_matchable)

    def test_self_referring_dependencies_no_exception_thrown_1(self):
        doc = analyzer.parse(
                "Die Version ist dabei mit der dieser Bug bereits gefixt sein sollte und nur noch nicht produktiv eingespielt.")

    def test_self_referring_dependencies_no_exception_thrown_2(self):
        doc = analyzer.parse(
                "Es sind Papiere, von denen SCD in den Simulationen dann eines auswählt.")

    def test_stripping_adjectival_inflections(self):
        doc = analyzer.parse(
                "Eine interessante Überlegung über gesunde Mittagessen.")
        self.assertEqual(doc[1].lemma_, 'interessante')
        self.assertEqual(doc[1]._.holmes.lemma, 'interessant')
        self.assertEqual(doc[4].lemma_, 'gesunden')
        self.assertEqual(doc[4]._.holmes.lemma, 'gesund')
