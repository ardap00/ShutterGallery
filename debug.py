import traceback
from app import create_app
from flask import render_template

app = create_app()

with app.test_request_context():
    try:
        class DummyUser:
            username = "ardap00"
        
        html = render_template('users/3d_gallery.html', user=DummyUser(), photos_json="[]")
        print("Template rendered successfully! Length:", len(html))
    except Exception as e:
        print("Template Syntax Error or Render Error:")
        traceback.print_exc()
