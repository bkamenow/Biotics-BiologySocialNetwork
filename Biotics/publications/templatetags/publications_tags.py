from django import template

register = template.Library()


@register.filter
def user_has_liked(publication, user):
    return publication.like_set.filter(user=user).exists()
