from django.utils.translation import ugettext_lazy as _
from sentry.models.groupresolution import GroupResolution
from sentry.plugins import Plugin
import logging
import sentry_regressions

try:
    from pkg_resources import parse_version as pkg_parse_version
except ImportError:
    pkg_parse_version = None


logger = logging.getLogger(__name__)

GITHUB_URL = 'https://github.com/4teamwork/sentry-regressions'


class RegressionPlugin(Plugin):

    author = "4teamwork AG"
    author_url = GITHUB_URL
    title = 'Regressions Plugin'
    description = 'Consider release versions when detecting regressions.'
    slug = 'regressions'

    resource_links = [
        (_('Bug Tracker'), GITHUB_URL + '/issues'),
        (_('Source'), GITHUB_URL),
    ]

    version = sentry_regressions.VERSION

    def is_regression(self, group, event, **kwargs):
        """
        Called on new events when the group's status is resolved.
        Return True if this event is a regression, False if it is not,
        None to defer to other plugins.

        :param group: an instance of ``Group``
        :param event: an instance of ``Event``
        """
        # Determine in which release this group has been marked as resolved.
        resolution = self.get_resolution(group)

        if resolution is None:
            # No resolution found
            return None

        res_type, res_release_version = resolution

        if res_type == GroupResolution.Type.in_next_release:
            # We don't do special handling for "next-release" resolutions.
            # Defer to other plugins and/or default implementation.
            return None

        # There exists a 'in_release' resolution for this group.
        resolved_in_release = res_release_version
        occurred_in_release = event.get_tag('sentry:release')

        if occurred_in_release is None:
            # Event not tagged with release information.
            return None

        # It's only a regression if the release version of the event is
        # equal or higher than the version the issue was supposedly resolved.
        pv = parse_version
        try:
            return pv(occurred_in_release) >= pv(resolved_in_release)
        except Exception as exc:
            # Error during version parsing - defer to other plugins
            logger.warn('Failed to compare versions %r and %r: %r' % (
                occurred_in_release, resolved_in_release, exc))
            return None

    def get_resolution(self, group):
        """Determine in which release this group has been marked as resolved.
        """
        resolution = GroupResolution.objects.filter(
            group=group,
        ).select_related('release').values_list(
            'type',
            'release__version',
        ).first()
        return resolution


def parse_version(version_string):
    """Parse a version string.

    Will attempt to use `packaging` module to parse versions according to
    PEP 440. If the `packaging` module is not available (usually vendored
    via `pkg_resources`) will fall back to a more naive version parsing.
    """
    if pkg_parse_version is not None:
        return pkg_parse_version(version_string)

    return parse_version_fallback(version_string)


def parse_version_fallback(version_string):
    """Naive version parsing implementation.

    Turns a version string into a list of version components with numeric
    integers.

    This allows these version tuples to be sorted / compared and get correct
    results regarding natural sorting of numbers. However, none of the
    subtleties of setuptools version parsing or PEP 440 are considered.

    So suffixes like 'rc1' or 'beta' will simply be sorted alphabetically.
    """
    return parse_ints(version_string.split('.'))


def tryint(value):
    try:
        value = int(value)
    except ValueError:
        pass
    return value


def parse_ints(sequence):
    return map(tryint, sequence)
