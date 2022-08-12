from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

try:
    connection = mysql.connector.connect(
        user="root",
        password="root",
        host="127.0.0.1",
        database="quickfood",
        port="8889",
    )
except:
    print("Connection failed or database does not exist")
    quit()

cursor = connection.cursor()


@app.route("/")
def adminoruser():
    return render_template("adminoruser.html")


@app.route("/admin")
def admin():
    query = "SELECT id,name, price FROM food WHERE deleted='0' ORDER BY id"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("admin/index.html", data=data)


@app.route("/admin", methods=["POST"])
def postFood():
    if request.form.get("type") == "addForm":
        name = request.form.get("name")
        price = request.form.get("price")
        query = f"INSERT INTO food(name, price) VALUES('{name}','{price}')"
    else:
        id = request.form.get("id")
        query = f"UPDATE food SET deleted = '1' WHERE food.id = '{id}'"
    cursor.execute(query)
    connection.commit()
    query = "SELECT id, name, price FROM food WHERE deleted='0' ORDER BY id"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("admin/index.html", data=data)


@app.route("/admin/<id>")
def foodPage(id):
    query = f"SELECT id, name FROM food WHERE id='{id}' ORDER BY id"
    cursor.execute(query)
    foodData = cursor.fetchall()
    query = f"SELECT tt.id, tt.name FROM tag_type tt WHERE id NOT IN(SELECT ft.tag_id FROM food_tag ft WHERE ft.food_id = '{id}')"
    cursor.execute(query)
    tagtypes = cursor.fetchall()
    query = (
        "SELECT ft.id, tt.name FROM food_tag ft "
        + "JOIN tag_type tt on tt.id = ft.tag_id "
        + f"WHERE ft.food_id='{id}' "
    )
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template(
        "admin/foodinfo.html", foodData=foodData, data=data, tagtypes=tagtypes
    )


@app.route("/admin/<id>", methods=["POST"])
def postTag(id):
    tagId = request.form.get("tagId")
    if request.form.get("type") == "addForm":
        query = f"INSERT INTO food_tag(food_id, tag_id) VALUES('{id}','{tagId}')"
    else:
        query = f"DELETE FROM food_tag WHERE id = '{tagId}'"
    cursor.execute(query)
    connection.commit()
    query = f"SELECT id, name FROM food WHERE id='{id}' ORDER BY id"
    cursor.execute(query)
    foodData = cursor.fetchall()
    query = f"SELECT tt.id, tt.name FROM tag_type tt WHERE id NOT IN(SELECT ft.tag_id FROM food_tag ft WHERE ft.food_id = '{id}')"
    cursor.execute(query)
    tagtypes = cursor.fetchall()
    query = (
        "SELECT ft.id, tt.name FROM food_tag ft "
        + "JOIN tag_type tt on tt.id = ft.tag_id "
        + f"WHERE ft.food_id='{id}' "
    )
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template(
        "admin/foodinfo.html", foodData=foodData, data=data, tagtypes=tagtypes
    )


@app.route("/admin/orders")
def orders():
    query = """SELECT o.id, f.name, c.first_name, c.last_name \
    FROM orders o \
    JOIN food f ON o.food_id = f.id \
    JOIN customer c ON o.customer_id = c.id \
    ORDER BY o.id"""
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("admin/orders.html", data=data)


@app.route("/admin/customers")
def customer():
    query = "SELECT id, first_name, last_name, orders_sum FROM customer_sum ORDER BY id"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("admin/customers.html", data=data)


