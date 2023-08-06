import re
from vint.ast.node_type import NodeType
from vint.linting.level import Level
from vint.linting.policy.abstract_policy import AbstractPolicy
from vint.linting.policy.reference.googlevimscriptstyleguide import get_reference_source
from vint.linting.policy_registry import register_policy
from vint.linting.policy.prohibit_unnecessary_double_quote import _special_char_matcher

_single_escape = re.compile(r'(?<!\\)\\(?!\\)')


@register_policy
class ProhibitDoubleQuoteWithWrongEscape(AbstractPolicy):
    description = 'Double quoted string contains probably wrong escape'
    reference = get_reference_source('STRINGS')
    level = Level.WARNING


    def listen_node_types(self):
        return [NodeType.STRING]


    def is_valid(self, node, lint_context):
        """ Whether the specified node is valid.

        Warns for double quoted strings that contain single backslashes, which
        are not part of the group of special escapes (e.g. "\n").

        See `:help expr-string`. """

        value = node['value']

        if value[0] != '"':
            return True

        if _special_char_matcher.search(value) is not None:
            return True

        if _single_escape.search(value) is not None:
            return False

        return True
