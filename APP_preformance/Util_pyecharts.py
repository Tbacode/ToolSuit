'''
 * @Descripttion : pyecharts 封装
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:07:25
 * @LastEditors  : Tommy
 * @LastEditTime : 2022-03-02 18:18:07
'''
from pyecharts import charts
from pyecharts.charts import Line, Page, Tab
from pyecharts import options as opts
from pyecharts.charts.composite_charts.grid import Grid
from pyecharts.globals import ThemeType
from pyecharts.options.global_options import DataZoomOpts, LegendOpts


class UsingMyecharts(object):
    def __init__(self, report_path):
        self.report_path = report_path

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
                                                              opts.MarkPointItem(
                                                                  name='平均值', type_='average'),
                                                              opts.MarkPointItem(name='谷值', type_='min')])
                       )

            .set_global_opts(title_opts=opts.TitleOpts(title=title_msg), datazoom_opts=opts.DataZoomOpts())
        )
        return c

    def set_lines_echarts(self, value_x, value_y1, y1_msg, value_y2, y2_msg, value_y3, y3_msg, title_msg):
        '''
         * @name: Tommy
         * @msg:
         * @param {x轴数据，y轴数据}
         * @return {返回一个line类型图表类型}
        '''
        c = (
            Line(init_opts=opts.InitOpts(theme=ThemeType.ESSOS))
            .add_xaxis(value_x)
            .add_yaxis(y1_msg,
                       value_y1,
                       symbol="emptyCircle",
                       is_smooth=True,
                       label_opts=opts.LabelOpts(is_show=False),

                       markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(type_='max', name='峰值'),
                                                              opts.MarkPointItem(
                                                                  name='平均值', type_='average'),
                                                              opts.MarkPointItem(name='谷值', type_='min')])
                       )
            .add_yaxis(y2_msg,
                       value_y2,
                       symbol="emptyCircle",
                       is_smooth=True,
                       label_opts=opts.LabelOpts(is_show=False),

                       markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(type_='max', name='峰值'),
                                                              opts.MarkPointItem(
                                                                  name='平均值', type_='average'),
                                                              opts.MarkPointItem(name='谷值', type_='min')])
                       )
            .add_yaxis(y3_msg,
                       value_y3,
                       symbol="emptyCircle",
                       is_smooth=True,
                       label_opts=opts.LabelOpts(is_show=False),

                       markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(type_='max', name='峰值'),
                                                              opts.MarkPointItem(
                                                                  name='平均值', type_='average'),
                                                              opts.MarkPointItem(name='谷值', type_='min')])
                       )
            # .add_yaxis(y4_msg,
            #            value_y4,
            #            symbol="emptyCircle",
            #            is_smooth=True,
            #            label_opts=opts.LabelOpts(is_show=False),

            #            markpoint_opts=opts.MarkLineOpts(data=[opts.MarkPointItem(type_='max', name='峰值'),
            #                                                   opts.MarkPointItem(
            #                                                       name='平均值', type_='average'),
            #                                                   opts.MarkPointItem(name='谷值', type_='min')])
            #            )

            .set_global_opts(title_opts=opts.TitleOpts(title=title_msg), datazoom_opts=opts.DataZoomOpts())
        )
        return c

    def page_simple_layout(self, mem1_x, mem1_y, mem2_x, mem2_y, mem3_x, mem3_y):
        '''
         * @name: Tommy
         * @msg: 简单布局多表合并显示
         * @param {*}
         * @return {*}
        '''
        page = Page(layout=Page.SimplePageLayout)  # 简单布局
        page.add(
            self.set_line_echarts(mem1_x, mem1_y,
                                  "FPS(帧)", "TC_FPS"),  # 传入内存图标数据，加入page
            self.set_line_echarts(mem2_x, mem2_y,
                                  "FPS(帧)", "TCP_FPS"),  # 传入CPU图标数据，加入page
            self.set_line_echarts(mem3_x, mem3_y,
                                  "FPS(帧)", "HC_FPS")   # 传入FPS图标数据，加入page
        )
        # page.add(
        #     self.set_lines_echarts(mem_x, mem_y, "pro_20211202", cpu_y,
        #                            "pbn_20211026", fps_y, "hc_20211026", "内存统计")
        # )
        page.render(self.report_path)
        # return page

    def page_simple_layout2(self, mem_x, mem_y):
        page = Page(layout=Page.SimplePageLayout)
        page.add(
            self.set_line_echarts(mem_x, mem_y, "内存(M)", "广告内存")
        )
        page.render(self.report_path)
