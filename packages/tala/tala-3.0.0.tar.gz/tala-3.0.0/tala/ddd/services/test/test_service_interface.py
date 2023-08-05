import unittest

import pytest
from mock import Mock

from tala.ddd.services.service_interface import ServiceActionInterface, DeviceModuleTarget, ServiceInterface, UnexpectedActionException, ServiceQueryInterface, ServiceValidatorInterface, ServiceEntityRecognizerInterface, DuplicateNameException, PlayAudioActionInterface, AudioURLServiceParameter, FrontendTarget, HttpTarget, FailureReasonsNotAllowedException, ActionFailureReason, UnsupportedServiceInterfaceTarget
from tala.testing.utils import EqualityAssertionTestCaseMixin


class ServiceInterfaceTests(unittest.TestCase):
    def setUp(self):
        self._play_audio_actions = []
        self._custom_actions = []
        self._queries = []
        self._validators = []
        self._entity_recognizers = []
        self._mocked_target = self._create_mocked_target()
        self._mocked_audio_url_parameter = Mock(spec=AudioURLServiceParameter)
        self._service_interface = None
        self._result = None

    def _create_mocked_target(self):
        mocked_target = Mock(spec=DeviceModuleTarget)
        mocked_target.is_frontend = False
        return mocked_target

    def test_has_play_audio_action_when_action_exists(self):
        self._given_play_audio_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_has_action("mocked_action")
        self._then_result_is(True)

    def _create_play_audio_action(self, name):
        return PlayAudioActionInterface(
            name, FrontendTarget(), parameters=[], audio_url_parameter=self._mocked_audio_url_parameter
        )

    def _given_play_audio_actions(self, names):
        self._play_audio_actions = [self._create_play_audio_action(name) for name in names]

    def test_has_action_when_action_exists(self):
        self._given_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_has_action("mocked_action")
        self._then_result_is(True)

    def _create_action(self, name):
        return ServiceActionInterface(name, self._mocked_target, parameters=[], failure_reasons=[])

    def _given_actions(self, names):
        self._custom_actions = [self._create_action(name) for name in names]

    def _given_service_interface(self):
        self._create_service_interface()

    def _create_service_interface(self):
        actions = self._play_audio_actions + self._custom_actions
        self._service_interface = ServiceInterface(actions, self._queries, self._entity_recognizers, self._validators)

    def _when_calling_has_action(self, name):
        self._result = self._service_interface.has_action(name)

    def _then_result_is(self, expected_result):
        self.assertEqual(self._result, expected_result)

    def test_has_play_audio_action_when_action_missing(self):
        self._given_play_audio_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_has_action("another_action")
        self._then_result_is(False)

    def test_has_action_when_action_missing(self):
        self._given_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_has_action("another_action")
        self._then_result_is(False)

    def test_has_play_audio_action_when_action_exists_among_several(self):
        self._given_play_audio_actions(["mocked_action", "another_action", "third_action"])
        self._given_service_interface()
        self._when_calling_has_action("another_action")
        self._then_result_is(True)

    def test_has_action_when_action_exists_among_several(self):
        self._given_actions(["mocked_action", "another_action", "third_action"])
        self._given_service_interface()
        self._when_calling_has_action("another_action")
        self._then_result_is(True)

    def test_get_play_audio_action_when_action_exists(self):
        self._given_play_audio_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_get_action("mocked_action")
        self._then_result_is_play_audio_action("mocked_action")

    def _then_result_is_play_audio_action(self, name):
        expected_action = self._create_play_audio_action(name)
        self.assertEqual(self._result, expected_action)

    def test_get_action_when_action_exists(self):
        self._given_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_get_action("mocked_action")
        self._then_result_is_action_named("mocked_action")

    def _when_calling_get_action(self, name):
        self._result = self._service_interface.get_action(name)

    def _then_result_is_action_named(self, name):
        expected_action = self._create_action(name)
        self.assertEqual(self._result, expected_action)

    def test_get_play_audio_action_when_action_missing(self):
        self._given_play_audio_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_get_action_then_exception_is_raised_matching(
            "another_action", UnexpectedActionException,
            "Expected one of the known actions \['mocked_action'\] but got 'another_action'"
        )

    def test_get_action_when_action_missing(self):
        self._given_actions(["mocked_action"])
        self._given_service_interface()
        self._when_calling_get_action_then_exception_is_raised_matching(
            "another_action", UnexpectedActionException,
            "Expected one of the known actions \['mocked_action'\] but got 'another_action'"
        )

    def _when_calling_get_action_then_exception_is_raised_matching(self, name, expected_exception, expected_message):
        with self.assertRaisesRegexp(expected_exception, expected_message):
            self._service_interface.get_action(name)

    def test_duplicate_actions(self):
        self._given_actions(["mocked_action", "mocked_action"])
        self._when_creating_service_interface_then_exception_is_raised_matching(
            DuplicateNameException, "Expected all names to be unique among "
            "\[ServiceActionInterface\('mocked_action', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\], failure_reasons=\[\]\),"
            " ServiceActionInterface\('mocked_action', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\], failure_reasons=\[\]\)\] "
            "but they weren't"
        )

    def _when_creating_service_interface_then_exception_is_raised_matching(self, expected_exception, expected_message):
        with self.assertRaisesRegexp(expected_exception, expected_message):
            self._given_service_interface()

    def test_duplicate_queries(self):
        self._given_queries(["mocked_query", "another_query", "mocked_query"])
        self._when_creating_service_interface_then_exception_is_raised_matching(
            DuplicateNameException, "Expected all names to be unique among "
            "\[ServiceQueryInterface\('mocked_query', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\), "
            "ServiceQueryInterface\('another_query', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\), "
            "ServiceQueryInterface\('mocked_query', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\)\] "
            "but they weren't"
        )

    def _given_queries(self, names):
        self._queries = [self._create_query(name) for name in names]

    def _create_query(self, name):
        return ServiceQueryInterface(name, self._mocked_target, [])

    def test_duplicate_validators(self):
        self._given_validators(["validator", "validator", "other"])
        self._when_creating_service_interface_then_exception_is_raised_matching(
            DuplicateNameException, "Expected all names to be unique among "
            "\[ServiceValidatorInterface\('validator', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\), "
            "ServiceValidatorInterface\('validator', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\), "
            "ServiceValidatorInterface\('other', <Mock spec='DeviceModuleTarget' id='[\d]+'>, parameters=\[\]\)\] "
            "but they weren't"
        )

    def _given_validators(self, names):
        self._validators = [self._create_validator(name) for name in names]

    def _create_validator(self, name):
        return ServiceValidatorInterface(name, self._mocked_target, [])

    def test_duplicate_entity_recognizers(self):
        self._given_entity_recognizers(["a_recognizer", "recognizer", "recognizer"])
        self._when_creating_service_interface_then_exception_is_raised_matching(
            DuplicateNameException, "Expected all names to be unique among "
            "\[ServiceEntityRecognizerInterface\('a_recognizer', <Mock spec='DeviceModuleTarget' id='[\d]+'>\), "
            "ServiceEntityRecognizerInterface\('recognizer', <Mock spec='DeviceModuleTarget' id='[\d]+'>\), "
            "ServiceEntityRecognizerInterface\('recognizer', <Mock spec='DeviceModuleTarget' id='[\d]+'>\)\] "
            "but they weren't"
        )

    def _given_entity_recognizers(self, names):
        self._entity_recognizers = [self._create_entity_recognizer(name) for name in names]

    def _create_entity_recognizer(self, name):
        return ServiceEntityRecognizerInterface(name, self._mocked_target)


