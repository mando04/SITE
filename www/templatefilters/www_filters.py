from django import template

register = template.Library()

@register.filter
def status(value):
	return "You suck!"