# tao

### API 请求地址 :
http://35.185.172.169:3000/stats?key=bitmex:BTC/USD

### 支持的keys : 
- bitmex:BTC/USD
- bitmex:ETHZ18
- bitmex:LTCZ18
- bitmex:EOSZ18
- bitmex:XRPZ18
- bitmex:BCHZ18

### API返回结果

```
{
    "status": 1, #状态为1表示请求成功
    "cur": { #当前捕获的数据
        "macd_4h": "up",
        "symbol": "BTC/USD",
        "macd_30m": "down",
        "macd_1h": "down",
        "30m": "mix",
        "4h": "mix",
        "1h": "down",
        "macd_1d": "down",
        "1d": "down"
    },
    "pre": { # 上一次捕获的数据
        "macd_4h": "up",
        "symbol": "BTC/USD",
        "macd_30m": "down",
        "macd_1h": "down",
        "30m": "mix",
        "4h": "mix",
        "1h": "down",
        "macd_1d": "down",
        "1d": "down"
    },
    "err":"" #当状态非1时则返回错误消息
}
```

### 提示
- 对比当前与上一次捕获的数据即可判断行情是否发生改变