class ActionInterfaceTests(unittest.TestCase):
    def setUp(self):
        self._action = None
        self._result = None

    def test_action_interface(self):
        self._given_action(ServiceActionInterface("mocked_action", Mock(spec=FrontendTarget), [], []))
        self._when_asking_is_play_audio_action()
        self._then_result_is(False)

    def _given_action(self, action):
        self._action = action

    def _then_result_is(self, expected_result):
        self.assertEqual(self._result, expected_result)

    def _when_asking_is_play_audio_action(self):
        self._result = self._action.is_play_audio_action

    def test_play_audio_action_interface(self):
        self._given_action(PlayAudioActionInterface("mocked_action", Mock(spec=FrontendTarget), [], "mocked_url"))
        self._when_asking_is_play_audio_action()
        self._then_result_is(True)


class ActionInterfaceCreationTests(unittest.TestCase):
    def setUp(self):
        self._name = None
        self._target = None
        self._parameters = []
        self._failure_reasons = []
        self._result = None

    def test_failure_reasons_not_allowed_with_frontend_target(self):
        self._given_name("MockedAction")
        self._given_target(FrontendTarget())
        self._given_failure_reasons([ActionFailureReason("mocked_failure_reason")])
        self._when_creating_action_then_exception_is_raised_matching(
            FailureReasonsNotAllowedException, "Expected no failure reasons for action 'MockedAction' with target "
            "'frontend', but got \['mocked_failure_reason'\]"
        )

    def _given_name(self, name):
        self._name = name

    def _given_target(self, target):
        self._target = target

    def _given_failure_reasons(self, failure_reasons):
        self._failure_reasons = failure_reasons

    def _when_creating_action_then_exception_is_raised_matching(self, expected_exception, expected_pattern):
        with self.assertRaisesRegexp(expected_exception, expected_pattern):
            self._create_action()

    def test_failure_reasons_allowed_with_device_module_target(self):
        self._given_name("MockedAction")
        self._given_target(DeviceModuleTarget(device="MockedDevice"))
        self._given_failure_reasons([ActionFailureReason("mocked_failure_reason")])
        self._when_creating_action()
        self._then_result_matches(
            ServiceActionInterface(
                "MockedAction", DeviceModuleTarget("MockedDevice"), [], [ActionFailureReason("mocked_failure_reason")]
            )
        )

    def _when_creating_action(self):
        self._result = self._create_action()

    def _create_action(self):
        return ServiceActionInterface(self._name, self._target, self._parameters, self._failure_reasons)

    def _then_result_matches(self, expected_result):
        self.assertEqual(self._result, expected_result)


