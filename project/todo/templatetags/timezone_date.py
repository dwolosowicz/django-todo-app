from django import template
from django.template.defaulttags import register


@register.filter(name="timezone_date")
def do_timezone_date(value, arg):
    try:
        tag_name, timezone_variable = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    return DatePriorityNode(timezone_variable)
