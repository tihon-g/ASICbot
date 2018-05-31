import requests
import json
#from main import write_json
#from flask import jsonify

url = 'https://blockchain.info/rawaddr/'
# кошельки==адреса по всем монетам
addr = [('tihon',"3QKZkzVMwwWQC1mqCxbLBKwjf9q9hFHMSg",""),
        ('mavr' ,"17TaVLtJCgq3Tb29g7jaBQEu3t3D88Kxk2","")]

coins = [("BTC",'bitcoin',"1", 10**8), ("LTC",'litecoin',"2", 1)] #, ("DSH", 'dash',"131")]

def get_price(id):
    url = 'https://api.coinmarketcap.com/v2/ticker/'+id
    r = requests.get(url).json()
    price = r['data']['quotes']['USD']['price']
    return price

def get_addr_info(owner, coin):
    r = requests.get(url+addr[owner][1+coin]).json()
    res = {
        "owner"  : addr[owner][0],
        "addr"   : addr[owner][1+coin][0],
        "balance": (r['final_balance'])/coins[coin][3],
        "n_tx"   : r['n_tx'] }
    return res

def get_pool_info():
    res = []
    for ticker, name, id, k in coins:
        try:
            r = requests.get('http://api.f2pool.com/%s/madskills' % name).json()
            #print (write_json(r, 'f2.json'))
            c_res = {
                "coin"          : ticker,
                "coin_id"       : id,
                "hashrate"      : r['hashrate'],
                "workers"       : r['worker_length'],
                "online"        : r['worker_length_online'],
                "rate24"        : r['hashrate_history'],
    #            "pay_history"   : r['payout_history'],
                "value24"       : r['value_last_day']
                }
            if c_res != None:
                res += [c_res]
        except:
            pass
        else:
            pass
    return res #json.dumps(res)

def get_wallets_info():
    res = ""
    # сначала цикл по монетам
    for i_coin, (ticker, name, id, k) in enumerate(coins):
        rate = get_price(id)
        res += '{} курс: {}usd\n'.format(ticker, round(rate))
        #  затем цикл по кошелькам
        for owner, w in enumerate(addr):
            if len(w[1+i_coin])>0: # адрес не пуст
                info = get_addr_info(owner, i_coin)
                res += '[{}] balance={}, tx={}\n'.format (w[0], info['balance'], info['n_tx'])
                res += 'итого: = %s USD\n' % str(round(info['balance'] * rate))
            else:
                res += '[{}] нет кошелька - нет денег!\n'.format (w[0])
        res+='\n'
    return res

def hashrate_tostr(h):
    if h>=10*13:
        return '{} TH/s'.format(round((h*1.)/10**12,1))
    elif h>=10*10:
        return '{} GH/s'.format(round((h*1.)/10**9,2))
    return '{} MH/s'.format(round((h*1.)/10**6,3))


def get_miners_info():
    res=''
    for i_coin, miners in enumerate(get_pool_info()):
        res+='[{}] hasrate = {} online {}/{}\n'.format (miners['coin'],
            hashrate_tostr(miners['hashrate']),miners['online'],miners['workers'])
        if miners['workers']>0:
#            res+='в среднем за сутки: {}, получено: {}\n'.format(hashrate_tostr(miners['rate24']),
            res+='в среднем за сутки: {}={}USD\n'.format(round(miners['value24'],4),
                round(miners['value24']*get_price(miners['coin_id'])))
    return res

def get_state_info():
    #r = requests.get('http://api.f2pool.com/bitcoin/madskills').json()
    #return r['hashrate']
    #return get_addr_info(0)['balance'] + ' ' + get_addr_info(1)['balance']  + ' ' + get_price("1")
    #print(get_pool_info())
    return get_price("1")
