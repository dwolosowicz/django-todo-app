from django import template
from django.template.defaulttags import register
from todo.models import Task


class TaskPriorityNode(template.Node):
    def __init__(self, priority_level):
        self.priority_level = template.Variable(priority_level)

    def render(self, context):
        try:
            priority_level_value = self.priority_level.resolve(context)

            return "<i class='task-priority task-priority-{}'></i>".format(Task.priority_label(priority_level_value))
        except template.VariableDoesNotExist:
            return ''

@register.tag(name="task_priority")
def do_task_priority(parser, token):
    try:
        tag_name, priority_level = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument" % token.contents.split()[0]
        )

    return TaskPriorityNode(priority_level)