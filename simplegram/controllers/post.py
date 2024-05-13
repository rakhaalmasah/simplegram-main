import os
from flask import render_template, redirect, request, flash, jsonify, url_for
from simplegram.forms import CommentForm, PostForm, EditPostForm, MessageForm
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
from sqlalchemy import select, text

from simplegram.models.models import Post, User, Comment, Bookmark, Message, Like
from config import db

@login_required
def index():
    sql = '''
            SELECT 
                post.id, user_id, image, post.description, 
                post.created_at, post.updated_at, username, fullname,profpic,
                (SELECT COUNT(*) FROM comment c WHERE c.post_id = post.id) AS jml_comment,
                (SELECT COUNT(*) FROM `like` l WHERE l.post_id = post.id) AS jml_likes,
                EXISTS (SELECT 1 FROM `like` l2 WHERE l2.post_id = post.id AND l2.user_id = :current_user_id) AS user_liked,
                EXISTS (SELECT 1 FROM bookmark b WHERE b.post_id = post.id AND b.user_id = :current_user_id) AS user_bookmarked
            FROM post 
            JOIN user ON (post.user_id = user.id)
            ORDER BY post.created_at DESC
        '''
    postData = db.session.execute(text(sql), {'current_user_id': current_user.id}).all()
    return render_template('index.html', postData=postData)

@login_required
def add_post():
    from bootstrap import app

    form = PostForm()
    if form.validate_on_submit():
        imFile = form.image.data
        fileName = secure_filename(imFile.filename)
        post = Post(user_id=current_user.id,description=form.description.data,image=fileName)
        db.session.add(post)
        db.session.commit()
        imFile.save(f'./static/uploads/{fileName}')
        flash({'info': 'Berhasil posting foto'})
        return redirect('/')
    return render_template('add_post.html', form=form)

@login_required
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = EditPostForm()
    if form.validate_on_submit():
        if post.user_id == current_user.id:
            post.description = form.description.data
            db.session.commit()
            flash({'info': 'posting berhasil dirubah'})
        else:
            flash({'error': 'posting gagal dirubah'})
        return redirect('/mypost')
    else:
        form.submit.label.text = 'Edit Postingan'
        form.description.data = post.description
        return render_template('edit_post.html', form=form, post=post)
    
@login_required
def del_post(post_id):
    post = Post.query.get(post_id)
    if post and post.user_id == current_user.id:
        db.session.delete(post)
        db.session.commit()
        flash({'info': 'berhasil hapus postingan'})
    else:
        flash({'error': 'tidak berhasil hapus posting'})
    return redirect('/mypost')

@login_required
def add_comment(post_id):
    sql = '''select 
            post.id, user_id, image, post.description, 
            post.created_at, post.updated_at, username, fullname
        from post
        join user on (post.user_id = user.id)
        where post.id = :id
    '''
    postData = db.session.execute(text(sql), {'id': post_id}).one()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(post_id=postData.id, user_id=current_user.id, comment=form.comment.data)
        db.session.add(comment)
        db.session.commit()
        flash({'info': 'Berhasil menambahkan komentar'})
        return redirect('/')
    return render_template('add_comment.html', form=form, postData=postData)

@login_required
def my_post():
    postData = db.session.execute(db.select(Post).filter_by(user_id=current_user.id)).scalars()
    return render_template('my_posts.html', postData=postData)

def api_comments(post_id):
    commentData = db.session.query(Comment, User).join(User)\
                    .filter(Comment.post_id==post_id)\
                    .order_by(Comment.created_at.desc())\
                    .all()
    commentDict = []
    for comment, user in commentData:
        adict = {'id': comment.id, 'comment': comment.comment, 
                 'username': user.username, 'fullname': user.fullname,
                 'created_at': comment.created_at.strftime('%Y-%m-%d'), 
                 'updated_at': comment.updated_at.strftime('%Y-%m-%d')}
        commentDict.append(adict)
    return jsonify(commentDict)

# Ini tambahan Kode Saya
@login_required
def my_bookmark():
    bookmark_data = db.session.query(Bookmark, Post).join(Post).filter(Bookmark.user_id == current_user.id).all()
    return render_template('add_bookmark.html', bookmark_data=bookmark_data)

