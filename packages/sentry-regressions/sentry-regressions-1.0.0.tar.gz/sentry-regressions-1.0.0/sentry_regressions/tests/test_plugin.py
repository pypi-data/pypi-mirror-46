from __future__ import absolute_import
from sentry.models import Event
from sentry.models.group import Group
from sentry.models.groupresolution import GroupResolution
from sentry.models.organization import Organization
from sentry.models.release import Release
from sentry.testutils import PluginTestCase
from sentry_regressions.plugin import parse_version as pv
from sentry_regressions.plugin import parse_version_fallback as pvfb
from sentry_regressions.plugin import RegressionPlugin


in_release = GroupResolution.Type.in_release
in_next_release = GroupResolution.Type.in_next_release


class TestRegressionPlugin(PluginTestCase):

    def setUp(self):
        super(TestRegressionPlugin, self).setUp()
        self.org = Organization.objects.create()

        self.release_8_0 = self.create_release(version='8.0')
        self.release_8_1 = self.create_release(version='8.1')
        self.release_8_0_1 = self.create_release(version='8.0.1')

        self.group = Group.objects.create()

    @property
    def plugin(self):
        return RegressionPlugin()

    def create_release(self, version):
        return Release.objects.create(organization=self.org, version=version)

    def create_event(self, release=None):
        event = Event(message='AttributeError', group=self.group)
        if release is not None:
            event.data['tags'] = [('sentry:release', release)]
        event.save()
        return event

    def resolve(self, group, release, type_):
        resolution = GroupResolution.objects.create(
            group=group,
            release=release,
            type=type_)
        return resolution

    def test_metadata(self):
        self.assertEqual('Regressions Plugin', self.plugin.title)
        self.assertEqual('4teamwork AG', self.plugin.author)

    def test_returns_false_if_not_an_actual_regression(self):
        event = self.create_event(release='8.0.1')
        self.resolve(self.group, self.release_8_1, in_release)

        self.assertEqual(False, self.plugin.is_regression(self.group, event))

    def test_returns_true_if_regression(self):
        event = self.create_event(release='8.1')
        self.resolve(self.group, self.release_8_1, in_release)

        self.assertEqual(True, self.plugin.is_regression(self.group, event))

    def test_defers_if_no_resolution_found(self):
        event = self.create_event(release='8.0.1')

        self.assertEqual(None, self.plugin.is_regression(self.group, event))

    def test_defers_in_next_release_resolutions(self):
        event = self.create_event(release='8.0.1')
        self.resolve(self.group, self.release_8_1, in_next_release)

        self.assertEqual(None, self.plugin.is_regression(self.group, event))

    def test_defers_if_no_version_in_event(self):
        event = self.create_event()
        self.resolve(self.group, self.release_8_1, in_release)

        self.assertEqual(None, self.plugin.is_regression(self.group, event))

    def test_compares_dev0_versions_correctly(self):
        # Note: Fallback version parsing doesn't handle this correctly
        self.assertTrue(pv('8.0') > pv('8.0.dev0'))

    def test_compares_year_based_versions_correctly(self):
        self.assertTrue(pv('2020.1') > pv('2019.1'))

    def test_compares_multi_digit_versions_correctly(self):
        self.assertTrue(pv('11.0') > pv('2.0'))
        self.assertTrue(pv('5.11') > pv('5.2'))
        self.assertTrue(pv('5.11.0') > pv('5.2.0'))

    def test_fallback_compares_year_based_versions_correctly(self):
        self.assertTrue(pvfb('2020.1') > pvfb('2019.1'))

    def test_fallback_compares_multi_digit_versions_correctly(self):
        self.assertTrue(pvfb('11.0') > pvfb('2.0'))
        self.assertTrue(pvfb('5.11') > pvfb('5.2'))
        self.assertTrue(pvfb('5.11.0') > pvfb('5.2.0'))
