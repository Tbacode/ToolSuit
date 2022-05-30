# python 操作redis数据库

- ## redis-py安装及链接
  - pip install redis==3.5.3
  - 链接

    ```python
    import redis

    connection = redis.Redis(
        host = 'localhost',
        password = 'password',
        port = 6379,
        db = 0,
        decode_responses=True # 编码转义
    )
    ```

  - 连接池链接

    ```python
    pool = redis.ConnectionPool(
        host='localhost',
        password='',
        port=6379,
        db=1,
        max_connections=20
    )

    connection = redis.Redis(
        connection_pool=pool
    )
    ```
  - 关闭链接
  
    ```python
    connection.close()
    ```

- ## python 操作string
  
  ```python
  import redis


  class TestString():
      def __init__(self) -> None:
          self.connect = redis.Redis(
              host='localhost',
              port=6379,
              db=1,
              decode_responses=True # 自动进行结果转换
          )

      def test_set(self):
          user1 = self.connect.set("user1", "tuotuo")
          # 手动进行结果转换
          # user1 = self.connect.set("user1", "tuotuo").decode("utf-8")
          print(user1)

      def test_get(self):
          return self.connect.get("user1")

      def test_mset(self):
          d = {
              'mset1': "mset1",
              'mset2': "mset2",
          }
          self.connect.mset(d)

      def test_mget(self):
          res = self.connect.mget(['mset1', 'mset2'])
          print(res)

      def test_incr(self):
          self.connect.incr('age')
          age = self.connect.get('age')
          print(age)

      def test_del(self):
          self.connect.delete('user1')

      def test_append(self):
          self.connect.append('mset1', 'append')


  def main():
      obj= TestString()
      # obj.test_get()
      # obj.test_set()
      # print(obj.test_get())
      # obj.test_mset()
      # obj.test_mget()
      # obj.test_incr()
      # obj.test_del()
      obj.test_append()


  if __name__ == "__main__":
      main()
  ```

- ## python String实战
  - 这里需要使用json库对数据进行格式上的转换

    ```python
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

- ## python 操作 List
  - 
    ```python
    from redis_baseconnection import BaseConnection


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
            pass

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
        obj_list.test_llen()

    if __name__ == "__main__":
        main()
    ```

- ## python 实战 List
  - 使用多线程模拟用户抢购排队的功能
    ```python
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
    ```
- ## python 操作 Hash
  - 
    ```python
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
        

    def main():
        obj_hash = TestHash()
        # obj_hash.test_hset()
        # obj_hash.test_hmset()
        obj_hash.test_hdel()


    if __name__ == "__main__":
        main()
    ```

- ## python 实战 Hash
  - 使用Hash模拟用户注册&登录，区别于之前String的实战
  
    ```python

    ```