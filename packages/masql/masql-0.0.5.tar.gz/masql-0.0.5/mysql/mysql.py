#!/usr/bin/python3
# -*- encoding: utf-8 -*-


import pymysql
import traceback


class Mysql(object):
    def __init__(self, batch_size=10000, logger=None, *args, **kwargs):
        """
            Representation of a socket with a mysql server.

            The proper way to get an instance of this class is to call
            connect().

            Establish a connection to the MySQL database. Accepts several
            arguments:

            :param host: Host where the database server is located
            :param user: Username to log in as
            :param password: Password to use.
            :param database: Database to use, None to not use a particular one.
            :param port: MySQL port to use, default is usually OK. (default: 3306)
            :param bind_address: When the client has multiple network interfaces, specify
                the interface from which to connect to the host. Argument can be
                a hostname or an IP address.
            :param unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
            :param read_timeout: The timeout for reading from the connection in seconds (default: None - no timeout)
            :param write_timeout: The timeout for writing to the connection in seconds (default: None - no timeout)
            :param charset: Charset you want to use.
            :param sql_mode: Default SQL_MODE to use.
            :param read_default_file:
                Specifies  my.cnf file to read these parameters from under the [client] section.
            :param conv:
                Conversion dictionary to use instead of the default one.
                This is used to provide custom marshalling and unmarshaling of types.
                See converters.
            :param use_unicode:
                Whether or not to default to unicode strings.
                This option defaults to true for Py3k.
            :param client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
            :param cursorclass: Custom cursor class to use.
            :param init_command: Initial SQL statement to run when connection is established.
            :param connect_timeout: Timeout before throwing an exception when connecting.
                (default: 10, min: 1, max: 31536000)
            :param ssl:
                A dict of arguments similar to mysql_ssl_set()'s parameters.
            :param read_default_group: Group to read from in the configuration file.
            :param compress: Not supported
            :param named_pipe: Not supported
            :param autocommit: Autocommit mode. None means use server default. (default: False)
            :param local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
            :param max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
                Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
            :param defer_connect: Don't explicitly connect on contruction - wait for connect call.
                (default: False)
            :param auth_plugin_map: A dict of plugin names to a class that processes that plugin.
                The class will take the Connection object as the argument to the constructor.
                The class needs an authenticate method taking an authentication packet as
                an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
                (if no authenticate method) for returning a string from the user. (experimental)
            :param server_public_key: SHA256 authenticaiton plugin public key value. (default: None)
            :param db: Alias for database. (for compatibility to MySQLdb)
            :param passwd: Alias for password. (for compatibility to MySQLdb)
            :param binary_prefix: Add _binary prefix on bytes and bytearray. (default: False)

            See `Connection <https://www.python.org/dev/peps/pep-0249/#connection-objects>`_ in the
            specification.
        """
        kw = {'host': 'localhost',
              'user': 'root',
              'password': '1234',
              'charset': 'utf8mb4',
              'cursorclass': pymysql.cursors.DictCursor}
        if kwargs:
            kw.update(kwargs)
        kwargs = kw
        self.con = pymysql.connect(*args, **kwargs)
        self.batch_size = batch_size
        self.logger = logger

    @staticmethod
    def __is_select(sql):
        return True if 'SELECT' in sql.upper() else False

    def execute_sql(self, sql):
        """
        execute raw sql
        执行原生sql语句(支持增删改查，批量查暂不支持)
        :param sql: <str/list>
        :return: <int> effect row number 影响行数 <tuple> query result 查询语句结果
        :todo: 解决多个select的sql的限制
        """
        current_sql = ''
        try:
            result = None
            select_flag = False
            with self.con.cursor() as cursor:
                if isinstance(sql, list):
                    for i in sql:
                        current_sql = i
                        select_flag = self.__is_select(i)
                        result = cursor.execute(i)
                else:
                    current_sql = sql
                    select_flag = self.__is_select(sql)
                    result = cursor.execute(sql)
            self.con.commit()
            if select_flag:
                return cursor.fetchall()
            return result
        except Exception:
            if self.logger:
                self.logger.error('sql : %s\nError Message : %s' % (
                    current_sql, traceback.format_exc()))
            return 0

    @staticmethod
    def __batch_slice(s, step):
        """
        cut into slices
        切分batch
        :param s: <list> array waitting for cut 待切数组
        :param step: <int> step length 步长
        :return:
        """
        res = []
        quotient = len(s) // step
        if quotient:
            for index in range(quotient):
                res.append(s[index:index + step])
        else:
            res.append(s)
        return res

    def __multi_line_parser(self, table, sql, *args, **kwargs):
        """
        multi-line sql parser
        多行sql语法解析器
        :param table: <str> table name 表名
        :param sql: <str>
        :param args: columns key-value
        :param kwargs: columns key-value
        :return: <list>
        """
        res = []
        if args:
            columns_sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_name = '%s'" % table
            columns = [i['COLUMN_NAME'] for i in self.execute_sql(columns_sql)]
            batch = self.__batch_slice(args, self.batch_size)
            for args in batch:
                if isinstance(args[0], dict):
                    for arg in args:
                        res.append(
                            self.__single_line_parser(sql, item=arg))
                elif isinstance(args[0], list):
                    for arg in args:
                        _columns = columns[:len(arg)]
                        res.append(
                            self.__single_line_parser(sql, item=dict(
                                zip(_columns, arg))))
                else:
                    _columns = columns[:len(args)]
                    res.append(self.__single_line_parser(sql, item=dict(
                        zip(_columns, args))))
        if kwargs:
            res.append(self.__single_line_parser(sql, item=kwargs))
        return res

    @staticmethod
    def __single_line_parser(sql, item):
        """
        single line sql parser
        单-行sql语法解析器
        :param sql: <str>
        :param item: <dict>
        :return: <str>
        """
        columns = ''
        values = ''
        for key, value in item.items():
            columns += '`%s`,' % key
            if isinstance(value, int):
                values += '%s,' % value
            else:
                values += '\'%s\',' % value
        columns = columns.strip(',')
        values = values.strip(',')
        sql = sql.format(columns=columns, values=values)
        return sql

    def insert(self, table, *args, **kwargs):
        """
        sql insert
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return:
        """
        static = "INSERT INTO `%s` ({columns}) VALUES ({values})" % table
        sql = self.__multi_line_parser(table, static, *args, **kwargs)
        return self.execute_sql(sql)

    def insert_ignore(self, table, *args, **kwargs):
        """
        sql insert ignore
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return:
        """
        static = "INSERT IGNORE INTO `%s` ({columns}) VALUES ({values})" % table
        sql = self.__multi_line_parser(table, static, *args, **kwargs)
        return self.execute_sql(sql)

    def replace(self, table, *args, **kwargs):
        """
        sql replace
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return:
        """
        static = "REPLACE INTO `%s` ({columns}) VALUES ({values})" % table
        sql = self.__multi_line_parser(table, static, *args, **kwargs)
        return self.execute_sql(sql)

    def delete(self, table, *args, **kwargs):
        """
        sql delete
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return:
        """
        static = "DELETE FROM `%s`  WHERE {columns} = {values}" % table
        sql = self.__multi_line_parser(table, static, *args, **kwargs)
        return self.execute_sql(sql)

    def select(self, table, *args, **kwargs):
        """
        sql select
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return: <tuple> query result
        """
        static = 'SELECT * FROM %s' % table
        if args or kwargs:
            static = 'SELECT * FROM %s WHERE {columns} = {values}' % table
        sql = self.__multi_line_parser(table, static, *args, **kwargs)
        sql = sql[0]
        return self.execute_sql(sql)

    def truncate(self, table):
        """
        sql truncate
        :param table: <str> table name 表名
        :param args: columns key-value
        :param kwargs: columns key-value
        :return: int
        """
        static = "TRUNCATE TABLE %s" % table
        return self.execute_sql(static)

    def __sql_parser(self, sql_template, *args, **kwargs):
        """
        sql parser
        Returns the exact string that is sent to the database by calling the
        execute() method.
        sql 语法解析器
        调用execute()方法时执行该解析器，为execute()方法提供方便
        :param sql_template: sql template sql模版
        :param args: columns key-value
        :param kwargs: columns key-value
        :return: <list>
        """
        res = []
        if args:
            if isinstance(args[0], dict) and '{' in sql_template:
                for i in args:
                    res.append(sql_template.format(**i))
            elif not isinstance(args[0], list) and '%s' in sql_template:
                res.append(sql_template % args)
            elif isinstance(args[0], list) and '%s' in sql_template:
                for i in args:
                    res.append(sql_template % tuple(i))
            return res
        if kwargs:
            res.append(sql_template.format(**kwargs))
            return res

    def execute(self, sql_template, *args, **kwargs):
        sql = self.__sql_parser(sql_template, *args, **kwargs)
        self.execute_sql(sql)

    def close(self):
        return self.con.close()
