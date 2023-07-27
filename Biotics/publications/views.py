from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from Biotics.publications.forms import PublicationCreateForm
from Biotics.publications.models import PublicationModel


def publications_page(request):
    all_publications = PublicationModel.objects.all()
    user = request.user

    context = {
        'all_publications': all_publications,
    }
    return render(request, template_name='publications/publications.html', context=context)


@login_required
def create_publication(request):
    form = PublicationCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        publication = form.save(commit=False)
        publication.user = request.user
        publication.save()
        return redirect('publications')
    context = {'form': form}

    return render(request, template_name='publications/create-publication.html', context=context)
