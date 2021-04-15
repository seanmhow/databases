# Connects to the Oracle DB

import cx_Oracle
import config


# may need to cache this.
def db():

    conn = cx_Oracle.connect(config.username,
                             config.password,
                             config.dsn + ":" + config.port + '/orcl',
                             encoding=config.encoding)
    return conn
