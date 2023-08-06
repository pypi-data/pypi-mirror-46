import logging
import re
import typing

import pg8000


class DbException(Exception):
    """
    Exception used to report issues related
    to Database Connectivity
    """


def create_db_connection(
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
        timeout: int,
        ssl: bool
) -> pg8000.Connection:
    """
    Creates a database connection session.
    In case the application is running locally, it will take the OS
    environment variables for the localhost and port.
    If the application is running locally, you are supposed to have
    a local forwarding of the database port into a localhost/port
    :param host:
    :param port:
    :param database:
    :param user:
    :param password:
    :param timeout:
    :param ssl:
    :return:
    """
    try:
        logging.getLogger().info(
            "Connecting to the database %s port: %s",
            host, port
        )
        return pg8000.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password,
            timeout=timeout,
            ssl=ssl,
        )
    except pg8000.InterfaceError:
        logging.getLogger().error(
            "Could not connect to %s as %s",
            host, user
        )
        raise DbException


def format_query(args: tuple, sql_file: str) -> str:
    """
    This function will match arguments sequentially
    with the parameters of a SQL file
    :param args:
    :param sql_file:
    :return:
    """
    def _replace(match):
        i = int(match.group(0)[1:]) - 1
        return f"'{args[i]}'" if i < len(args) else match.group(0)

    return re.sub(r"\$[1-9][0-9]*", _replace, sql_file)


def get_column_name(cursor: pg8000.Cursor) -> list:
    """
    Gets the Column name of an executed query
    :param cursor:
    :return:
    """
    return [row[0].decode("utf-8") for row in cursor.description]


def map_results_into_object(
        cursor: pg8000.Cursor,
        query: str,
        args: any,
        type_object: typing.Type
) -> list:
    """
    :param cursor:
    :param query:
    :param args:
    :param type_object:
    :return:
    """
    cursor.execute(query, args)
    columns = get_column_name(cursor)
    return [
        type_object(**{
            column[1]: row[column[0]]
            for column in enumerate(columns)
        }) for row in list(cursor.fetchall())
    ]


def execute_query(
        db_session: pg8000.Connection,
        type_object: typing.Type,
        sql_file: str,
        args: any = None,
        msg_id: str = None,
) -> list:
    """
    With a given sql_file and arguments sequentially ordered according to the sql_file,
    this function will execute a query to the database and return a list of objects
    of type_object
    :param db_session:
    :param type_object:
    :param sql_file:
    :param args:
    :param msg_id:
    :return:
    """
    try:
        file = open(sql_file, "r")
        query = file.read()
        file.close()
        cursor = db_session.cursor()
        return map_results_into_object(
            cursor=cursor,
            query=query,
            args=args,
            type_object=type_object,
        )
    except pg8000.DatabaseError as e:
        msg = (
            f'{msg_id} '
            f'Unexpected error: {e} '
            f'for sql file {sql_file} '
            f'and args {args}'
        )
        logging.getLogger().error(msg)
        db_session.rollback()
        db_session.close()
        raise DbException
    except IOError as e:
        msg = (
            f'{msg_id} '
            f'Unexpected error: {e} '
            f'for sql file {sql_file} '
            f'and args {args}'
        )
        logging.getLogger().error(msg)
        raise IOError


def commit(
        db_session: pg8000.Connection,
        msg_id: str = None,
):
    """
    Commits the Database
    :param db_session:
    :param msg_id:
    :return:
    """
    try:
        db_session.commit()
        db_session.close()
    except pg8000.DatabaseError as e:
        msg = (
            f'{msg_id} '
            f'Unexpected error: {e} '
            f'while trying to do a '
            f'db commit'
        )
        logging.getLogger().error(msg)
        db_session.rollback()
        db_session.close()
        raise DbException
