from app.forms import PostForm

def test_valid_post_form():
    form = PostForm(data={'title': 'Test', 'content': 'Something'})
    assert form.is_valid()

def test_invalid_post_form():
    form = PostForm(data={'title': '', 'content': 'Missing title'})
    assert not form.is_valid()
