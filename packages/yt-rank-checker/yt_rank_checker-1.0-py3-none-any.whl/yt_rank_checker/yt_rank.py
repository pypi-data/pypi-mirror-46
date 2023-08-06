import time
import json

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pyecharts.charts import Line
from pyecharts import options as opts
import arrow

from utils import search_query

def yt_rank(channel, iterator_value=4):
    channel_name = channel
    try:
        chrome_options = Options()

        chrome_options.add_argument("--headless")
        chrome_options.add_argument('log-level=3')
        driver = webdriver.Chrome(chrome_options=chrome_options)
        driver.maximize_window()

    except Exception as e:
        print('error opening selenium browser')
        raise e

    with open("keywords.json", "r") as file:
        try:
            data_dict = json.load(file)
        except json.JSONDecodeError:
            print('file is empty')
            data_dict = {}

    #insert keywords as a list of strings
    keyword_list = ['jupyter notebook tutorial 2019']

    for keyword in keyword_list:
        url = search_query(keyword)
        driver.get(url)

        #change iterator count to increase how many pages deep it will check, default is 4 which looks at the top 100 results in YT search
        iterator_count = iterator_value
        iterator_tracker = 0
        keyword_rank = ''
        for _ in range(iterator_count):
            break_early = False

            channel_name_list = driver.find_elements_by_xpath('//*[@id="byline"]')

            for i, channel in enumerate(channel_name_list):
                if channel.text == channel_name:
                    print('video ranks for keyword at position:', i + 1)
                    keyword_rank = (i + 1)
                    break_early = True
                    break
            if break_early:
                print('keyword found, stopping scroll loop')
                break

            driver.execute_script('window.scrollTo(0, document.documentElement.scrollHeight)')
            print('scrolling')
            iterator_tracker += 1

            if iterator_tracker >= iterator_count:
                print('keyword not found in top', ((iterator_count + 1) * 20), ' results')
                keyword_rank = 'NR'

            time.sleep(2)
        current_date = arrow.utcnow()
        date_str = current_date.format('M/D/YY')

        key_list = list(data_dict.keys())

        if keyword in key_list:
            print('keyword already exists, checking for date')
            date_list = data_dict[keyword]['dates']
            if date_str in date_list:
                print('date present, overriding')
                loc = date_list.index(date_str)
                print(loc)
                print('before value: ', data_dict[keyword]['ranks'][loc] )

                data_dict[keyword]['ranks'][loc] = keyword_rank
                print('after value: ', data_dict[keyword]['ranks'][loc] )
            else:
              #date not in list, just append
              print('appending new data to list')
              data_dict[keyword]['dates'].append(date_str)
              data_dict[keyword]['ranks'].append(keyword_rank)

        else:
            #create new dict key
            print('creating new keyword')
            data_dict[keyword] = {
              'dates': [date_str],
              'ranks': [keyword_rank]
            }

    try:
        with open("keywords.json", 'w') as file:
            json.dump(data_dict, file)
    except Exception as e:
        print('error saving data to file')
        driver.close()
        raise e
    
    print('done searching')
    driver.close()

    with open("keywords.json", "r") as file:
        data_dict = json.load(file)

    line = Line()

    for k,v in data_dict.items():
        line.add_xaxis(v['dates'])
        line.add_yaxis(k,v['ranks'], 
        linestyle_opts=opts.LineStyleOpts( width=2),
        itemstyle_opts=opts.ItemStyleOpts(),
        label_opts=opts.LabelOpts(font_size=18 ),
        tooltip_opts=opts.TooltipOpts()
        )

    line.set_global_opts(legend_opts=opts.LegendOpts(is_show=True))
    line.render()