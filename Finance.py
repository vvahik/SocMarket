from yahoo_finance import Share

def price(name):
    dict={}
    q='qaA'
    q=q.lower()
    if(name.lower()=='apple'):
        name='AAPL'
    company=Share(name)
    dict['price']=company.get_price()
    dict['open']=company.get_open()
    return dict

