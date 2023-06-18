from flask import Blueprint, render_template, url_for, flash, redirect, request
from DarkTech.forms import PostForm
from .models import Post # import db from models.py
from . import db # import db from __init__.py
import markdown
import requests
from bs4 import BeautifulSoup

main = Blueprint('main', __name__)

@main.route('/')
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@main.route('/post/new', methods=['GET', 'POST'])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        md = markdown.Markdown()
        html_content = md.convert(form.content.data)
        post_ = Post(id=1, title=form.title.data, content=html_content)
        post_id = post_.id
        post = Post(id=post_id + 1, title=form.title.data, content=html_content)
        db.session.add(post)
        db.session.flush()  # Add this line
        try:
            db.session.commit()
            created_post = Post.query.get(post.id)
            print(f"Created post: {created_post}")
            print(f"Post ID: {post.id}")
        except Exception as e:
            print(f"Error saving post: {e}")
            db.session.rollback()
        flash('Your post has been created!', 'success')
        return redirect(url_for('main.post', post_id=post.id))
    else:
        print(f"Form validation errors: {form.errors}")
    return render_template('create_post.html', title='New Post', form=form)

@main.route('/admin')
def admin():
    return render_template('admin.html')

@main.route('/admin/users')
def admin_users():
    # Here you could fetch data from your database and pass it to the template
    # users = get_all_users()
    # return render_template('admin_users.html', users=users)
    return render_template('admin_users.html')

