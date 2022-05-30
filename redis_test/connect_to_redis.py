'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-26 17:47:59
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-30 14:45:23
'''
import redis


def get_connection():
    '''直接链接数据库'''
    connection = redis.Redis(host='localhost', password='', port=6379, db=1)
    return connection


def get_connection_by_pool():
    '''使用连接池'''
    pool = redis.ConnectionPool(host='localhost',
                                password='',
                                port=6379,
                                db=1,
                                max_connections=20)

    connection = redis.Redis(connection_pool=pool)
    return connection


def close_connection(connection):
    '''关闭链接'''
    connection.close()


if __name__ == "__main__":
    connect = get_connection()
    connect.set('key', 'value')
    close_connection(connect)

    connect2 = get_connection_by_pool()
    res = connect2.set('key2', 'value2')
    print(res)
    close_connection(connect2)