import copy

from tala.model.domain import Domain
from tala.model.goal import ResolveGoal, PerformGoal, HandleGoal
from tala.model.lambda_abstraction import LambdaAbstractedPredicateProposition
from tala.model.speaker import Speaker
from tala.model.set import Set
from tala.model.ontology import Ontology
from tala.model.plan import Plan, InvalidPlansException
from tala.model.plan_item import BindPlanItem, IfThenElse, InvokeServiceActionPlanItem
from tala.model.polarity import Polarity
from tala.model.proposition import PredicateProposition, GoalProposition, PropositionSet, ServiceActionTerminatedProposition
from tala.model.question import WhQuestion, AltQuestion
from tala.model.question_raising_plan_item import QuestionRaisingPlanItem, FindoutPlanItem, RaisePlanItem
from tala.model.sort import CustomSort, RealSort
from tala.testing.lib_test_case import LibTestCase


class DomainTests(LibTestCase):
    def setUp(self):
        self.ontology_name = "mockup_ontology"
        self._city_sort = CustomSort(self.ontology_name, "city", dynamic=True)
        self.setUpDomainTestCase()

    def setUpDomainTestCase(self):
        self._create_ontologies()
        self._create_semantic_objects()
        self._create_domains()

    def _create_ontologies(self):
        sorts = {
            CustomSort(self.ontology_name, "country"),
            self._city_sort,
            CustomSort(self.ontology_name, "city_type"),
        }
        predicates = {
            self._create_predicate("dest_city", self._city_sort),
            self._create_predicate("dept_city", self._city_sort),
            self._create_predicate("dest_country", CustomSort(self.ontology_name, "country")),
            self._create_predicate("price", RealSort()),
            self._create_predicate("code", RealSort()),
            self._create_predicate(
                "dest_city_type", sort=CustomSort(self.ontology_name, "city_type"), feature_of_name="dest_city"
            )
        }
        individuals = {
            "paris": self._city_sort,
            "london": self._city_sort,
        }
        self.actions = {
            "top",
            "buy",
            "always_preferred",
            "conditionally_preferred",
            "planless",
            "with_context",
            "with_dynamic_title",
            "accommodate_unrestricted",
            "downdate_plan_true",
            "downdate_plan_false",
            "event",
        }
        self.ontology = Ontology(self.ontology_name, sorts, predicates, individuals, self.actions)

        self.empty_ontology = Ontology("empty_ontology", {}, {}, {}, set([]))

    def _create_semantic_objects(self):
        self.predicate_dest_city = self.ontology.get_predicate("dest_city")
        self.predicate_dest_city_type = self.ontology.get_predicate("dest_city_type")
        self.predicate_dept_city = self.ontology.get_predicate("dept_city")
        self.predicate_price = self.ontology.get_predicate("price")
        self.predicate_dest_country = self.ontology.get_predicate("dest_country")
        self.predicate_code = self.ontology.get_predicate("code")

        self.lambda_abstracted_price_prop = LambdaAbstractedPredicateProposition(
            self.predicate_price, self.ontology_name
        )
        self.lambda_abstracted_dest_city_prop = LambdaAbstractedPredicateProposition(
            self.predicate_dest_city, self.ontology_name
        )
        self.lambda_abstracted_dest_city_type_prop = LambdaAbstractedPredicateProposition(
            self.predicate_dest_city_type, self.ontology_name
        )
        self.lambda_abstracted_dept_city_prop = LambdaAbstractedPredicateProposition(
            self.predicate_dept_city, self.ontology_name
        )

        self.price_question = WhQuestion(self.lambda_abstracted_price_prop)
        self.dest_city_question = WhQuestion(self.lambda_abstracted_dest_city_prop)
        self.dest_city_type_question = WhQuestion(self.lambda_abstracted_dest_city_type_prop)
        self.dept_city_question = WhQuestion(self.lambda_abstracted_dept_city_prop)
        self.dest_country_question = WhQuestion(
            LambdaAbstractedPredicateProposition(self.predicate_dest_country, self.ontology_name)
        )

        self.individual_paris = self.ontology.create_individual("paris")
        self.individual_london = self.ontology.create_individual("london")
        self.proposition_dest_city_paris = PredicateProposition(self.predicate_dest_city, self.individual_paris)
        self.proposition_dest_city_london = PredicateProposition(self.predicate_dest_city, self.individual_london)
        self.proposition_not_dest_city_paris = PredicateProposition(
            self.predicate_dest_city, self.individual_paris, Polarity.NEG
        )

    def _create_domains(self):
        self.domain_name = "mockup_domain"

        self._create_actions()
        self._create_questions()
        self.condition = self.proposition_dest_city_paris
        plans = self._create_plans()

        dependencies = {self.dest_country_question: {self.dest_city_question}}

        self.non_verbalized_question = self.dest_city_question

        parameters = {
            self.non_verbalized_question: {
                "verbalize": False
            },
        }

        self.domain = Domain(
            self.DDD_NAME,
            self.domain_name,
            self.ontology,
            plans=plans,
            default_questions=[self.dest_city_question],
            dependencies=dependencies,
            parameters=parameters
        )

        self.empty_domain = Domain(self.DDD_NAME, "empty_domain", self.empty_ontology)

    def _create_actions(self):
        for action_name in self.actions:
            action = self.ontology.create_action(action_name)
            attribute_name = action_name + "_action"
            setattr(self, attribute_name, action)
        self.up_action = self.ontology.create_action("up")

    def _create_questions(self):
        for predicate_name in ["dest_city", "dept_city", "code"]:
            question = self.ontology.create_wh_question(predicate_name)
            attribute_name = predicate_name + "_question"
            setattr(self, attribute_name, question)

    def _create_plans(self):
        return [{
            "goal":
            ResolveGoal(self.price_question, Speaker.SYS),
            "plan":
            Plan([
                FindoutPlanItem(self.domain_name, self.dest_city_question),
                FindoutPlanItem(self.domain_name, self.dept_city_question),
            ]),
            "gui_context": [
                self.predicate_dest_city,
                self.predicate_dept_city,
            ]
        },
                {
                    "goal": PerformGoal(self.buy_action),
                    "plan": Plan([FindoutPlanItem(self.domain_name, self.price_question)]),
                    "postconds": [self.condition]
                },
                {
                    "goal": PerformGoal(self.always_preferred_action),
                    "preferred": True,
                    "plan": Plan([]),
                    "postplan": [FindoutPlanItem(self.domain_name, self.price_question)],
                    "superactions": [self.buy_action]
                },
                {
                    "goal": PerformGoal(self.conditionally_preferred_action),
                    "preferred": self.condition,
                    "plan": Plan([])
                },
                {
                    "goal": PerformGoal(self.with_context_action),
                    "plan": Plan([]),
                    "gui_context": [self.predicate_dest_city]
                },
                {
                    "goal": PerformGoal(self.with_dynamic_title_action),
                    "plan": Plan([]),
                    "dynamic_title": True,
                    "gui_context": [self.predicate_dest_city]
                },
                {
                    "goal": PerformGoal(self.accommodate_unrestricted_action),
                    "plan": Plan([]),
                    "unrestricted_accommodation": True,
                },
                {
                    "goal":
                    PerformGoal(self.downdate_plan_true_action),
                    "plan":
                    Plan([InvokeServiceActionPlanItem("mockup_ontology", "mock_service_action", downdate_plan=True)]),
                },
                {
                    "goal":
                    PerformGoal(self.downdate_plan_false_action),
                    "plan":
                    Plan([InvokeServiceActionPlanItem("mockup_ontology", "mock_service_action", downdate_plan=False)]),
                }, {
                    "goal": HandleGoal("mockup_ontology", "event"),
                    "plan": Plan([]),
                }]

    def test_top_and_up_goals_added_implicitly_by_domain(self):
        self.given_custom_goals_without_top_and_up()
        self.when_fetching_goals_from_domain()
        self.then_top_and_up_are_included()

    def given_custom_goals_without_top_and_up(self):
        plans = self._create_plans()
        goals = [info["goal"] for info in plans]
        self.expected_goals = goals
        action_names = self._action_names_of_perform_goals(self.expected_goals)
        self.assertNotIn("top", action_names)
        self.assertNotIn("up", action_names)

    def when_fetching_goals_from_domain(self):
        self.actual_goals = self.domain.goals

    def then_top_and_up_are_included(self):
        self.assertEqual(len(self.actual_goals), len(self.expected_goals) + 2)
        action_names = self._action_names_of_perform_goals(self.actual_goals)
        self.assertIn("top", action_names)
        self.assertIn("up", action_names)

    def _action_names_of_perform_goals(self, goals):
        actions_of_perform_goals = [goal.get_content() for goal in goals if goal.is_perform_goal()]
        action_names = [action.value for action in actions_of_perform_goals]
        return action_names

    def test_domain_equality(self):
        identical_domain = copy.copy(self.domain)
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(self.domain, identical_domain)

    def test_domain_inequality(self):
        non_identical_domain = self.empty_domain
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(self.domain, non_identical_domain)

    def test_get_name(self):
        self.assertEquals("mockup_domain", self.domain.get_name())

    def test_action_method(self):
        self.assertEquals(self.buy_action, self.domain.action("buy"))

    def test_has_goal_true_for_question_with_plan(self):
        self.assertTrue(self.domain.has_goal(ResolveGoal(self.price_question, Speaker.SYS)))

    def test_has_goal_false_for_question_without_plan(self):
        question_without_plan = self.dest_city_question
        self.assertFalse(self.domain.has_goal(ResolveGoal(question_without_plan, Speaker.USR)))

    def test_has_goal_true_for_action_with_plan(self):
        self.assertTrue(self.domain.has_goal(PerformGoal(self.buy_action)))

    def test_has_goal_false_for_planless_action(self):
        self.assertFalse(self.domain.has_goal(PerformGoal(self.planless_action)))

    def test_up_plan_empty(self):
        self.assertEquals(0, len(self.domain.get_plan(PerformGoal(self.up_action))))

    def test_goal_is_preferred_true_if_plan_always_preferred(self):
        self.assertTrue(self.domain.goal_is_preferred(PerformGoal(self.always_preferred_action)))

    def test_goal_is_preferred_false_if_plan_never_preferred(self):
        never_preferred_action = self.buy_action
        self.assertFalse(self.domain.goal_is_preferred(PerformGoal(never_preferred_action)))

    def test_goal_is_preferred_true_if_condition_in_facts(self):
        facts_with_condition = [self.condition]
        self.assertTrue(
            self.domain.goal_is_conditionally_preferred(
                PerformGoal(self.conditionally_preferred_action), facts_with_condition
            )
        )

    def test_goal_is_preferred_false_if_condition_not_in_facts(self):
        facts_without_condition = []
        self.assertFalse(
            self.domain.goal_is_conditionally_preferred(
                PerformGoal(self.conditionally_preferred_action), facts_without_condition
            )
        )

    def test_is_default_question(self):
        default_question = self.dest_city_question
        non_default_question = self.price_question
        self.assertTrue(self.domain.is_default_question(default_question))
        self.assertFalse(self.domain.is_default_question(non_default_question))

    def test_plan_can_be_silently_accommodated(self):
        silently_accommodatable_goal = PerformGoal(self.accommodate_unrestricted_action)
        self.assertTrue(self.domain.is_silently_accommodatable(silently_accommodatable_goal))

    def test_plan_with_conditionally_preferred_action_can_not_be_silently_accommodated(self):
        silently_accommodatable_goal = PerformGoal(self.conditionally_preferred_action)
        self.assertFalse(self.domain.is_silently_accommodatable(silently_accommodatable_goal))

    def test_get_plan_questions(self):
        self.maxDiff = None
        expected_questions = ["?X.dest_city(X)", "?X.dest_city_type(X)", "?X.dept_city(X)", "?X.price(X)"]
        actual_result = [question for question in self.domain.get_plan_questions()]
        actual_result_strings = map(str, actual_result)
        self.assertItemsEqual(expected_questions, actual_result_strings)

    def test_get_all_goals(self):
        expected_goals = {
            ResolveGoal(self.price_question, Speaker.SYS),
            PerformGoal(self.buy_action),
            PerformGoal(self.always_preferred_action),
            PerformGoal(self.conditionally_preferred_action),
            PerformGoal(self.with_context_action),
            PerformGoal(self.up_action),
            PerformGoal(self.with_dynamic_title_action),
            PerformGoal(self.accommodate_unrestricted_action),
            PerformGoal(self.top_action),
            PerformGoal(self.downdate_plan_true_action),
            PerformGoal(self.downdate_plan_false_action),
            HandleGoal("mockup_ontology", "event")
        }
        actual_result = set(self.domain.get_all_goals())
        self.assertEqual(expected_goals, actual_result)

    def test_get_all_goals_in_defined_order(self):
        expected_goals = [
            ResolveGoal(self.price_question, Speaker.SYS),
            PerformGoal(self.buy_action),
            PerformGoal(self.always_preferred_action),
            PerformGoal(self.conditionally_preferred_action),
            PerformGoal(self.with_context_action),
            PerformGoal(self.with_dynamic_title_action),
            PerformGoal(self.accommodate_unrestricted_action),
            PerformGoal(self.downdate_plan_true_action),
            PerformGoal(self.downdate_plan_false_action),
            HandleGoal("mockup_ontology", "event")
        ]
        actual_result = self.domain.get_all_goals_in_defined_order()
        self.assertEqual(expected_goals, actual_result)

    def test_get_dependent_question_returns_goal_issue_for_question_in_plan(self):
        self.assertEquals(self.price_question, self.domain.get_dependent_question(self.dest_city_question))

    def test_get_dependent_question_returns_none_for_goal_issue(self):
        self.assertEquals(None, self.domain.get_dependent_question(self.price_question))

    def test_iterate_plans(self):
        expected_goals = {
            ResolveGoal(self.price_question, Speaker.SYS),
            PerformGoal(self.buy_action),
            PerformGoal(self.always_preferred_action),
            PerformGoal(self.conditionally_preferred_action),
            PerformGoal(self.with_context_action),
            PerformGoal(self.up_action),
            PerformGoal(self.with_dynamic_title_action),
            PerformGoal(self.accommodate_unrestricted_action),
            PerformGoal(self.top_action),
            PerformGoal(self.downdate_plan_true_action),
            PerformGoal(self.downdate_plan_false_action),
            HandleGoal("mockup_ontology", "event")
        }
        actual_goals = set([goal for goal in self.domain.get_plan_goal_iterator()])
        self.assertEqual(expected_goals, actual_goals)

    def test_get_postconds_for_goal_with_postcond(self):
        action_with_postconds = self.buy_action
        self.assertEqual([self.condition], list(self.domain.get_postconds(PerformGoal(action_with_postconds))))

    def test_get_postconds_for_goal_without_postconds(self):
        action_without_postcond = self.always_preferred_action
        self.assertEqual([], list(self.domain.get_postconds(PerformGoal(action_without_postcond))))

    def test_get_postconds_returns_implicit_postconds_for_service_action_invocations_if_downdate_plan_is_true(self):
        self.assertEquals([ServiceActionTerminatedProposition("mockup_ontology", "mock_service_action")],
                          list(self.domain.get_postconds(PerformGoal(self.downdate_plan_true_action))))

    def test_get_postconds_doesnt_return_implicit_postconds_for_service_action_invocations_if_not_downdating_plan(self):
        self.assertEquals([], list(self.domain.get_postconds(PerformGoal(self.downdate_plan_false_action))))

    def test_get_postconds_considers_downdate_plan_property_for_handle_goals(self):
        self.assertEquals([ServiceActionTerminatedProposition("mockup_ontology", "event")],
                          list(self.domain.get_postconds(HandleGoal("mockup_ontology", "event"))))

    def test_get_postconds_for_resolve_goal(self):
        resolve_goal = ResolveGoal(self.price_question, Speaker.SYS)
        self.assertEqual([], list(self.domain.get_postconds(resolve_goal)))

    def test_get_postplan_for_goal_with_postplan(self):
        action_with_postplan = self.always_preferred_action
        postplan = self.domain.get_postplan(PerformGoal(action_with_postplan))
        expected_postplan = [FindoutPlanItem(self.domain_name, self.price_question)]
        self.assertEqual(expected_postplan, postplan)

    def test_get_postplan_for_goal_without_postplan(self):
        action_without_postplan = self.buy_action
        self.assertEqual([], self.domain.get_postplan(PerformGoal(action_without_postplan)))

    def test_get_superactions_for_goal_with_superactions(self):
        action_with_superactions = self.always_preferred_action
        expected_result = [self.buy_action]
        self.assertEqual(expected_result, self.domain.get_superactions(PerformGoal(action_with_superactions)))

    def test_get_superactions_for_goal_without_superactions(self):
        action_without_superactions = self.buy_action
        self.assertEqual([], self.domain.get_superactions(PerformGoal(action_without_superactions)))

    def test_is_depending_on_true_for_goal_issue_wrt_question_in_its_plan(self):
        goal_issue = self.price_question
        question_in_plan = self.dest_city_question
        self.assertTrue(self.domain.is_depending_on(goal_issue, question_in_plan))

    def test_is_depending_on_false_for_plan_question_wrt_its_goal_issue(self):
        goal_issue = self.price_question
        question_in_plan = self.dest_city_question
        self.assertFalse(self.domain.is_depending_on(question_in_plan, goal_issue))

    def test_is_depending_on_true_due_to_domain_declaration(self):
        self.assertTrue(self.domain.is_depending_on(self.dest_country_question, self.dest_city_question))

    def test_is_depending_on_false_for_inverse_domain_declaration(self):
        self.assertFalse(self.domain.is_depending_on(self.dest_city_question, self.dest_country_question))

    def test_is_depending_on_true_because_of_featurehood(self):
        self.assertTrue(self.domain.is_depending_on(self.dest_city_question, self.dest_city_type_question))

    def test_is_depending_on_robust_to_non_sortal_questions(self):
        city_prop_set = PropositionSet([
            self.proposition_dest_city_london,
            self.proposition_dest_city_paris,
        ])
        non_sortal_question = AltQuestion(city_prop_set)

        self.domain.is_depending_on(non_sortal_question, non_sortal_question)

    def test_get_gui_context_for_issue_goal_with_context(self):
        expected_result = [self.predicate_dest_city, self.predicate_dept_city]
        self.assertEquals(expected_result, self.domain.get_gui_context(ResolveGoal(self.price_question, Speaker.SYS)))

    def test_goal_with_dynamic_title_has_dynamic_title(self):
        self.assertTrue(self.domain.has_dynamic_title(PerformGoal(self.with_dynamic_title_action)))

    def test_goal_without_dynamic_title_has_no_dynamic_title(self):
        self.assertFalse(self.domain.has_dynamic_title(PerformGoal(self.with_context_action)))

    def test_get_gui_context_for_action_goal_with_context(self):
        expected_result = [self.predicate_dest_city]
        self.assertEquals(expected_result, self.domain.get_gui_context(PerformGoal(self.with_context_action)))

    def test_get_gui_context_for_goal_without_context(self):
        expected_result = []
        goal_without_context = self.buy_action
        self.assertEquals(expected_result, self.domain.get_gui_context(PerformGoal(goal_without_context)))

    def test_get_resolving_answers(self):
        question = self.dest_city_question
        expected_answers = [self.proposition_dest_city_paris, self.proposition_dest_city_london]
        self.assertEqual(set(expected_answers), set(self.domain.get_resolving_answers(question)))

    def test_question_presented_as_list_forces_graphical_choice(self):
        self.domain.parameters[self.dest_city_question] = {
            "graphical_type": QuestionRaisingPlanItem.GRAPHICAL_TYPE_LIST
        }
        self.assertTrue(self.domain.question_forces_graphical_choice(self.dest_city_question))

    def test_question_presented_as_text_forces_graphical_choice(self):
        self.domain.parameters[self.dest_city_question] = {
            "graphical_type": QuestionRaisingPlanItem.GRAPHICAL_TYPE_TEXT
        }
        self.assertTrue(self.domain.question_forces_graphical_choice(self.dest_city_question))

    def test_incremental_question_does_not_force_graphical_choice(self):
        self.domain.parameters[self.dest_city_question] = {"incremental": True}
        self.assertFalse(self.domain.question_forces_graphical_choice(self.dest_city_question))

    def test_get_question_verbalize_returns_true_by_default(self):
        question_with_verbalize_unspecified = self.price_question
        self.assertTrue(self.domain.get_verbalize(question_with_verbalize_unspecified))

    def test_get_question_verbalize_returns_false_when_specified_as_false(self):
        self.assertFalse(self.domain.get_verbalize(self.non_verbalized_question))

    def test_empty_top_plan_by_default(self):
        self.assertEquals(Plan([]), self.domain.get_plan(PerformGoal(self.top_action)))

    def test_multiple_plans_for_same_goal_yields_exception(self):
        invalid_plans = [
            {
                "goal": PerformGoal(self.top_action),
                "plan": Plan([])
            },
            {
                "goal": PerformGoal(self.top_action),
                "plan": Plan([])
            },
        ]

        with self.assertRaises(InvalidPlansException):
            Domain(self.DDD_NAME, self.domain_name, self.ontology, invalid_plans)

    def test_get_questions_in_plan_base_case(self):
        plan = Plan([
            FindoutPlanItem(self.domain_name, self.price_question),
            RaisePlanItem(self.domain_name, self.dest_city_question)
        ])
        expected_questions = [self.price_question, self.dest_city_question, self.dest_city_type_question]
        actual_result = [question for question in self.domain.get_questions_in_plan(plan)]
        self.assertEqual(set(expected_questions), set(actual_result))

    def test_get_questions_in_plan_supports_if_then_else(self):
        arbitrary_condition = self.proposition_dest_city_paris
        plan = Plan([
            IfThenElse(
                arbitrary_condition, FindoutPlanItem(self.domain_name, self.price_question),
                BindPlanItem(self.dest_city_question)
            )
        ])
        expected_questions = [self.price_question, self.dest_city_question, self.dest_city_type_question]
        actual_result = [question for question in self.domain.get_questions_in_plan(plan)]
        self.assertEqual(set(expected_questions), set(actual_result))

    def test_get_questions_in_plan_include_features(self):
        plan = Plan([FindoutPlanItem(self.domain_name, self.dest_city_question)])
        expected_questions = [self.dest_city_question, self.dest_city_type_question]
        actual_result = [question for question in self.domain.get_questions_in_plan(plan)]
        self.assertEqual(set(expected_questions), set(actual_result))


