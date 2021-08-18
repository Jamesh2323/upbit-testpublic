import time
import pyupbit
import datetime

access = "your-access"
secret = "your-secret"

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma3(ticker):
    """3일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=3)
    ma03 = df['close'].rolling(3).mean().iloc[-1]
    return ma3

def get_ma5(ticker):
    """5일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=5)
    ma5 = df['close'].rolling(5).mean().iloc[-1]
    return ma5

def get_ma10(ticker):
    """10일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=10)
    ma15 = df['close'].rolling(10).mean().iloc[-1]
    return ma15

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-XRP") #09:00
        end_time = start_time + datetime.timedelta(days=1) #09:00 +1일

        # 09:00 < 현재 < #08:59:50 
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-XRP", 0.5)
            ma3 = get_ma3("KRW-XRP")
            ma5 = get_ma5("KRW-XRP")
            ma10 = get_ma10("KRW-XRP")
            ma15 = get_ma15("KRW-XRP")
            current_price = get_current_price("KRW-XRP")
            if target_price < current_price and ma3 < current_price and ma5 < current_price and ma10 < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 1000:
                    upbit.buy_market_order("KRW-XRP", krw*0.9995)
        else:
            xrp = get_balance("XRP")
            if xrp > 2.90000:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)