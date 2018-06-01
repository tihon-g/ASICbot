import requests
import json

APIurl = 'https://chain.so/api/v2/'

# кошельки, точнее адреса по всем монетам
address = [('tihon',"3QKZkzVMwwWQC1mqCxbLBKwjf9q9hFHMSg","M9xRE2k7dvFYV1gEjdj2KiUzqVapsijm8W"),
           ('mavr' ,"17TaVLtJCgq3Tb29g7jaBQEu3t3D88Kxk2","")]
# метаданные по монетам
# ticker , fullname , id, multiplyer
coins = [("BTC", 'bitcoin'), ("LTC", 'litecoin')]
    #get_address_balance
    #, ("DSH", 'dash',"131")]

def get_price(coin, currency = 'usd'):
    r = requests.get(APIurl+'get_price/{}/{}'.format(coin,currency)).json()
    if r["status"] == "success":
        return float(r['data']['prices'][0]['price'])
    else:
        return 10000. # хотя бы так
        # если будет часто буду ходить на другой API

def get_addr_info(owner, i_coin):
    # узнаем сколько зашло всего
    coin = coins[i_coin]
    addr = address[owner][1+i_coin] #номера кошельков записаны в порядке монет
    r1 = requests.get(APIurl+'get_address_received/{}/{}'.format(coin,addr)).json()
    # [/{AFTER TXID}] - можно найти транзакции после какой-то
    r2 = requests.get(APIurl+'get_tx_received/{}/{}'.format(coin,addr)).json()
    res = {
        "owner"         : address[owner][0],
        "coin"          : coin,
        "addr"          : addr,
        "confirmed"     : 0.0,
        "unconfirmed"   : 0.0,
        "txs"           : []}
    if r1["status"] == "success":
        res["confirmed"]=float(r1["data"]["confirmed_received_value"])
        res["unconfirmed"]=float(r1["data"]["unconfirmed_received_value"])
    if r2["status"] == "success":
        res["txs"] = r2["data"]["txs"] # len()
    return res

def get_pool_info():
    res = []
    for ticker, name in coins:
        try:
            r = requests.get('http://api.f2pool.com/{}/madskills'.format(name)).json()
            c_res = {
                "coin"          : ticker,
                "hashrate"      : r['hashrate'],
                "workers"       : r['worker_length'],
                "online"        : r['worker_length_online'],
                "rate24"        : r['hashrate_history'],
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
    for i_coin, (ticker, name)  in enumerate(coins):
        rate = get_price(ticker)
        res += '{} курс: {}usd\n'.format(ticker, round(rate))
        #  затем цикл по кошелькам
        for owner, w in enumerate(address):
            if len(w[1+i_coin])>0: # адрес не пуст
                info = get_addr_info(owner, i_coin)
                res += '[{}] received={}, tx={}\n'.format (w[0], info['confirmed'], len(info['txs']))
                res += 'total: = %s USD\n' % str(round(info['confirmed'] * rate))
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
                round(miners['value24']*get_price(miners['coin'])))
    return res

def get_state_info():
    #r = requests.get('http://api.f2pool.com/bitcoin/madskills').json()
    #return r['hashrate']
    #return get_addr_info(0)['balance'] + ' ' + get_addr_info(1)['balance']  + ' ' + get_price("1")
    #print(get_pool_info())
    return get_price("BTC")
