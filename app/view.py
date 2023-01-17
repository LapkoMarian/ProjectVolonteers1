from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
from flask import current_app as app


@app.route("/")
def index():
    return redirect (url_for("post.view_post"))

