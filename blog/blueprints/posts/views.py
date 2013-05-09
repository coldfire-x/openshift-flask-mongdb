# -*- coding: utf8 -*-
from datetime import datetime

from flask import (Blueprint, request, redirect, 
    render_template, url_for, session)
from flask.views import MethodView
from flask.ext.mongoengine.wtf import model_form

from models import Post, Comment
from utilities import login_required, uniq_list

posts = Blueprint('posts', __name__, template_folder='templates')

def check_slug_uniq(slug):
    try:
        post = Post.objects.get(slug=slug)
    except Post.DoesNotExist:
        return True
    else:
        return False


@posts.route('/')
def index():
    page = request.args.get('page', 1)

    paginated_posts = Post.objects.paginate(page=int(page), per_page=6)
    tags = Post.objects.item_frequencies('tags')

    return render_template('list_posts.html', pagination=paginated_posts, tags=tags)

@posts.route('/tags/<tag>')
def tags(tag):
    page = request.args.get('page', 1)

    paginated_posts = Post.objects(tags=tag).paginate(page=int(page), per_page=6)
    tags = Post.objects.item_frequencies('tags')

    return render_template('list_posts.html', pagination=paginated_posts, tags=tags, tag=tag)


@posts.route('/admin/posts/')
@login_required
def list_posts():
    posts = Post.objects.all()
    return render_template('list_posts_for_editing.html', posts=posts)


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
        return render_template('detail.html', **context)

    def post(self, slug):
        context = self.get_context(slug)
        form = context.get('form')

        if form.validate():
            comment = Comment()
            form.populate_obj(comment)

            post = context.get('post')
            post.comments.append(comment)
            post.save()

            return redirect(url_for('.detail', slug=slug))

        return render_template('detail.html', **context)


class NewPostView(MethodView):
    form = model_form(Post, 
        exclude=('created_at', 'comments', 'updated_at'))

    def get(self):
        return render_template('new.html', form=self.form())

    def post(self):
        form = self.form(request.form)
        tags = request.form['tags'] if request.form['tags'] else ''

        if form.validate():
            post = Post()
            form.populate_obj(post)

            tags = uniq_list(tags, ',')
            post['tags'] = tags

            post.save()

        return redirect(url_for('.index'))


class EditPost(MethodView):
    form = model_form(Post, 
        exclude=('created_at', 'comments', 'updated_at'))

    def get(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form()
        return render_template('edit.html', post=post, form=form)

    def post(self, slug):
        post = Post.objects.get_or_404(slug=slug)
        form = self.form(request.form)
        tags = request.form['tags'] if request.form['tags'] else ''

        if form.validate():
            now = datetime.now()

            for field in ['slug', 'title', 'body']:
                post[field] = form[field].data

            tags = uniq_list(tags, ',')
            post['tags'] = tags

            post['updated_at'] = now

            post.save()

        return redirect(url_for('.index'))

# Register the urls
posts.add_url_rule('/posts/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/posts/new', view_func=login_required(NewPostView.as_view('new')))
posts.add_url_rule('/posts/<slug>/edit',view_func=login_required(EditPost.as_view('edit')))
