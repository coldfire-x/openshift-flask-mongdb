# -*- coding: utf8 -*-

from flask import Blueprint, request, redirect, render_template, url_for
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form

from models import Post, Comment
from utilities import login_required

posts = Blueprint('posts', __name__, template_folder='templates')

def check_slug_uniq(slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return True
    else:
        return False

class ListView(MethodView):

    def get(self):
        posts = Post.objects.all()
        return render_template('posts/list.html', posts=posts)


class DetailView(MethodView):
    form = model_form(Comment, exclude=['created_at'])

    def get_context(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)

        context = {
            "post": post,
            "form": form
        }
        return context

    def get(self, slug):
        context = self.get_context(slug)
        return render_template('posts/detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('posts.detail', slug=slug))

        return render_template('posts/detail.html', **context)

class NewPostView(MethodView):
    form = model_form(Post, 
        exclude=('created_at', 'comments'))

    def get(self):
        return render_template('posts/new.html', form=self.form())

    def post(self):
        form = self.form(request.form)

        if form.validate():
            post = Post()
            form.populate_obj(post)
            post.save()

        return redirect(url_for('.list'))


# Register the urls
posts.add_url_rule('/', view_func=ListView.as_view('list'))
posts.add_url_rule('/posts/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/posts/new', view_func=login_required(NewPostView.as_view('new')))
