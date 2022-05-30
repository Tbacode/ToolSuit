'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-05-30 15:19:17
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-05-30 16:26:38
'''

from threading import Thread
import time, random
from unicodedata import name
from redis_baseconnection import BaseConnection


class QueeueThread(Thread):

    def __init__(self, connection, team_name, max_count=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.connection = connection
        self.team_name = team_name
        self.max_count = max_count

    def run(self) -> None:
        i = 1
        while i <= self.max_count:
            member = f'{self.name}_{i}'
            print(member)
            self.connection.rpush(self.team_name, member)
            i += 1
            time.sleep(random.random())


class TestList(BaseConnection):

    def test_push(self):
        ''' lpush/rpush '''
        t = ['Amy', 'Tommy']
        self.connection.lpush('userKey', *t)
        # self.connection.lpush('userKey', 'Amy', 'Tommy')  上面的写法等同于这样
        res = self.connection.lrange('userKey', 0, -1)
        print(res)

    def test_pop(self):
        ''' lpop/rpoph '''
        res_pop = self.connection.lpop('userKey')
        print(res_pop)
        res = self.connection.lrange('userKey', 0, -1)
        print(res)

    def test_llen(self):
        ''' llen 长度 '''
        lens = self.connection.llen("userKey")
        print(lens)

    def test_queeue_up(self):
        ''' 模拟排队 '''
        team_name = "team_name"
        t1 = QueeueThread(name='T1',
                          connection=self.connection,
                          team_name=team_name,
                          max_count=10)
        t2 = QueeueThread(name='T2',
                          connection=self.connection,
                          team_name=team_name,
                          max_count=10)
        t3 = QueeueThread(name='T3',
                          connection=self.connection,
                          team_name=team_name,
                          max_count=10)

        t1.start()
        t2.start()
        t3.start()
        t1.join()
        t2.join()
        t3.join()
        llen = self.connection.llen(team_name)
        print(llen)

    # def test_push(self):
    #     ''' lpush/rpush '''
    #     pass

    # def test_push(self):
    #     ''' lpush/rpush '''
    #     pass


def main():
    obj_list = TestList()
    # obj_list.test_push()
    # obj_list.test_pop()
    # obj_list.test_llen()
    obj_list.test_queeue_up()


if __name__ == "__main__":
    main()