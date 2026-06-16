from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from sqlalchemy import or_, and_
from app.models import db, User, Message
from app.messages import messages
from app.messages.forms import MessageForm

@messages.route('/inbox')
@login_required
def inbox():
    # Son atılan mesajları al
    messages_query = db.session.execute(
        db.select(Message).filter(
            or_(Message.sender_id == current_user.id, Message.recipient_id == current_user.id)
        ).order_by(Message.timestamp.desc())
    ).scalars().all()
    
    conversations = {}
    for msg in messages_query:
        other_user = msg.recipient if msg.sender_id == current_user.id else msg.sender
        if other_user.id not in conversations:
            conversations[other_user.id] = {
                'user': other_user,
                'last_message': msg,
                'unread_count': 0
            }
        
        # Eğer bu mesaj bana gelmişse ve henüz okunmamışsa sayacı artır
        if msg.recipient_id == current_user.id and not msg.is_read:
            conversations[other_user.id]['unread_count'] += 1
            
    conv_list = list(conversations.values())
    
    return render_template('messages/inbox.html', conversations=conv_list)

@messages.route('/chat/<username>', methods=['GET', 'POST'])
@login_required
def chat(username):
    user = db.session.execute(db.select(User).filter_by(username=username)).scalar_one_or_none()
    if not user:
        flash('Kullanıcı bulunamadı.', 'danger')
        return redirect(url_for('messages.inbox'))
        
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message(sender_id=current_user.id, recipient_id=user.id, body=form.body.data)
        db.session.add(msg)
        db.session.commit()
        return redirect(url_for('messages.chat', username=username))
        
    chat_history = db.session.execute(
        db.select(Message).filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.recipient_id == user.id),
                and_(Message.sender_id == user.id, Message.recipient_id == current_user.id)
            )
        ).order_by(Message.timestamp.asc())
    ).scalars().all()
    
    # Okunmamış mesajları okundu olarak işaretle
    has_unread = False
    for msg in chat_history:
        if msg.recipient_id == current_user.id and not msg.is_read:
            msg.is_read = True
            has_unread = True
            
    if has_unread:
        db.session.commit()
        
    return render_template('messages/chat.html', user=user, chat_history=chat_history, form=form)