@login_required
def add_bookmark(post_id):
    existing_bookmark = db.session.query(Bookmark).filter_by(user_id=current_user.id, post_id=post_id).first()

    if existing_bookmark:
        flash({'error': 'Postingan sudah ada di bookmark'})
    else:
        bookmark = Bookmark(user_id=current_user.id, post_id=post_id)
        db.session.add(bookmark)
        db.session.commit()
        flash({'info': 'Posting berhasil ditambahkan ke bookmark'})

    return redirect('/')

@login_required
def del_bookmark(post_id):
    bookmark = db.session.query(Bookmark).filter_by(user_id=current_user.id, post_id=post_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash({'info': 'Bookmark dihapus'})
    else:
        flash({'error': 'Bookmark tidak ditemukan'})
    return redirect('/mybookmark')

@login_required
def dels_bookmark(post_id):
    bookmark = db.session.query(Bookmark).filter_by(user_id=current_user.id, post_id=post_id).first()
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        flash({'info': 'Bookmark dihapus'})
    else:
        flash({'error': 'Bookmark tidak ditemukan'})
    return redirect('/')

# Ini tambahan Kode saya
@login_required
def mailbox():
    received_messages = Message.query.filter_by(receiver_id=current_user.id).all()
    sent_messages = Message.query.filter_by(sender_id=current_user.id).all()
    return render_template('mailbox.html', received_messages=received_messages, sent_messages=sent_messages)

@login_required
def delete_message(message_id):
    message = Message.query.get(message_id)
    if message:
        if message.sender_id == current_user.id:
            db.session.delete(message)
            db.session.commit()
            flash({'info': 'Pesan berhasil dihapus'})
        else:
            flash({'error': 'Anda tidak memiliki izin untuk menghapus pesan ini'})
    else:
        flash({'error': 'Pesan tidak ditemukan'})
    return redirect(url_for('sg.mailbox'))

@login_required
def sendmail():
    form = MessageForm()
    users = [(user.id, user.username) for user in User.query.filter(User.id != current_user.id).all()]
    form.receiver_id.choices = users
    if request.method == 'POST' and form.validate_on_submit():
        receiver_id = form.receiver_id.data
        content = form.content.data
        if int(receiver_id) == current_user.id:
            flash({'error': 'Tidak dapat mengirim pesan ke diri sendiri'})
        else:
            message = Message(sender_id=current_user.id, receiver_id=int(receiver_id), content=content)
            db.session.add(message)
            db.session.commit()
            flash({'info': 'Pesan terkirim'})
            return redirect(url_for('sg.mailbox'))
    return render_template('sendmail.html', form=form)

@login_required
def like_post(post_id):
    post = Post.query.get(post_id)
    if post:
        existing_like = db.session.query(Like).filter_by(user_id=current_user.id, post_id=post_id).first()

        if existing_like:
            flash({'error': 'Anda sudah menyukai posting ini'})
        else:
            like = Like(user_id=current_user.id, post_id=post_id)
            db.session.add(like)
            db.session.commit()
            flash({'info': 'Posting disukai'})
    else:
        flash({'error': 'Posting tidak ditemukan'})
    return redirect('/')

@login_required
def unlike_post(post_id):
    like = db.session.query(Like).filter_by(user_id=current_user.id, post_id=post_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        flash({'info': 'Suka dihapus'})
    else:
        flash({'error': 'Suka tidak ditemukan'})
    return redirect('/')

@login_required
def show_likes(post_id):
    sql = '''select 
            post.id, user_id, image, post.description, 
            post.created_at, post.updated_at, username, fullname
        from post
        join user on (post.user_id = user.id)
        where post.id = :id
    '''
    postData = db.session.execute(text(sql), {'id': post_id}).one()
    likes = db.session.query(User).join(Like).filter(Like.post_id == post_id).all()
    return render_template('showlikes.html', postData=postData, likes=likes)

@login_required
def view_profil(username):
    user = db.session.query(User).filter_by(username=username).first()
    if not user:
        flash({'error': 'Pengguna tidak ditemukan'})
        return redirect('/')
    return render_template('viewprofil.html', user=user)