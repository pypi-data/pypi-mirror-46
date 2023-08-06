from django.template import Library, TemplateSyntaxError, Node, NodeList
from django.utils.encoding import smart_str
from .. import feature_enabled, feature_activated

register = Library()


def parse_args_kwargs(parser, bits):
    args = []
    kwargs = {}
    bits = iter(bits)

    for bit in bits:
        for arg in bit.split(","):
            if '=' in arg:
                k, v = arg.split('=', 1)
                k = k.strip()
                kwargs[k] = parser.compile_filter(v)
            elif arg:
                args.append(parser.compile_filter(arg))

    return args, kwargs


def get_args_and_kwargs(args, kwargs, context):
    out_args = [arg.resolve(context) for arg in args]

    out_kwargs = dict(
        [
            (
                smart_str(k, 'ascii'),
                v.resolve(context)
            )
            for k, v in kwargs.items()
        ]
    )

    return out_args, out_kwargs


@register.tag()
def feature(parser, token):
    bits = token.contents.split(' ')

    if len(bits) < 1:
        raise TemplateSyntaxError(
            '%r tag requires at least one argument' % token.contents.split()[0]
        )

    nodelist_true = parser.parse(('else', 'endfeature'))
    token = parser.next_token()

    if token.contents == 'else':
        nodelist_false = parser.parse(('endfeature',))
        parser.delete_first_token()
    else:
        nodelist_false = NodeList()

    args, kwargs = parse_args_kwargs(parser, bits[1:])
    return FeatureNode(nodelist_true, nodelist_false, args, kwargs)


class FeatureNode(Node):
    def __init__(self, nodelist_true, nodelist_false, args, kwargs):
        if not any(args):
            raise TemplateSyntaxError(
                'feature tag expects at least one position argument'
            )

        if len(args) > 1:
            raise TemplateSyntaxError(
                'feature tag expects at most one position argument'
            )

        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false
        self.args = args
        self.kwargs = kwargs

    def render(self, context):
        features, kwargs = get_args_and_kwargs(self.args, self.kwargs, context)
        active = kwargs.pop('active', False)

        for key in kwargs.keys():
            raise TemplateSyntaxError(
                'feature tag got unexpected keyworwd argument: %s' % key
            )

        feature = features[0]
        request = context.get('request')

        if request is None:  # pragma: no cover
            return ''

        if feature_enabled(feature, request):
            if active and not feature_activated(feature, request):
                return self.nodelist_false.render(context)

            return self.nodelist_true.render(context)

        return self.nodelist_false.render(context)
