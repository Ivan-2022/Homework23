import os

from flask import request
from werkzeug.exceptions import BadRequest

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def get_file(file_name):
    """
    Проверяет, что файл file_name существует в папке DATA_DIR, при ошибке вернет ошибку 400
    """
    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest(description=f"файл {file_name} не был найден")
    return path_file


def construct_a_query(iterable, cmd, value):
    """
    Конструирует запрос
    """
    result = map(lambda v: v.strip(), iterable)
    if cmd == 'filter':
        result = filter(lambda v: value in v, result)
    if cmd == 'map':
        result = map(lambda v: v.split(' ')[int(value)], result)
    if cmd == 'unique':
        result = set(result)
    if cmd == 'sort':
        value = bool(value)
        result = sorted(result, reverse=value)
    if cmd == 'limit':
        result = list(result)[:int(value)]
    return result


def query():
    """
    Получает параметры запроса и file_name из request.args, при ошибке вернет ошибку 400
    Формирует результат запроса
    """
    try:
        cmd1 = request.args['cmd1']
        cmd2 = request.args['cmd2']
        value1 = request.args['value1']
        value2 = request.args['value2']
        file_name = request.args['file_name']
    except BadRequest:
        raise BadRequest(description="Ошибка запроса")
    data = get_file(file_name)
    with open(data) as f:
        result = construct_a_query(f, cmd1, value1)
        result = construct_a_query(result, cmd2, value2)
        result = '\n'.join(result)
    return result
