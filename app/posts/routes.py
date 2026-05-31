import os
import uuid
from flask import render_template, url_for, flash, redirect, current_app
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from PIL import Image

from app.posts import posts
from app.posts.forms import PhotoPostForm, CommentForm
from app.models import PhotoPost, db, Comment
from flask import request

def format_ratio(val):
    if isinstance(val, tuple) and len(val) == 2:
        return val[0] / val[1] if val[1] != 0 else val[0]
    if hasattr(val, 'numerator') and hasattr(val, 'denominator'):
        return val.numerator / val.denominator if val.denominator != 0 else val.numerator
    return val

def format_shutter_speed(val):
    if isinstance(val, tuple) and len(val) == 2:
        return f"{val[0]}/{val[1]}"
    if hasattr(val, 'numerator') and hasattr(val, 'denominator'):
        return f"{val.numerator}/{val.denominator}"
    return str(val)

def extract_exif(image_path):
    exif_data = {
        'camera_model': None, 'iso': None, 
        'aperture': None, 'shutter_speed': None,
        'found': False
    }
    try:
        img = Image.open(image_path)
        
        # Pillow 8+ getexif()
        exif = img.getexif()
        
        # Fallback to _getexif() if needed
        if not exif and hasattr(img, '_getexif'):
            exif = img._getexif()
            
        if exif:
            # 271 Make, 272 Model
            make = str(exif.get(271, '')).strip()
            model = str(exif.get(272, '')).strip()
            
            if make and model:
                if make.lower() in model.lower():
                    exif_data['camera_model'] = model
                else:
                    exif_data['camera_model'] = f"{make} {model}"
            elif model:
                exif_data['camera_model'] = model
                
            # Exif IFD tags (ISO, FNumber, ExposureTime)
            exif_ifd = None
            if hasattr(exif, 'get_ifd'):
                try:
                    exif_ifd = exif.get_ifd(0x8769)
                except:
                    pass
            
            # Dictionary to search (prefer Exif IFD, fallback to main EXIF)
            search_dict = exif_ifd if exif_ifd else exif
            
            iso = search_dict.get(34855) or exif.get(34855)
            if iso: 
                exif_data['iso'] = str(iso)
                exif_data['found'] = True
                
            fnumber = search_dict.get(33437) or exif.get(33437)
            if fnumber:
                val = format_ratio(fnumber)
                if val: 
                    exif_data['aperture'] = f"f/{val}"
                    exif_data['found'] = True
                    
            exposure = search_dict.get(33434) or exif.get(33434)
            if exposure:
                exif_data['shutter_speed'] = format_shutter_speed(exposure)
                exif_data['found'] = True
                
            if exif_data['camera_model']:
                exif_data['found'] = True
                
    except Exception as e:
        print(f"EXIF okunurken hata: {e}")
        
    return exif_data

@posts.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PhotoPostForm()
    if form.validate_on_submit():
        if form.image_file.data:
            picture_file = form.image_file.data
            
            filename = secure_filename(picture_file.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            upload_dir = os.path.join(current_app.root_path, 'static', 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            
            picture_path = os.path.join(upload_dir, unique_filename)
            picture_file.save(picture_path)
            
            exif_info = extract_exif(picture_path)
            
            if current_app.config.get('CLOUDINARY_CLOUD_NAME'):
                import cloudinary.uploader
                try:
                    upload_result = cloudinary.uploader.upload(picture_path)
                    image_url = upload_result.get('secure_url')
                    os.remove(picture_path)
                except Exception as e:
                    print(f"Cloudinary upload failed: {e}")
                    image_url = unique_filename
            else:
                image_url = unique_filename
            
            camera_model = exif_info.get('camera_model') or form.camera_model.data
            iso = exif_info.get('iso') or form.iso.data
            aperture = exif_info.get('aperture') or form.aperture.data
            shutter_speed = exif_info.get('shutter_speed') or form.shutter_speed.data
            
            post = PhotoPost(
                title=form.title.data,
                description=form.description.data,
                category=form.category.data,
                image_file=image_url,
                camera_model=camera_model,
                lens_model=form.lens_model.data,
                iso=iso,
                aperture=aperture,
                shutter_speed=shutter_speed,
                editing_software=form.editing_software.data,
                user_id=current_user.id
            )
            db.session.add(post)
            db.session.commit()
            
            if exif_info.get('found'):
                flash('Fotoğrafınız başarıyla paylaşıldı! (Kamera verileri otomatik eklendi)', 'success')
            else:
                flash('Fotoğrafınız paylaşıldı ancak EXIF (kamera) verisi bulunamadı. Fotoğraf işlenmiş (WhatsApp, ekran görüntüsü vb.) olabilir.', 'info')
                
            return redirect(url_for('main.index'))
            
    return render_template('posts/new_post.html', form=form)

@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = db.get_or_404(PhotoPost, post_id)
    
    if request.method == 'GET':
        post.views += 1
        db.session.commit()
        
    form = CommentForm()
    
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash('Yorum yazabilmek için lütfen giriş yapın.', 'info')
            return redirect(url_for('auth.login', next=request.path))
            
        comment = Comment(
            body=form.body.data,
            post=post,
            author=current_user
        )
        db.session.add(comment)
        db.session.commit()
        
        flash('Yorumunuz eklendi!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
        
    return render_template('posts/post.html', post=post, form=form)

@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = db.get_or_404(PhotoPost, post_id)
    if post.author != current_user:
        flash('Sadece kendi yüklediğiniz fotoğrafları silebilirsiniz.', 'danger')
        return redirect(url_for('posts.post', post_id=post.id))
    
    # Delete the physical image file if not a URL
    if post.image_file and not post.image_file.startswith('http'):
        picture_path = os.path.join(current_app.root_path, 'static', 'uploads', post.image_file)
        if os.path.exists(picture_path):
            os.remove(picture_path)
            
    db.session.delete(post)
    db.session.commit()
    flash('Fotoğrafınız başarıyla silindi.', 'success')
    return redirect(url_for('main.index'))

@posts.route('/like/<int:post_id>', methods=['POST'])
@login_required
def like_post(post_id):
    post = db.session.get(PhotoPost, post_id)
    if not post:
        flash('Fotoğraf bulunamadı.', 'danger')
        return redirect(url_for('main.index'))
    
    if current_user.has_liked_post(post):
        current_user.unlike_post(post)
    else:
        current_user.like_post(post)
    
    db.session.commit()
    
    # Redirect back to where the user came from (feed, profile, or post detail)
    return redirect(request.referrer or url_for('posts.post', post_id=post.id))
