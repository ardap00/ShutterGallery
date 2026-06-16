import traceback
from app import create_app
from flask import render_template
from flask_login import current_user

app = create_app()

with app.test_request_context():
    try:
        class DummyUser:
            is_authenticated = True
            username = "ardap00"
            language = "tr"
            
        html = render_template('main/index.html', current_user=DummyUser(), posts=[], feed_type='feed')
        print("index.html compiled successfully! Length:", len(html))
    except Exception as e:
        print("Template Syntax Error or Render Error:")
        traceback.print_exc()