class DominatesTests(LibTestCase):
    def setUp(self):
        self.ontology_name = "mockup_ontology"
        actions = {
            "dominating_action", "dominated_action", "super_dominated_action", "non_dominated_action", "planless_action"
        }
        sorts = set([])
        predicates = {
            self._create_predicate("dominated_issue", RealSort()),
            self._create_predicate("non_dominated_issue", RealSort())
        }
        individuals = {}
        self.ontology_name = "mockup_ontology"
        self.ontology = Ontology(self.ontology_name, sorts, predicates, individuals, actions)

        self.domain_name = "mockup_domain"
        self.DDD_NAME = "mock_ddd"

        for action_name in actions:
            action = self.ontology.create_action(action_name)
            setattr(self, action_name, action)

        for question_name in ["dominated_issue", "non_dominated_issue"]:
            question = self.ontology.create_wh_question(question_name)
            setattr(self, question_name, question)

        plans = [{
            "goal":
            PerformGoal(self.dominating_action),
            "plan": [
                self._findout_with_alts([
                    GoalProposition(PerformGoal(self.dominated_action)),
                    GoalProposition(ResolveGoal(self.dominated_issue, Speaker.SYS))
                ])
            ]
        },
                 {
                     "goal": PerformGoal(self.dominated_action),
                     "plan": [self._findout_with_alts([GoalProposition(PerformGoal(self.super_dominated_action))])]
                 }, {
                     "goal": PerformGoal(self.super_dominated_action),
                     "plan": []
                 }, {
                     "goal": ResolveGoal(self.dominated_issue, Speaker.SYS),
                     "plan": []
                 }, {
                     "goal": PerformGoal(self.non_dominated_action),
                     "plan": []
                 }]

        self.domain = Domain(self.DDD_NAME, self.domain_name, self.ontology, plans=plans)

    def test_dominates_true_for_dominated_action(self):
        self.assertTrue(self.domain.dominates(PerformGoal(self.dominating_action), PerformGoal(self.dominated_action)))

    def test_dominates_true_for_super_dominated_action(self):
        self.assertTrue(
            self.domain.dominates(PerformGoal(self.dominating_action), PerformGoal(self.super_dominated_action))
        )

    def test_dominates_true_for_dominated_issue(self):
        self.assertTrue(
            self.domain.dominates(PerformGoal(self.dominating_action), ResolveGoal(self.dominated_issue, Speaker.SYS))
        )

    def test_dominates_false_for_non_dominated_action(self):
        self.assertFalse(
            self.domain.dominates(PerformGoal(self.dominating_action), PerformGoal(self.non_dominated_action))
        )

    def test_dominates_false_for_non_dominated_issue(self):
        self.assertFalse(
            self.domain.dominates(
                PerformGoal(self.dominating_action), ResolveGoal(self.non_dominated_issue, Speaker.SYS)
            )
        )

    def test_dominates_false_for_action_without_plan(self):
        self.assertFalse(self.domain.dominates(PerformGoal(self.planless_action), PerformGoal(self.dominated_action)))

    def _findout_with_alts(self, alts):
        return FindoutPlanItem(self.domain_name, AltQuestion(PropositionSet(alts)))


