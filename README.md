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

### 更多信息
- 此提醒适合右侧交易法则。
- 对比当前与上一次捕获的数据即可判断行情是否发生改变
- 当MA出现四个up或者四个down 有较大概率为重要信号，应当立刻关注实时行情加以分析判断。
- MACD 的交叉在不背离的情况下通常表示行情的开始与结束。
- 在不肯定以及没有数据支撑的情况下，不要进行左侧交易操作。
