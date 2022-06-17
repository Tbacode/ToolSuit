'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-17 18:04:33
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-17 18:04:33
'''
'''
 * @Descripttion : 
 * @Author       : Tommy
 * @Date         : 2022-06-14 15:59:12
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-06-14 17:37:40
'''
'''
视图函数中
    1.在views中，根据自己的情况获得数据
    queryset = PhoneNumber.objects.filter(**data_dict).order_by("level")
    2.实例化分页组件对象
    pageNationObject = PageNation(request, queryset)
    3.返回前端页面数据
    return render(request, 'phone_list.html', {
            "page_queryset": pageNationObject.page_queryset,
            "value": value,
            "page_string": pageNationObject.html()
        })

前端
    {% for obj in page_queryset%}
        ...
    {% endfor %}
    <ul class="pagination" style="float: right;">
        {{ page_string }}     
    </ul>
'''

import copy
from django.utils.safestring import mark_safe


class PageNation():
    """ 自定义分页组件 """

    def __init__(self, request, queryset, page_size=15) -> None:
        self.page = int(request.GET.get("page", 1))
        self.page_size = page_size
        self.start = (self.page - 1) * 15
        self.end = self.page * 15
        self.page_queryset = queryset[self.start:self.end]
        total_count = queryset.count()
        total_page_count, div = divmod(total_count, 15)
        if div:
            total_page_count += 1
        self.total_page_count = total_page_count
        self.query_dict = copy.deepcopy(request.GET)
        self.query_dict._mutable = True  # 修改参数，变为可拼接的querydict

    def html(self):
        # 数据库中，数据分页小于11页
        if self.total_page_count <= 11:
            start_page = 1
            end_page = self.total_page_count
        else:
            # 小极值的处理
            if self.page <= 5:
                start_page = 1
                end_page = 11
            else:
                # 大极值的处理
                if self.page + 5 > self.total_page_count:
                    start_page = self.total_page_count - 10
                    end_page = self.total_page_count
                else:
                    start_page = self.page - 5
                    end_page = self.page + 5

        page_str_list = []
        # 首页
        self.query_dict.setlist('page', [1])
        page_str_list.append('<li><a href="?{}">首页</a></li>'.format(
            self.query_dict.urlencode()))
        # 上一页
        if self.page > 1:
            self.query_dict.setlist('page', [self.page - 1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist('page', [1])
            prev = '<li><a href="?{}">上一页</a></li>'.format(
                self.query_dict.urlencode())

        page_str_list.append(prev)
        for i in range(start_page, end_page + 1):
            self.query_dict.setlist('page', [i])
            if i != self.page:
                ele = '<li><a href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            else:
                ele = '<li class="active"><a href="?{}">{}</a></li>'.format(
                    self.query_dict.urlencode(), i)
            page_str_list.append(ele)

        # 下一页
        if self.page < self.total_page_count:
            self.query_dict.setlist('page', [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
        else:
            self.query_dict.setlist('page', [self.total_page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(
                self.query_dict.urlencode())
        page_str_list.append(prev)

        # 尾页
        self.query_dict.setlist('page', [self.total_page_count])
        page_str_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))

        serch_string = '''
        <div style="float: right; width:100px;">
            <form method='get'>
                <div class="input-group">
                    <input type="text" name="page" class="form-control" placeholder="跳转">
                        <span class="input-group-btn">
                        <button class="btn btn-default" type="submit">
                            go
                        </button>
                </div>
            </form>
        </div>
        '''
        page_str_list.append(serch_string)

        return mark_safe("".join(page_str_list))
