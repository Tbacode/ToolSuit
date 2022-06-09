'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-02 16:14:34
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-06 11:25:54
'''

from redis_baseconnection import BaseConnection


class TestSet(BaseConnection):

    def test_sadd(self):
        res = self.connection.sadd("zoo1", "Dog", "Cat", "Monkey")
        print(res)
        animals = ['Monkey', "Panda", "Dog"]
        res = self.connection.sadd("zoo2", *animals)
        print(res)
        members = self.connection.smembers("zoo2")
        print(members)

    def test_srem(self):
        self.connection.srem("zoo1", "Dog")
        print(self.connection.smembers("zoo1"))

    def test_course_analysis(self):
        science_stu_list = ["Stu003", "Stu033", "Stu023", "Stu013", "Stu005"]
        self.connection.sadd('science', *science_stu_list)

        english_stu_list = ["Stu003", "Stu053", "Stu023", "Stu113", "Stu004"]
        self.connection.sadd('english', *english_stu_list)

        result = self.connection.sinter('science', 'english')
        print(result)

    # def test_sadd(self):
    #     pass

    # def test_sadd(self):
    #     pass


def main():
    obj_set = TestSet()
    # obj_set.test_sadd()
    # obj_set.test_srem()
    obj_set.test_course_analysis()


if __name__ == "__main__":
    main()
