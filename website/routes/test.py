from flask import Blueprint, render_template, request, flash, redirect, url_for

test = Blueprint('test', __name__)

@test.route('/')
def test_page():
    return render_template('index.html')