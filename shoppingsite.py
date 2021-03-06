"""Ubermelon shopping application Flask server.

Provides web interface for browsing melons, seeing detail about a melon, and
put melons in a shopping cart.

Authors: Joel Burton, Christian Fernandez, Meggie Mahnken.
"""


from flask import Flask, render_template, redirect, flash, session
import jinja2

import melons


app = Flask(__name__)

# Need to use Flask sessioning features

app.secret_key = 'this-should-be-something-unguessable'

# Normally, if you refer to an undefined variable in a Jinja template,
# Jinja silently ignores this. This makes debugging difficult, so we'll
# set an attribute of the Jinja environment that says to make this an
# error.

app.jinja_env.undefined = jinja2.StrictUndefined


@app.route("/")
def index():
    """Return homepage."""

    return render_template("homepage.html")


@app.route("/melons")
def list_melons():
    """Return page showing all the melons ubermelon has to offer"""

    melon_list = melons.get_all()
    return render_template("all_melons.html",
                           melon_list=melon_list)



@app.route("/melon/<int:melon_id>")    # /melon/17  show_
def show_melon(melon_id):
    """Return page showing the details of a given melon.

    Show all info about a melon. Also, provide a button to buy that melon.
    """

    melon = melons.get_by_id(melon_id)
    print melon
    return render_template("melon_details.html",
                           display_melon=melon)


@app.route("/cart")
def shopping_cart():
    """Display content of shopping cart."""

    melon_list = []

    total_cost = 0

    if "cart" in session:
        melon_id_list = session['cart']
        melon_cost = 0

        for m_id in melon_id_list:
            melon = melons.get_by_id(m_id)
            melon_cost += melon.price
            print melon
            melon_list.append(melon)

        total_cost = melon_cost

    melon_order = {}

    for melon in melon_list:
        melon_order[melon] = {
                                "price": melon.price,
                                "quantity": melon_order[melon].get("quantity", 0) + 1,
                                "sub_total": melon_order[melon]["price"] * melon_order[melon]["quantity"],
        }


    print melon_order

        # total_cost = melon_cost 

    return render_template("cart.html", melon_list=melon_list, 
                                        total_cost=total_cost)


@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """Add a melon to cart and redirect to shopping cart page.

    When a melon is added to the cart, redirect browser to the shopping cart
    page and display a confirmation message: 'Successfully added to cart'.
    """
    # On adding an item, check to see if the session contains a cart already.

    # how to avoid key error

    if session.get('cart'):
        session['cart'].append(id)
    else:
        session['cart'] = [id]
 
    flash("Melon successfully added to cart.")

    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    """Show login form."""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """Log user into site.

    Find the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session.
    """

    # TODO: Need to implement this!

    return "Oops! This needs to be implemented"


@app.route("/checkout")
def checkout():
    """Checkout customer, process payment, and ship melons."""

    # For now, we'll just provide a warning. Completing this is beyond the
    # scope of this exercise.

    flash("Sorry! Checkout will be implemented in a future version.")
    return redirect("/melons")


if __name__ == "__main__":
    app.run(debug=True)
