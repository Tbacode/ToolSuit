'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-30 14:01:35
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-30 15:05:38
'''
import redis


class BaseConnection():

    def __init__(self):
        pool = redis.ConnectionPool(
            host='localhost',
            password='',
            port=6379,
            db=1,
            max_connections=20,
            decode_responses=True  # 自动进行结果转换
        )

        self.connection = redis.Redis(connection_pool=pool)

    def __del__(self):
        try:
            self.connection.close()
        except Exception as ex:
            print(ex)
