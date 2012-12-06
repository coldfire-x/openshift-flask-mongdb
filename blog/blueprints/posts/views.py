# -*- coding: utf8 -*-
from datetime import datetime

from flask import (Blueprint, request, redirect, 
    render_template, url_for, session)
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


@posts.route('/list/', defaults={'mode':'normal'})
@posts.route('/list/<string:mode>')
def list(mode):
    if mode is 'edit' and 'uid' not in session:
        return redirect(url_for('admin.login'))

    posts = Post.objects.all()
    template = 'edit_list.html' if mode is 'edit' else 'normal_list.html'

    return render_template(template, posts=posts)


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

            tags = [ele for ele in set(x.strip().lower() for x in tags.split(','))]
            post['tags'] = tags

            post.save()

        return redirect(url_for('.list'))


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

            tags = [ele for ele in set(x.strip().lower() for x in tags.split(','))]
            post['tags'] = tags

            post['updated_at'] = now

            post.save()

        return redirect(url_for('.list'))

# Register the urls
posts.add_url_rule('/<slug>/', view_func=DetailView.as_view('detail'))
posts.add_url_rule('/new', view_func=login_required(NewPostView.as_view('new')))
posts.add_url_rule('/<slug>/edit',view_func=login_required(EditPost.as_view('edit')))