class IOStatusTests(LibTestCase):
    def setUp(self):
        self.DDD_NAME = "mockup_ddd"
        self.statuses = ["default", "excluded", "hidden", "silent", "disabled"]
        self.facts = Set()
        self._create_ontology()
        self._create_domain()

    def _create_ontology(self):
        self.ontology_name = "status_ontology"
        sorts = set([])
        predicates = set([])
        individuals = {}
        actions = set(self.statuses)
        self.ontology = Ontology(self.ontology_name, sorts, predicates, individuals, actions)

    def _create_domain(self):
        self.domain_name = "status_domain"

        for status in self.statuses:
            action = self.ontology.create_action(status)
            attribute_name = status + "_action"
            setattr(self, attribute_name, action)

        plans = [{
            "goal": PerformGoal(self.default_action),
            "plan": []
        }, {
            "goal": PerformGoal(self.excluded_action),
            "io_status": "excluded",
            "plan": []
        }, {
            "goal": PerformGoal(self.hidden_action),
            "io_status": "hidden",
            "plan": []
        }, {
            "goal": PerformGoal(self.silent_action),
            "io_status": "silent",
            "plan": []
        }, {
            "goal": PerformGoal(self.disabled_action),
            "io_status": "disabled",
            "plan": []
        }]

        self.domain = Domain(self.DDD_NAME, self.domain_name, self.ontology, plans=plans)

    def test_io_status_for_default_plan(self):
        self.assertEquals(Domain.DEFAULT_IO_STATUS, self.domain.get_io_status(PerformGoal(self.default_action)))

    def test_io_status_for_excluded_plan(self):
        self.assertEquals(Domain.EXCLUDED_IO_STATUS, self.domain.get_io_status(PerformGoal(self.excluded_action)))

    def test_io_status_for_hidden_plan(self):
        self.assertEquals(Domain.HIDDEN_IO_STATUS, self.domain.get_io_status(PerformGoal(self.hidden_action)))

    def test_io_status_for_silent_plan(self):
        self.assertEquals(Domain.SILENT_IO_STATUS, self.domain.get_io_status(PerformGoal(self.silent_action)))

    def test_io_status_for_disabled_plan(self):
        self.assertEquals(Domain.DISABLED_IO_STATUS, self.domain.get_io_status(PerformGoal(self.disabled_action)))
