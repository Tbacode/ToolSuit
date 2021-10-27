'''
 * @Descripttion : pyecharts 封装
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:07:25
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-10-25 16:08:51
'''
from pyecharts.charts import Line, Page
from pyecharts import options as opts
from pyecharts.globals import ThemeType


class UsingMyecharts(object):
    def __init__(self, report_path, mem_x, mem_y, cpu_x, cpu_y, fps_x, fps_y):
        self.report_path = report_path
        self.mem_x = mem_x
        self.mem_y = mem_y
        self.cpu_x = cpu_x
        self.cpu_y = cpu_y
        self.fps_x = fps_x
        self.fps_y = fps_y

    def set_line_echarts(self, value_x, value_y, y_msg, title_msg):
        '''
         * @name: Tommy
         * @msg: 
         * @param {x轴数据，y轴数据}
         * @return {返回一个line类型图表类型}
        '''
        c = (
            Line(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
            .add_xaxis(value_x)
            .add_yaxis(y_msg,
                       value_y,
                       symbol="emptyCircle",
                       is_smooth=True,
                       label_opts=opts.LabelOpts(is_show=False),

                       markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(type_='max', name='峰值'),
                                                              opts.MarkPointItem( name='平均值', type_='average'),
                                                              opts.MarkPointItem(name='谷值', type_='min')])
                       )

            .set_global_opts(title_opts=opts.TitleOpts(title=title_msg), datazoom_opts=opts.DataZoomOpts())
        )
        return c

    def page_simple_layout(self):
        '''
         * @name: Tommy
         * @msg: 简单布局多表合并显示
         * @param {*}
         * @return {*}
        '''
        page = Page(layout=Page.SimplePageLayout)  # 简单布局
        page.add(
            self.set_line_echarts(self.mem_x, self.mem_y,
                                  "内存(M)", "内存"),  # 传入内存图标数据，加入page
            self.set_line_echarts(self.cpu_x, self.cpu_y,
                                  "CPU(%)", "CPU"),  # 传入CPU图标数据，加入page
            self.set_line_echarts(self.fps_x, self.fps_y,
                                  "FPS(帧)", "FPS")   # 传入FPS图标数据，加入page
        )
        page.render(self.report_path)
