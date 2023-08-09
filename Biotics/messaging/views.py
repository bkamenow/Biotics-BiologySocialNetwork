from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import MessageForm
from .models import Conversation, Message
from ..profiles.models import BioticsUserModel


@login_required
def create_conversation(request, other_user_id):
    logged_in_user = request.user
    other_user = get_object_or_404(BioticsUserModel, id=other_user_id)

    existing_conversation = Conversation.objects.filter(participants=logged_in_user) \
        .filter(participants=other_user).first()

    if existing_conversation:
        conversation_id = existing_conversation.id
    else:
        conversation = Conversation.objects.create()
        conversation.participants.add(logged_in_user, other_user)
        conversation_id = conversation.id

    return redirect('conversation_view', user_id=other_user.id)


@login_required
def conversations_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    conversation_infos = []

    for conversation in conversations:
        other_user = conversation.participants.exclude(id=request.user.id).first()
        if other_user:
            conversation_infos.append({
                'conversation': conversation,
                'other_user': other_user,
            })

    return render(request, 'messaging/conversations_list.html', {'conversation_infos': conversation_infos})


@login_required
def conversation_view(request, user_id):
    other_user = get_object_or_404(BioticsUserModel, id=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(other_user, request.user)

    messages = Message.objects.filter(conversation=conversation).order_by('timestamp')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            message = Message.objects.create(conversation=conversation, sender=request.user, content=content)

            recipient_ids = request.POST.getlist('recipients')
            if recipient_ids:
                recipients = BioticsUserModel.objects.filter(id__in=recipient_ids)
                message.receiver.set(recipients)

            form = MessageForm()

    else:
        form = MessageForm()

    context = {
        'conversation': conversation,
        'messages': messages,
        'other_user': other_user,
        'form': form,
    }
    return render(request, 'messaging/conversation_view.html', context)
