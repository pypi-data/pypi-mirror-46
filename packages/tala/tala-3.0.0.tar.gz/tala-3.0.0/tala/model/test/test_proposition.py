import copy
import unittest

from mock import Mock

from tala.model.error import OntologyError
from tala.model.goal import PerformGoal
from tala.model.speaker import Speaker
from tala.model.ontology import Ontology
from tala.model.polarity import Polarity
from tala.model.question import YesNoQuestion
from tala.model.proposition import PreconfirmationProposition, ResolvednessProposition, PrereportProposition, ServiceActionTerminatedProposition, RejectedPropositions, PropositionSet, ServiceResultProposition, Proposition, QuitProposition, MuteProposition, UnderstandingProposition, UnmuteProposition, PredicateProposition, GoalProposition
from tala.model.sort import StringSort, ImageSort
from tala.testing.lib_test_case import LibTestCase
from tala.model.image import Image


class PropositionTests(LibTestCase, unittest.TestCase):
    def setUp(self):
        self.setUpLibTestCase()

    def test_quit_proposition_string(self):
        quit_prop = QuitProposition()
        self.assertEquals("QUIT", unicode(quit_prop))

    def test_quit_proposition_get_type(self):
        quit_prop = QuitProposition()
        self.assertEquals("QUIT", quit_prop.get_type())

    def test_mute_proposition_string(self):
        mute_prop = MuteProposition()
        self.assertEquals("MUTE", unicode(mute_prop))

    def test_unmute_proposition_string(self):
        unmute_prop = UnmuteProposition()
        self.assertEquals("UNMUTE", unicode(unmute_prop))

    def test_quit_proposition_equality(self):
        quit_proposition_1 = QuitProposition()
        quit_proposition_2 = QuitProposition()
        self.assertEquals(quit_proposition_1, quit_proposition_2)

    def test_understanding_proposition_getters(self):
        proposition = self.proposition_dest_city_paris
        und = UnderstandingProposition(Speaker.USR, proposition)
        self.assertEquals(Speaker.USR, und.get_speaker())
        self.assertEquals(proposition, und.get_content())

    def test_understanding_proposition_to_string(self):
        proposition = self.proposition_dest_city_paris
        und = UnderstandingProposition(Speaker.USR, proposition)
        self.assertEquals("und(USR, dest_city(paris))", unicode(und))


class ServiceResultPropositionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.action = "mockup_action"
        self.arguments = ["mockup_arguments"]
        self.proposition = ServiceResultProposition(
            self.ontology_name, self.action, self.arguments, "mock_perform_result"
        )

    def test_is_service_result_proposition(self):
        self.assertTrue(self.proposition.is_service_result_proposition())

    def test_getters(self):
        self.assertEquals(self.action, self.proposition.get_service_action())
        self.assertEquals(self.arguments, self.proposition.get_arguments())
        self.assertEquals("mock_perform_result", self.proposition.get_result())

    def test_equality(self):
        identical_proposition = ServiceResultProposition(
            self.ontology_name, self.action, self.arguments, "mock_perform_result"
        )
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.proposition, identical_proposition)

    def test_inequality_due_to_result(self):
        non_identical_proposition = ServiceResultProposition(
            self.ontology_name, self.action, self.arguments, "other_perform_result"
        )
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.proposition, non_identical_proposition)

    def test_inequality_due_to_action(self):
        other_action = "other_service_action"
        non_identical_proposition = ServiceResultProposition(
            self.ontology_name, other_action, self.arguments, True, None
        )
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.proposition, non_identical_proposition)

    def test_unicode(self):
        self.assertEquals(
            "ServiceResultProposition(mockup_action, ['mockup_arguments'], mock_perform_result)",
            unicode(self.proposition)
        )

    def test_hashable(self):
        set([self.proposition])


class PropositionSetTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.positive_prop_set = PropositionSet([self.proposition_dest_city_london, self.proposition_dest_city_paris])
        self.negative_prop_set = PropositionSet([self.proposition_dest_city_london, self.proposition_dest_city_paris],
                                                polarity=Polarity.NEG)

    def test_equality(self):
        identical_prop_set = PropositionSet([self.proposition_dest_city_london, self.proposition_dest_city_paris])
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.positive_prop_set, identical_prop_set)

    def test_inequality_due_to_propositions(self):
        non_identical_prop_set = PropositionSet([self.proposition_dest_city_london])
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.positive_prop_set, non_identical_prop_set)

    def test_inequality_due_to_polarity(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.negative_prop_set, self.positive_prop_set)

    def test_inequality_due_to_element_order(self):
        non_identical_prop_set = PropositionSet([self.proposition_dest_city_paris, self.proposition_dest_city_london])
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.positive_prop_set, non_identical_prop_set)

    def test_is_positive(self):
        self.assertTrue(self.positive_prop_set.is_positive())
        self.assertFalse(self.negative_prop_set.is_positive())

    def test_get_polarity(self):
        self.assertEquals(Polarity.POS, self.positive_prop_set.get_polarity())
        self.assertEquals(Polarity.NEG, self.negative_prop_set.get_polarity())

    def test_positive_propositionset_unicode(self):
        self.assertEquals("set([dest_city(london), dest_city(paris)])", unicode(self.positive_prop_set))

    def test_negative_propositionset_unicode(self):
        self.assertEquals("~set([dest_city(london), dest_city(paris)])", unicode(self.negative_prop_set))

    def test_is_understanding_proposition_false(self):
        self.assertFalse(self.positive_prop_set.is_understanding_proposition())

    def test_is_proposition_set(self):
        self.assertTrue(self.positive_prop_set.is_proposition_set())
        self.assertFalse(self.buy_action.is_proposition_set())

    def test_get_predicate(self):
        self.assertEquals(self.predicate_dest_city, self.positive_prop_set.getPredicate())

    def test_repr(self):
        self.assertEquals(
            "PropositionSet([PredicateProposition("
            "Predicate('dest_city', CustomSort('city', True), None, False), "
            "Individual('london', CustomSort('city', True)), "
            "u'POS', False), "
            "PredicateProposition("
            "Predicate('dest_city', CustomSort('city', True), None, False), "
            "Individual('paris', CustomSort('city', True)"
            "), u'POS', False)], u'POS')", repr(self.positive_prop_set)
        )

    def test_is_ontology_specific_with_some_ontology_specific_propositions(self):
        self.given_proposition_set_with([
            self._create_mocked_ontology_specific_proposition("an ontology"),
            self._create_mocked_proposition(),
        ])
        self.when_retrieving_is_ontology_specific()
        self.then_result_is(False)

    def _create_mocked_ontology_specific_proposition(self, ontology_name):
        mock = Mock(spec=PreconfirmationProposition)
        mock.is_ontology_specific.return_value = True
        mock.ontology_name = ontology_name
        return mock

    def _create_mocked_proposition(self):
        mock = Mock(spec=Proposition)
        mock.is_ontology_specific.return_value = False
        return mock

    def given_proposition_set_with(self, propositions):
        self._proposition_set = PropositionSet(propositions)

    def when_retrieving_is_ontology_specific(self):
        self._actual_result = self._proposition_set.is_ontology_specific()

    def test_is_ontology_specific_with_only_ontology_specific_propositions_of_different_ontologies(self):
        self.given_proposition_set_with([
            self._create_mocked_ontology_specific_proposition("an ontology"),
            self._create_mocked_ontology_specific_proposition("another ontology"),
        ])
        self.when_retrieving_is_ontology_specific()
        self.then_result_is(False)

    def test_is_ontology_specific_with_only_ontology_specific_propositions_of_same_ontologies(self):
        self.given_proposition_set_with([
            self._create_mocked_ontology_specific_proposition("an ontology"),
            self._create_mocked_ontology_specific_proposition("an ontology"),
        ])
        self.when_retrieving_is_ontology_specific()
        self.then_result_is(True)

    def test_is_ontology_specific_with_no_ontology_specific_propositions(self):
        self.given_proposition_set_with([
            self._create_mocked_proposition(),
            self._create_mocked_proposition(),
        ])
        self.when_retrieving_is_ontology_specific()
        self.then_result_is(False)

    def test_is_ontology_specific_without_propositions(self):
        self.given_proposition_set_with([])
        self.when_retrieving_is_ontology_specific()
        self.then_result_is(False)


class ServiceActionTerminatedTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.service_action = "MakeReservation"
        self.done = ServiceActionTerminatedProposition(self.ontology_name, self.service_action)

    def test_done_proposition_is_done_prop(self):
        self.assertTrue(self.done.is_service_action_terminated_proposition())

    def test_done_proposition_contains_action(self):
        self.assertEquals(self.service_action, self.done.get_service_action())

    def test_done_proposition_equality(self):
        identical_done_prop = ServiceActionTerminatedProposition(self.ontology_name, self.service_action)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(identical_done_prop, self.done)

    def test_done_proposition_inequality(self):
        inequal_done_prop = ServiceActionTerminatedProposition(self.ontology_name, "hskjhs")
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(inequal_done_prop, self.done)

    def test_done_proposition_unicode(self):
        expected_str = "service_action_terminated(MakeReservation)"
        self.assertEquals(expected_str, unicode(self.done))

    def test_hashing(self):
        set([self.done])

    def test_repr(self):
        self.assertEquals(
            "ServiceActionTerminatedProposition('mockup_ontology', 'MakeReservation', u'POS')", repr(self.done)
        )


class RejectionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.rejected_combination = PropositionSet([self.proposition_dest_city_paris])
        self.rejected = RejectedPropositions(self.rejected_combination)

    def test_rejected_proposition_is_rejected_prop(self):
        self.assertTrue(self.rejected.is_rejected_proposition())

    def test_creation_with_reason(self):
        reason = "ssdlfkjslkf"
        rejected = RejectedPropositions(self.rejected_combination, reason=reason)
        self.assertEquals(self.rejected_combination, rejected.get_rejected_combination())
        self.assertEquals(reason, rejected.get_reason())

    def test_rejected_with_reason_unicode(self):
        reason = "ssdlfkjslkf"
        rejected = RejectedPropositions(self.rejected_combination, reason=reason)
        string = "rejected(%s, %s)" % (self.rejected_combination, reason)
        self.assertEquals(string, unicode(rejected))

    def test_get_rejected_combination(self):
        self.assertEquals(self.rejected_combination, self.rejected.get_rejected_combination())

    def test_rejected_proposition_unicode(self):
        rejected_as_string = "rejected(%s)" % self.rejected_combination
        self.assertEquals(rejected_as_string, unicode(self.rejected))

    def test_equality(self):
        identical_rejected_prop = RejectedPropositions(PropositionSet([self.proposition_dest_city_paris]))
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(identical_rejected_prop, self.rejected)

    def test_inequality_due_to_rejected_combination(self):
        other_combination = "hskjhs"
        inequal_rejected_prop = RejectedPropositions(PropositionSet(other_combination))
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(inequal_rejected_prop, self.rejected)

    def test_inequality_due_to_reason(self):
        inequal_rejected_prop = RejectedPropositions(self.rejected_combination, reason="some_reason")
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(inequal_rejected_prop, self.rejected)


class PrereportPropositionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.service_action = "MakeReservation"
        self.empty_arguments = []
        self.prereport = self._create_with_empty_param_list()

    def _create_with_empty_param_list(self):
        confirmation_proposition = PrereportProposition(self.ontology_name, self.service_action, self.empty_arguments)
        return confirmation_proposition

    def test_type(self):
        self.assertTrue(self.prereport.is_prereport_proposition())

    def test_get_service_action(self):
        self.assertEquals(self.service_action, self.prereport.get_service_action())

    def test_get_arguments(self):
        self.assertEquals(self.empty_arguments, self.prereport.get_arguments())

    def test_proposition_unicode(self):
        self.assertEquals("prereported(MakeReservation, [])", unicode(self.prereport))

    def test_equality(self):
        identical_prereport = PrereportProposition(self.ontology_name, self.service_action, self.empty_arguments)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.prereport, identical_prereport)

    def test_inequality_due_to_action(self):
        other_action = "CacelTransaction"
        non_identical_proposition = PrereportProposition(self.ontology_name, other_action, self.empty_arguments)
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.prereport, non_identical_proposition)


class PreconfirmationTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.service_action = "MakeReservation"
        self.arguments = [self.proposition_dest_city_paris, self.proposition_dept_city_london]
        self.preconfirmation = PreconfirmationProposition(self.ontology_name, self.service_action, self.arguments)

    def test_type(self):
        self.assertTrue(self.preconfirmation.is_preconfirmation_proposition())

    def test_get_service_action(self):
        self.assertEquals(self.service_action, self.preconfirmation.get_service_action())

    def test_get_arguments(self):
        self.assertEquals(self.arguments, self.preconfirmation.get_arguments())

    def test_positive_proposition_unicode(self):
        self.assertEquals(
            "preconfirmed(MakeReservation, [dest_city(paris), dept_city(london)])", unicode(self.preconfirmation)
        )

    def test_negative_proposition_unicode(self):
        negative_preconfirmation = self.preconfirmation.negate()
        self.assertEquals(
            "~preconfirmed(MakeReservation, [dest_city(paris), dept_city(london)])", unicode(negative_preconfirmation)
        )

    def test_equality(self):
        identical_preconfirmation = PreconfirmationProposition(self.ontology_name, self.service_action, self.arguments)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.preconfirmation, identical_preconfirmation)

    def test_inequality_due_to_other_class(self):
        object_of_other_class = ServiceActionTerminatedProposition(self.ontology_name, self.service_action)
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.preconfirmation, object_of_other_class)

    def test_inequality_due_to_action(self):
        other_action = "CancelTransaction"
        non_identical_proposition = PreconfirmationProposition(self.ontology_name, other_action, self.arguments)
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.preconfirmation, non_identical_proposition)

    def test_inequality_due_to_polarity(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            self.preconfirmation, self.preconfirmation.negate()
        )

    def test_inequality_due_to_arguments_in_other_order(self):
        other_arguments = [self.proposition_dept_city_london, self.proposition_dest_city_paris]
        other_preconfirmation = PreconfirmationProposition(self.ontology_name, self.service_action, other_arguments)
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.preconfirmation, other_preconfirmation)

    def test_default_polarity_is_positive(self):
        self.assertTrue(self.preconfirmation.is_positive())

    def test_is_positive_false_for_negative_proposition(self):
        self.assertFalse(self.preconfirmation.negate().is_positive())

    def test_hashable(self):
        set([self.preconfirmation])


class ResolvednessPropositionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.issue = self.price_question
        self.proposition = ResolvednessProposition(self.issue)

    def test_get_issue(self):
        self.assertEquals(self.issue, self.proposition.get_issue())

    def test_unicode(self):
        self.assertEquals("resolved(?X.price(X))", unicode(self.proposition))

    def test_equality(self):
        identical_proposition = ResolvednessProposition(self.issue)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.proposition, identical_proposition)

    def test_inequality_due_to_issue(self):
        other_issue = self.dest_city_question
        non_identical_proposition = ResolvednessProposition(other_issue)
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.proposition, non_identical_proposition)

    def test_hashable(self):
        set([self.proposition])


class QuestionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()

    def test_is_preconfirmation_question_true_for_yes_no_questions_about_confirmation(self):
        preconfirmation_question = YesNoQuestion(
            PreconfirmationProposition(self.ontology_name, "mockup_service_action", [])
        )
        self.assertTrue(preconfirmation_question.is_preconfirmation_question())

    def test_is_preconfirmation_question_false_for_yes_no_questions_about_non_preconfirmations(self):
        non_preconfirmation_question = YesNoQuestion(self.proposition_dest_city_paris)
        self.assertFalse(non_preconfirmation_question.is_preconfirmation_question())

    def test_is_preconfirmation_question_false_for_non_yes_no_questions(self):
        self.assertFalse(self.dest_city_question.is_preconfirmation_question())


class PredicatePropositionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()

    def test_getters(self):
        self.assertEquals(self.predicate_dest_city, self.proposition_dest_city_paris.getPredicate())
        self.assertEquals(self.individual_paris, self.proposition_dest_city_paris.getArgument())

    def test_positive_unicode(self):
        self.assertEquals("dest_city(paris)", unicode(self.proposition_dest_city_paris))

    def test_negative_unicode(self):
        self.assertEquals("~dest_city(paris)", unicode(self.proposition_not_dest_city_paris))

    def test_equality(self):
        proposition = self.proposition_dest_city_paris
        identical_proposition = copy.copy(self.proposition_dest_city_paris)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(proposition, identical_proposition)

    def test_inequality_due_to_individual(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            self.proposition_dest_city_paris, self.proposition_dest_city_london
        )

    def test_inequality_due_to_polarity(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            self.proposition_dest_city_paris, self.proposition_not_dest_city_paris
        )

    def test_default_polarity_is_positive(self):
        proposition = PredicateProposition(self.predicate_dest_city, self.individual_paris)
        self.assertTrue(proposition.is_positive())

    def test_default_polarity_is_positive_with_help_method(self):
        proposition = PredicateProposition(self.predicate_dest_city, self.individual_paris)
        self.assertTrue(proposition.is_positive())

    def test_negative_proposition(self):
        proposition = PredicateProposition(self.predicate_dest_city, self.individual_paris, Polarity.NEG)
        self.assertFalse(proposition.is_positive())

    def test_create_illegal_proposition(self):
        with self.assertRaises(OntologyError):
            predicate = self.ontology.get_predicate("destination")
            individual = self.ontology.create_individual("car")
            PredicateProposition(predicate, individual)

    def test_getPredicate(self):
        self.assertEquals("dest_city", self.proposition_dest_city_paris.getPredicate().get_name())

    def test_getArgument(self):
        self.assertEquals("paris", self.proposition_dest_city_paris.getArgument().getValue())

    def test_hashable(self):
        set([self.proposition_dest_city_paris])

    def test_nullary(self):
        proposition = PredicateProposition(self.predicate_need_visa)
        self.assertEquals(None, proposition.getArgument())
        self.assertEquals("need_visa", unicode(proposition))

    def test_is_predicate_proposition_true(self):
        self.assertTrue(self.proposition_dest_city_paris.is_predicate_proposition())

    def test_is_predicate_proposition_false(self):
        self.assertFalse(self.individual_paris.is_predicate_proposition())

    def test_predicate_proposition_with_sortal_mismatch_yields_exception(self):
        individual_of_wrong_type = self.ontology.create_individual("paris")
        with self.assertRaises(OntologyError):
            PredicateProposition(self.predicate_price, individual_of_wrong_type)


class GoalPropositionTests(LibTestCase):
    def setUp(self):
        self.setUpLibTestCase()
        self.proposition = GoalProposition(PerformGoal(self.buy_action))
        self.negative_proposition = GoalProposition(PerformGoal(self.buy_action), polarity=Polarity.NEG)

    def test_equality(self):
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(
            GoalProposition(PerformGoal(self.buy_action)), GoalProposition(PerformGoal(self.buy_action))
        )

    def test_inequality_due_to_goal(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            GoalProposition(PerformGoal(self.buy_action)), GoalProposition(PerformGoal(self.top_action))
        )

    def test_inequality_due_to_polarity(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            GoalProposition(PerformGoal(self.buy_action), polarity=Polarity.POS),
            GoalProposition(PerformGoal(self.buy_action), polarity=Polarity.NEG)
        )

    def test_hashable(self):
        set([self.proposition])

    def test_positive_proposition_unicode(self):
        self.assertEquals("goal(perform(buy))", unicode(self.proposition))

    def test_negative_proposition_unicode(self):
        self.assertEquals("~goal(perform(buy))", unicode(self.negative_proposition))


class StringPropositionTests(LibTestCase):
    def setUp(self):
        self._create_ontology()

    def _create_ontology(self):
        self.ontology_name = "mockup_ontology"
        predicates = set([self._create_predicate("number_to_call", StringSort())])
        sorts = set([])
        individuals = {}
        actions = set([])
        self.ontology = Ontology(self.ontology_name, sorts, predicates, individuals, actions)

    def test_str_with_string_argument(self):
        predicate_number_to_call = self.ontology.get_predicate("number_to_call")
        individual = self.ontology.create_individual('"123"')
        string_proposition = PredicateProposition(predicate_number_to_call, individual)
        self.assertEquals('number_to_call("123")', unicode(string_proposition))


class ImagePropositionTests(LibTestCase):
    def setUp(self):
        self._create_ontology()

    def _create_ontology(self):
        self.ontology_name = "mockup_ontology"
        predicates = set([self._create_predicate("map_to_show", ImageSort())])
        sorts = set([])
        individuals = {}
        actions = set([])
        self.ontology = Ontology(self.ontology_name, sorts, predicates, individuals, actions)

    def test_str_with_string_argument(self):
        map_to_show = self.ontology.get_predicate("map_to_show")
        individual = self.ontology.create_individual(Image("http://mymap.com/map.png"))
        image_proposition = PredicateProposition(map_to_show, individual)
        self.assertEquals(u'map_to_show(image("http://mymap.com/map.png"))', unicode(image_proposition))
