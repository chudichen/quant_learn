import requests
import anyjson


def get_hot_stock_from_sina():
    """
    从新浪得到热门数据
    """
    html = str(requests.get(
        'https://ssl-data.sina.com.cn/api/openapi.php/WeiboReferService.getListSymbol?code=CNHOUR6&callback=var%20AHM=').content, 'utf-8')
    t = html.index('(')
    f = html.index(')')
    n = html[t + 1:f]
    h = anyjson.deserialize(n)
    data = h['result']['data']
    hot_stock = {}
    for x in data:
        if x['SYMBOL'].find('sh') > -1:
            x['SYMBOL'] = x['SYMBOL'].replace('sh', '') + '.XSHG'
        if x['SYMBOL'].find('sz') > -1:
            x['SYMBOL'] = x['SYMBOL'].replace('sz', '') + '.XSHE'
        hot_stock[x['NAME']] = x['SYMBOL']
    return hot_stock