@main.route('/create', methods=['GET', 'POST'])
def create():
    # Get the basic toolbox elements
    basic_elements = [
        {"name": "Heading", "value": "<h1>Heading</h1>"},
        {"name": "Paragraph", "value": "<p>Paragraph</p>"},
        {"name": "Image", "value": "<img src='/path/to/image.jpg' />"},
        {"name": "Button", "value": "<button>Button</button>"},
    ]
    basic_properties = [
        {"name": "Color", "id": "color", "value": "color: red;"},
        {"name": "Background Color", "id": "background-color", "value": "background-color: #eaeaea;"},
        {"name": "Font Size", "id": "font-size", "value": "font-size: 16px;"},
        {"name": "Margin", "id": "margin", "value": "margin: 10px;"},
        {"name": "Padding", "id": "padding", "value": "padding: 5px;"},
        {"name": "Border", "id": "border", "value": "border: 1px solid #eaeaea;"},
        {"name": "Border Radius", "id": "border-radius", "value": "border-radius: 5px;"},
        {"name": "Width", "id": "width", "value": "width: 100%;"},
        {"name": "Height", "id": "height", "value": "height: 100%;"},
        {"name": "Text Align", "id": "text-align", "value": "text-align: center;"},
        {"name": "Font Family", "id": "font-family", "value": "font-family: Arial;"},
        {"name": "Font Weight", "id": "font-weight", "value": "font-weight: normal;"},
        {"name": "Line Height", "id": "line-height", "value": "line-height: 1.5;"},
        {"name": "Text Decoration", "id": "text-decoration", "value": "text-decoration: none;"},
        {"name": "Text Transform", "id": "text-transform", "value": "text-transform: none;"},
        {"name": "Box Shadow", "id": "box-shadow", "value": "box-shadow: none;"},
        {"name": "Opacity", "id": "opacity", "value": "opacity: 1;"},
        {"name": "Position", "id": "position", "value": "position: relative;"},
        {"name": "Top", "id": "top", "value": "top: 0;"},
        {"name": "Right", "id": "right", "value": "right: 0;"},
        {"name": "Bottom", "id": "bottom", "value": "bottom: 0;"},
        {"name": "Left", "id": "left", "value": "left: 0;"},
        {"name": "Float", "id": "float", "value": "float: none;"},
        {"name": "Clear", "id": "clear", "value": "clear: none;"},
        {"name": "Display", "id": "display", "value": "display: block;"},
        {"name": "Flex", "id": "flex", "value": "flex: none;"},
        {"name": "Flex Direction", "id": "flex-direction", "value": "flex-direction: row;"},
        {"name": "Flex Wrap", "id": "flex-wrap", "value": "flex-wrap: nowrap;"},
        {"name": "Justify Content", "id": "justify-content", "value": "justify-content: flex-start;"},
        {"name": "Align Items", "id": "align-items", "value": "align-items: stretch;"},
        {"name": "Align Content", "id": "align-content", "value": "align-content: stretch;"},
        {"name": "Align Self", "id": "align-self", "value": "align-self: auto;"},
        {"name": "Order", "id": "order", "value": "order: 0;"},
        {"name": "Flex Grow", "id": "flex-grow", "value": "flex-grow: 0;"},
        {"name": "Flex Shrink", "id": "flex-shrink", "value": "flex-shrink: 1;"},
        {"name": "Flex Basis", "id": "flex-basis", "value": "flex-basis: auto;"},
        {"name": "Grid Template Columns", "id": "grid-template-columns", "value": "grid-template-columns: none;"},
        {"name": "Grid Template Rows", "id": "grid-template-rows", "value": "grid-template-rows: none;"},
        {"name": "Grid Gap", "id": "grid-gap", "value": "grid-gap: 0;"},
        {"name": "Grid Column", "id": "grid-column", "value": "grid-column: auto;"},
        {"name": "Grid Row", "id": "grid-row", "value": "grid-row: auto;"},
        {"name": "Grid Area", "id": "grid-area", "value": "grid-area: auto;"},
        {"name": "Grid Auto Columns", "id": "grid-auto-columns", "value": "grid-auto-columns: auto;"},
        {"name": "Grid Auto Rows", "id": "grid-auto-rows", "value": "grid-auto-rows: auto;"},
        {"name": "Grid Auto Flow", "id": "grid-auto-flow", "value": "grid-auto-flow: row;"},
        {"name": "Grid Column Start", "id": "grid-column-start", "value": "grid-column-start: auto;"},
        {"name": "Grid Column End", "id": "grid-column-end", "value": "grid-column-end: auto;"},
        {"name": "Grid Row Start", "id": "grid-row-start", "value": "grid-row-start: auto;"},
        {"name": "Grid Row End", "id": "grid-row-end", "value": "grid-row-end: auto;"},
        {"name": "Grid Column Gap", "id": "grid-column-gap", "value": "grid-column-gap: 0;"},
        {"name": "Grid Row Gap", "id": "grid-row-gap", "value": "grid-row-gap: 0;"},
        {"name": "Grid Template Areas", "id": "grid-template-areas", "value": "grid-template-areas: none;"},
        {"name": "Grid Area", "id": "grid-area", "value": "grid-area: auto;"},
        {"name": "Grid Template", "id": "grid-template", "value": "grid-template: none;"},
        {"name": "Grid", "id": "grid", "value": "grid: none;"},
        {"name": "Grid Column Start", "id": "grid-column-start", "value": "grid-column-start: auto;"},
        {"name": "Grid Column End", "id": "grid-column-end", "value": "grid-column-end: auto;"},
        {"name": "Grid Row Start", "id": "grid-row-start", "value": "grid-row-start: auto;"},
        {"name": "Grid Row End", "id": "grid-row-end", "value": "grid-row-end: auto;"},
        {"name": "Grid Column", "id": "grid-column", "value": "grid-column: auto;"},
        {"name": "Grid Row", "id": "grid-row", "value": "grid-row: auto;"},
        {"name": "Grid Area", "id": "grid-area", "value": "grid-area: auto;"},
        {"name": "Grid Template Columns", "id": "grid-template-columns", "value": "grid-template-columns: none;"},
        {"name": "Grid Template Rows", "id": "grid-template-rows", "value": "grid-template-rows: none;"},
        {"name": "Grid Template Areas", "id": "grid-template-areas", "value": "grid-template-areas: none;"},
        {"name": "Grid Template", "id": "grid-template", "value": "grid-template: none;"},
        {"name": "Grid", "id": "grid", "value": "grid: none;"},
        {"name": "Grid Auto Columns", "id": "grid-auto-columns", "value": "grid-auto-columns: auto;"},
        {"name": "Grid Auto Rows", "id": "grid-auto-rows", "value": "grid-auto-rows: auto;"},
        {"name": "Grid Auto Flow", "id": "grid-auto-flow", "value": "grid-auto-flow: row;"},
        {"name": "Grid Column Gap", "id": "grid-column-gap", "value": "grid-column-gap: 0;"},
        {"name": "Grid Row Gap", "id": "grid-row-gap", "value": "grid-row-gap: 0;"},
        {"name": "Grid Gap", "id": "grid-gap", "value": "grid-gap: 0;"},
    ]




    if request.method == 'POST':
        # Get the HTML code from the text box
        html_code = request.form['html_code']
        # Do something with the HTML code
        pass

    return render_template("create.html", basic_elements=basic_elements, basic_properties=basic_properties)