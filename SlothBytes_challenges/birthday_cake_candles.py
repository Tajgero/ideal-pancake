def birthdayCakeCandles(candles: list) -> int:
    """Returns number of tallest candles on a cake"""
    
    if len(candles) == 0:
        print("output = 0")
        return 0
    
    tallest = max(candles)
    n = 0
    for candle in candles:
        if candle == tallest:
            n += 1
    
    print(f"output = {n}")
    return n


birthdayCakeCandles([4,4,1,3])
birthdayCakeCandles([1, 1, 1, 1])
birthdayCakeCandles([])
