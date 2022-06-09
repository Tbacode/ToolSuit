'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-06 14:32:23
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-06 15:09:37
'''
from redis_baseconnection import BaseConnection


class TestZset(BaseConnection):

    def test_zadd(self):
        rank = {
            '徐拓': 3.25,
            '金圣尧': 3.21,
            '张梦云': 3.20,
            '周雪莹': 4.25,
            '笨猪': 2.0,
            '臭猪': 1.7,
            '傻狗': 4.1,
            '猪哥': 3.9
        }
        result = self.connection.zadd('swimming', rank)
        print(result)
        count = self.connection.zcount('swimming', 0, 100)
        print('count:', count)

    def test_zrem(self):
        result = self.connection.zrem('swimming', '徐拓')
        print(result)
        count = self.connection.zcount('swimming', 0, 100)
        print('count:', count)

    def test_zrange(self):
        result = self.connection.zrange('swimming', 0 , -1)
        print(result)
    # def test_zadd(self):
    #     pass


def main():
    obj_zset = TestZset()
    # obj_zset.test_zadd()
    # obj_zset.test_zrem()
    obj_zset.test_zrange()


if __name__ == "__main__":
    main()
