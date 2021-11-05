'''
 * @Descripttion : pyecharts 封装
 * @Author       : Tommy
 * @Date         : 2021-10-15 12:07:25
 * @LastEditors  : Tommy
 * @LastEditTime : 2021-11-03 19:00:22
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
        # self.mem_x = mem_x
        # self.mem_y = mem_y
        # self.cpu_x = cpu_x
        # self.cpu_y = cpu_y
        # self.fps_x = fps_x
        # self.fps_y = fps_y

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

    def set_lines_echarts(self, value_x, value_y1, y1_msg, value_y2, y2_msg, value_y3, y3_msg, value_y4, y4_msg, title_msg):
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
            .add_yaxis(y4_msg,
                       value_y4,
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

    def page_simple_layout(self, mem_x, mem_y, cpu_x, cpu_y, fps_x, fps_y):
        '''
         * @name: Tommy
         * @msg: 简单布局多表合并显示
         * @param {*}
         * @return {*}
        '''
        page = Page(layout=Page.SimplePageLayout)  # 简单布局
        page.add(
            self.set_line_echarts(mem_x, mem_y,
                                  "内存(M)", "内存"),  # 传入内存图标数据，加入page
            self.set_line_echarts(cpu_x, cpu_y,
                                  "CPU(%)", "CPU"),  # 传入CPU图标数据，加入page
            self.set_line_echarts(fps_x, fps_y,
                                  "FPS(帧)", "FPS")   # 传入FPS图标数据，加入page
        )
        # page.add(
        #     self.set_lines_echarts(mem1_x, mem1_y, "HC", mem2_y,
        #                            "PBN", mem3_y, "LITE", mem4_y, "COLOR", "内存统计")
        # )
        # page.render(self.report_path)
        return page

    def set_table_echarts(self, mem_x, mem_y, cpu_x, cpu_y, fps_x, fps_y, msg):
        tab = MyTab()
        tab.add(msg, self.set_grid_echarts(mem_x, mem_y, fps_x, fps_y))
        # tab.add(msg, self.set_line_echarts(mem_x, mem_y, "内存(M)", "内存"), self.set_line_echarts(fps_x, fps_y, "FPS(帧)", "FPS"))
        # tab.add(self.set_line_echarts(cpu_x, cpu_y, "CPU(%)", "CPU"), msg)
        # tab.add(self.set_line_echarts(fps_x, fps_y, "FPS(帧)", "FPS"), msg)
        tab.render(self.report_path)

    def set_grid_echarts(self, mem_x, mem_y, fps_x, fps_y):
        grid = Grid(init_opts=opts.InitOpts(width="1500px", height="2000px"))
        grid.add(self.set_line_echarts(mem_x, mem_y, "内存(M)", "内存"),
                 grid_opts=opts.GridOpts(pos_top="10%"))
        grid.add(self.set_line_echarts(fps_x, fps_y, "FPS(帧)", "FPS").set_global_opts(title_opts=opts.TitleOpts(
            title="wwowowow", pos_bottom="10%"), legend_opts=LegendOpts(pos_bottom="100%"), datazoom_opts=opts.DataZoomOpts()), grid_opts=opts.GridOpts(pos_bottom="10%"))
        return grid


class MyTab(Tab):
    def add(self, table_name, *args):
        for chart in args:
            chart.tab_name = table_name
            self._charts.append(chart)
            for d in chart.js_dependencies.items:
                self.js_dependencies.add(d)
        return self
