from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def main_index():
    return render_template("index.html")

#
# @main.route('/')
# def index():
#     product_data = Product.query.all()
#
#     return render_template("index.html", products=product_data)

