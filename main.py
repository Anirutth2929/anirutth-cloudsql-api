from flask import Flask, jsonify, request
import pymysql
import os

app = Flask(__name__)

@app.route("/users", methods=["GET"])
def get_user_by_name():
    name = request.args.get("name")

    if not name:
        return {"error": "name query parameter is required"}, 400

    try:
        conn = pymysql.connect(
            user=os.environ["DB_USER"],
            password=os.environ["DB_PASSWORD"],
            unix_socket=f"/cloudsql/{os.environ['INSTANCE_CONNECTION_NAME']}",
            database=os.environ["DB_NAME"]
        )

        cursor = conn.cursor(pymysql.cursors.DictCursor)

        query = "SELECT id FROM users WHERE name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        if result:
            return jsonify(result), 200
        else:
            return {"message": "User not found"}, 404

    except Exception as e:
        return {"error": str(e)}, 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