class TestExceptionRaisedForUnsupportedTarget(object):
    def create_action_interface(self, target):
        ServiceActionInterface("mock_name", target, "mock_parameters", failure_reasons=[])

    def create_validator_interface(self, target):
        ServiceValidatorInterface("mock_name", target, "mock_parameters")

    def create_entity_recognizer_interface(self, target):
        ServiceEntityRecognizerInterface("mock_name", target)

    def create_query_interface(self, target):
        ServiceQueryInterface("mock_name", target, "mock_parameters")

    device_module_target = DeviceModuleTarget("mock_device")
    http_target = HttpTarget("mock_endpoint")
    frontend_target = FrontendTarget()

    @pytest.mark.parametrize(
        "interface_constructor,target", [
            (create_action_interface, device_module_target),
            (create_action_interface, http_target),
            (create_action_interface, frontend_target),
            (create_query_interface, device_module_target),
            (create_query_interface, http_target),
            (create_validator_interface, device_module_target),
            (create_validator_interface, http_target),
            (create_entity_recognizer_interface, device_module_target),
            (create_entity_recognizer_interface, http_target),
        ]
    )
    def test_supported_targets(self, interface_constructor, target):
        self.when_create_interface(interface_constructor, target)
        self.then_no_exception_is_raised()

    def when_create_interface(self, interface_constructor, target):
        interface_constructor(self, target)

    def then_no_exception_is_raised(self):
        pass

    @pytest.mark.parametrize(
        "interface_constructor",
        [create_query_interface, create_validator_interface, create_entity_recognizer_interface]
    )
    def test_unsupported_frontend_target(self, interface_constructor):
        self.when_create_interface_then_exception_is_raised_matching(
            interface_constructor, FrontendTarget(), UnsupportedServiceInterfaceTarget,
            "Expected a non-frontend target for service interface 'mock_name' but got a frontend target."
        )

    def when_create_interface_then_exception_is_raised_matching(
        self, interface_constructor, target, expected_exception, expected_message
    ):
        with pytest.raises(expected_exception) as excinfo:
            interface_constructor(self, target)
        assert expected_message == str(excinfo.value)


class ServiceTargetsTestCase(unittest.TestCase, EqualityAssertionTestCaseMixin):
    def test_device_module_target_equality(self):
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(
            DeviceModuleTarget("mock_device"), DeviceModuleTarget("mock_device")
        )

    def test_device_module_target_inequality_due_to_device(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            DeviceModuleTarget("mock_device_1"), DeviceModuleTarget("mock_device_2")
        )

    def test_device_module_target_not_equals_instance_of_other_class(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            DeviceModuleTarget("mock_device"), "instance_of_other_class"
        )

    def test_frontend_target_equality(self):
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(FrontendTarget(), FrontendTarget())

    def test_frontend_target_target_not_equals_instance_of_other_class(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(FrontendTarget(), "instance_of_other_class")

    def test_http_target_equality(self):
        self.assert_eq_returns_true_and_ne_returns_false_symmetrically(
            HttpTarget("mock_endpoint"), HttpTarget("mock_endpoint")
        )

    def test_http_target_inequality_due_to_endpoint(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            HttpTarget("mock_endpoint_1"), HttpTarget("mock_endpoint_2")
        )

    def test_http_target_target_not_equals_instance_of_other_class(self):
        self.assert_eq_returns_false_and_ne_returns_true_symmetrically(
            HttpTarget("mock_endpoint"), "instance_of_other_class"
        )
