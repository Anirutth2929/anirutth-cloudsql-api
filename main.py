from flask import Flask, jsonify
import os
import pymysql

app = Flask(__name__)


@app.route("/users", methods=["GET"])
def get_users():
    # Read config from ENV variables
    db_user = os.environ["DB_USER"]
    db_password = os.environ["DB_PASSWORD"]
    db_name = os.environ["DB_NAME"]
    instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]

    # Connect to Cloud SQL
    connection = pymysql.connect(
        user=db_user,
        password=db_password,
        unix_socket=f"/cloudsql/{instance_connection_name}",
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    cursor = connection.cursor()
    cursor.execute("SELECT id, name, email FROM users")
    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(rows)


@app.route("/")
def health():
    return {"status": "API is running"}


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
