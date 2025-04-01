from pyecharts import options as opts
from pyecharts.charts import Bar, Timeline
import pandas as pd
import webbrowser


# 增加更多且更加美观的颜色以供选择
nice_colors = [
    "#FF6347",  # Tomato Red
    "#4682B4",  # Steel Blue
    "#FFD700",  # Gold
    "#90EE90",  # Pale Green
    "#FFB6C1",  # Hot Pink
    "#8A2BE2",  # Blue Violet
    "#DEB887",  # Burlywood
    "#FFA500",  # Orange Red
    "#00FFFF",  # Cyan
    "#7FFFD4",  # Aquamarine
    "#F0FFFF",  # Azure
    "#FAF0E6",  # Peach Puff
    "#FA8072",  # Light Salmon
    "#D2B48C",  # Tan
    "#D8BFD8",  # Thistle
    "#FF69B4",  # Hot Pink (another shade)
]


def create_daily_bar_chart(data, date):
    # 筛选指定日期的数据，并按地震次数降序排列，取前8个国家
    daily_data = data[data['date'] == date].sort_values('count', ascending=False).head(8)
    print(daily_data)
    countries = daily_data['country'].tolist()
    print(countries)
    counts = daily_data['count'].tolist()
    print(counts)
    max_count = max(counts) if counts else 0

    def get_label_position(params):
        # 根据国家名称长度调整标签位置
        country = params.name
        if len(country) > 5:
            return "insideLeft"
        else:
            return "insideRight"

    # 创建条形图
    bar = (
        Bar(init_opts=opts.InitOpts(width='800px', height='500px'))

    )
    bar.add_xaxis(" ")  # 一次性添加 x 轴数据
    for country, count, color in zip(countries, counts, nice_colors):

        bar.add_yaxis(
            series_name=country,  # 图例名称即为国家名称
            y_axis=[count],  # y 轴数据
            label_opts=opts.LabelOpts(
                position=get_label_position,
                formatter="{a}: {c}"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color=color)  # 设置系列颜色
        )

    bar.set_global_opts(
        title_opts=opts.TitleOpts(title=f"日期: {date.strftime('%Y-%m-%d')} 全世界地震次数排名（前8名）"),
        toolbox_opts=opts.ToolboxOpts(is_show=True),
        xaxis_opts=opts.AxisOpts(name="国家", axislabel_opts=opts.LabelOpts(rotate=-15)),
        yaxis_opts=opts.AxisOpts(name="地震次数", max_=max_count),
        legend_opts=opts.LegendOpts(orient="vertical", pos_left="right", pos_right="5%", pos_bottom="10%")
    )
    return bar


def main():
    # 读取 CSV 文件中的数据
    df = pd.read_csv('query_utf8.csv')
    df['date'] = pd.to_datetime(df['date'])

    # 按日期和国家分组，计算每个国家的地震次数
    country_counts = df.groupby(['date', 'country']).size().reset_index(name='count')

    # 创建时间线动画
    timeline = Timeline()
    for date in country_counts['date'].unique():
        bar_chart = create_daily_bar_chart(country_counts, date)
        # print(bar_chart)
        # bar_chart.render("render.html")
        # webbrowser.open_new_tab("render.html")
        timeline.add(bar_chart, time_point=date.strftime("%Y-%m-%d"))

    # 设置时间线动画的参数
    timeline.add_schema(
        play_interval=1000,
        is_auto_play=True,
        is_timeline_show=True,
        is_loop_play=True,
        label_opts=opts.LabelOpts(
            is_show=True,
            position="bottom",
            color="#333",
            font_size=12
        )
    )

    # 渲染时间线动画为 HTML 文件
    timeline.render("earthquake_geo_timeline.html")


if __name__ == "__main__":
    main()
    webbrowser.open_new_tab("earthquake_geo_timeline.html")