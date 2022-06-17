'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-30 16:37:12
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-02 13:48:14
'''
from time import sleep
from redis_baseconnection import BaseConnection

class TestHash(BaseConnection):

    def test_hset(self):
        result = self.connection.hset('stu:0001', 'name', 'lili')
        print(result)
        is_exists = self.connection.hexists('stu:0001', 'name')
        print("is_exists:", is_exists)
        res = self.connection.hsetnx('stu:0001', 'name', 'lilili')
        print(res)

    def test_hmset(self):
        m = {
            'name': 'bob',
            'age': 21,
            'grade': 98
        }
        res = self.connection.hset('stu:0002', mapping=m)
        print(res)
        keys = self.connection.hkeys('stu:0002')
        print('keys:', keys)

    def test_hdel(self):
        res = self.connection.hdel('stu:0002', 'age')
        print(res)
        keys = self.connection.hkeys('stu:0002')
        print('keys:', keys)

    def set_user_info(self, username, password, nickname):
        user_info = {
            'username': username,
            'password': password,
            'nickname': nickname,
        }
        key = f'user:{username}'
        self.connection.hset(key, mapping=user_info)

    def get_user_info(self, username):
        key = f'user:{username}'
        user = self.connection.hmget(key, 'username', 'password', 'nickname')
        print(user)
        print('username:', user[0])
        

def main():
    obj_hash = TestHash()
    # obj_hash.test_hset()
    # obj_hash.test_hmset()
    # obj_hash.test_hdel()
    obj_hash.set_user_info("xutuo", "123", "tt")
    obj_hash.get_user_info("xutuo")


if __name__ == "__main__":
    main()