@app.route("/admin/customers/<id>")
def customerInfo(id):
    query = f"SELECT first_name, last_name FROM customer WHERE id = {id}"
    cursor.execute(query)
    customer_data = cursor.fetchall()
    query = (
        """SELECT o.id, f.name, f.price \
    FROM orders o \
    JOIN food f ON o.food_id = f.id """
        + f"WHERE o.customer_id = '{id}' "
        + "ORDER BY o.id"
    )
    cursor.execute(query)
    orders_data = cursor.fetchall()
    query = (
        """SELECT SUM(f.price) FROM orders o \
        JOIN food f on f.id = o.food_id """
        + f"WHERE o.customer_id = '{id}'"
        + "GROUP BY o.customer_id "
    )
    cursor.execute(query)
    orders_sum = cursor.fetchall()
    return render_template(
        "admin/customerinfo.html",
        customer_data=customer_data,
        orders_data=orders_data,
        orders_sum=orders_sum,
    )


@app.route("/admin/tagtypes")
def tagtypes():
    query = "SELECT id, name FROM tag_type"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("/admin/tagtypes.html", data=data)


@app.route("/admin/tagtypes", methods=["POST"])
def postTagtype():
    formType = request.form.get("type")
    if formType == "addForm":
        name = request.form.get("name")
        query = f"SELECT id FROM tag_type WHERE name = '{name}'"
        cursor.execute(query)
        dupCheck = cursor.fetchall()
        if not len(dupCheck) > 0:
            query = f"INSERT INTO tag_type(name) VALUES('{name}') "
            cursor.execute(query)
            connection.commit()
    elif formType == "deleteForm":
        tagId = request.form.get("id")
        query = f"DELETE FROM food_tag WHERE tag_id = '{tagId}'"
        cursor.execute(query)
        connection.commit()
        query = f"DELETE FROM tag_type WHERE id = '{tagId}'"
        cursor.execute(query)
        connection.commit()

    query = "SELECT id, name FROM tag_type"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("/admin/tagtypes.html", data=data)


@app.route("/user")
def user():
    tags = request.args.get("tags")
    tagsList = tags.strip("[]") if tags != None else False
    data = []
    if tagsList:
        query = (
            "SELECT food_id FROM food_tag "
            f"WHERE tag_id in ({tagsList}) " + "GROUP BY food_id " +
            f"HAVING count(distinct tag_id) = {len(tagsList.split(','))}"
        )
        cursor.execute(query)
        foodids = cursor.fetchall()
        query = "SELECT id,name,price FROM food WHERE id in ({})".format(
            "'" + "','".join([x[0] for x in foodids]) + "' AND deleted='0'"
        )
    else:
        query = "SELECT id,name,price FROM food WHERE deleted='0'"
    cursor.execute(query)
    data = cursor.fetchall()
    query = "SELECT id,name from tag_type"
    cursor.execute(query)
    filters = cursor.fetchall()

    return render_template("user/index.html", data=data, filters=filters)


@app.route("/product/<id>")
def checkout(id):
    query = f"SELECT id,name,price FROM food WHERE id = {id}"
    cursor.execute(query)
    data = cursor.fetchall()
    return render_template("user/checkout.html", data=data)


@app.route("/product/<id>", methods=["POST"])
def postOrder(id):
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    query = f"SELECT id FROM customer WHERE first_name = '{first_name}' AND last_name = '{last_name}'"
    cursor.execute(query)
    data = cursor.fetchall()
    if len(data) > 0:
        customer_id = data[0][0]
    else:
        query = f"INSERT INTO customer(first_name, last_name) VALUES('{first_name}', '{last_name}')"
        cursor.execute(query)
        connection.commit()
        customer_id = cursor.lastrowid
    query = f"INSERT INTO orders(food_id, customer_id) VALUES('{id}', '{customer_id}')"
    cursor.execute(query)
    connection.commit()
    """ query = f"INSERT INTO orders(first_name, last_name) VALUES('{first_name}', '{last_name}')"
    cursor.execute(query) """
    query = f"SELECT name FROM food WHERE id = {id}"
    cursor.execute(query)
    data = cursor.fetchall()
    data.append(first_name)
    data.append(last_name)
    return render_template("/user/thankyou.html", data=data)

