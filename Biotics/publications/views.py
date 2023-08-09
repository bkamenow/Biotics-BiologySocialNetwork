from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, resolve_url, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from Biotics.publications.forms import PublicationCreateForm, PublicationEditForm, CommentForm
from Biotics.publications.models import PublicationModel, Like

from pyperclip import copy


class PublicationListView(LoginRequiredMixin, ListView):
    model = PublicationModel
    template_name = 'publications/publications.html'
    context_object_name = 'all_publications'
    login_url = reverse_lazy('login_page')

    def get_queryset(self):
        return PublicationModel.objects.order_by('-timestamp')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context


class PublicationCreateView(LoginRequiredMixin, CreateView):
    model = PublicationModel
    template_name = 'publications/create-publication.html'
    form_class = PublicationCreateForm
    success_url = reverse_lazy('publications')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PublicationUpdateView(LoginRequiredMixin, UpdateView):
    model = PublicationModel
    template_name = 'publications/edit-publication.html'
    form_class = PublicationEditForm

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.request.user.pk})

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PublicationDetailView(DetailView):
    model = PublicationModel
    template_name = 'publications/details-publication.html'
    context_object_name = 'publication'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        publication = self.object
        likes = publication.like_set.all()
        publication_is_liked_by_user = likes.filter(user=self.request.user)
        comments = publication.comment_set.all()
        comment_form = CommentForm()
        user = self.request.user

        context['likes'] = likes
        context['comments'] = comments
        context['comment_form'] = comment_form
        context['photo_is_liked_by_user'] = publication_is_liked_by_user
        context['user'] = user

        return context


class PublicationDeleteView(LoginRequiredMixin, DeleteView):
    model = PublicationModel
    template_name = 'publications/delete-publication.html'

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.user.pk})

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publication'] = self.object
        return context


@login_required
def like_publication(request, pk):
    publication = PublicationModel.objects.get(id=pk)
    like_objects = Like.objects.filter(publication_id=pk, user=request.user).first()

    if like_objects:
        like_objects.delete()
        publication.likes_count -= 1
    else:
        like = Like(publication=publication, user=request.user)
        like.save()
        publication.likes_count += 1

    publication.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{pk}')


@login_required
def add_comment(request, pk):
    if request.method == 'POST':
        publication = PublicationModel.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.publication = publication
            comment.user = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{pk}')


def filtered_publications(request, filter_type):
    comment_form = CommentForm()

    if filter_type == 'Botany':
        publications = PublicationModel.objects.filter(type_of_publication='Botany').order_by('-timestamp')
    elif filter_type == 'Microbiology':
        publications = PublicationModel.objects.filter(type_of_publication='Microbiology').order_by('-timestamp')
    elif filter_type == 'Zoology':
        publications = PublicationModel.objects.filter(type_of_publication='Zoology').order_by('-timestamp')
    else:
        publications = PublicationModel.objects.all().order_by('-timestamp')

    return render(request, 'publications/filtered_publications.html',
                  {'publications': publications, 'filter_type': filter_type, 'form': comment_form})


