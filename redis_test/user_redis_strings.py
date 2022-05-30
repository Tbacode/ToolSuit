'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-26 23:55:03
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-30 15:07:37
'''
import json
from redis_baseconnection import BaseConnection


class TestString(BaseConnection):

    def test_set(self, key, value):
        user1 = self.connection.set(key, value)
        # 手动进行结果转换
        # user1 = self.connection.set("user1", "tuotuo").decode("utf-8")
        print(user1)

    def test_get(self, key):
        return self.connection.get(key)

    def test_mset(self):
        d = {
            'mset1': "mset1",
            'mset2': "mset2",
        }
        self.connection.mset(d)

    def test_mget(self):
        res = self.connection.mget(['mset1', 'mset2'])
        print(res)

    def test_incr(self):
        self.connection.incr('age')
        age = self.connection.get('age')
        print(age)

    def test_del(self):
        self.connection.delete('user1')

    def test_append(self):
        self.connection.append('mset1', 'append')

    def register(self, username, password, nickname):
        key = f'username:{username}'
        value = {
            'username': username,
            'password': password,
            'nickname': nickname,
        }
        value_json = json.dumps(value)
        self.test_set(key, value_json)

    def login(self, username, password):
        key = f'username:{username}'
        res = self.test_get(key)
        if res is None:
            print("用户不存在")
            return None
        res_dict = json.loads(res)
        print(res_dict)
        if password != res_dict['password']:
            print("用户名和密码不正确")
            return None
        print("Login Success")


def main():
    obj = TestString()
    # obj.test_get()
    # obj.test_set()
    # print(obj.test_get())
    # obj.test_mset()
    # obj.test_mget()
    # obj.test_incr()
    # obj.test_del()
    # obj.test_append()
    # obj.register('tuotuo', '123456', 'tt')
    obj.login('tuotuo1', '12')


if __name__ == "__main__":
    main()