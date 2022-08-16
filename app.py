from flask import Flask
from utils import query

app = Flask(__name__)


@app.route("/perform_query", methods=['POST'])
def perform_query():
    """
    Возвращает пользователю сформированный результат запроса
    """
    result = query()
    return app.response_class(result, content_type="text/plain")


if __name__ == "__main__":
    app.run()
