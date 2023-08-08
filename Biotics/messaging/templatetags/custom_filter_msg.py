from django import template

register = template.Library()


@register.filter
def get_conversation_with_other_user(conversations, other_user):
    for conversation in conversations:
        if conversation.participants.filter(id=other_user.id).exists():
            return {
                'conversation': conversation,
                'other_user': other_user,
            }
    return None

