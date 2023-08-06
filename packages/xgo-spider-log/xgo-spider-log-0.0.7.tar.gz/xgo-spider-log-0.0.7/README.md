### 介绍

本项目主要封装了几个爬虫监控方法

### 安装

```
pipenv install xgo-spider-log
```

### 使用

```python
from xgo_spider_log import spider_start, spider_stop, queue_remaining, crawl_content, general_log

spider_start()
crawl_content('ahh', 1)
queue_remaining('ahh', 1)
general_log({'ahh': 111})
spider_stop()
```