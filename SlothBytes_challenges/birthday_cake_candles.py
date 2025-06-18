class Candles():
    
    def __init__(self, input):
        self.count, self.tallest = self.birthdayCakeCandles(input)
        print(self)
        
    def __repr__(self):
        return f"Count: {self.count}\nTallest: {self.tallest}"
    
    def birthdayCakeCandles(self, candles: list) -> tuple:
        """
        Returns count and tallest of candles on a cake
        in more complicated recursive way than just
        5 lines of code
        """
        this_candle = 0
        
        # Base Case
        try:
            this_candle = candles[0]
        except:
            # When recursion ends returns count and candle height
            return 0, this_candle
        
        # Recursion
        n, next_candle = self.birthdayCakeCandles(candles[1:])
        
        # Checking candle heights
        if next_candle < this_candle:
            n = 1
            
        elif next_candle > this_candle:
            this_candle = next_candle
            
        else:
            return 1 + n, this_candle
           
            
        return n, this_candle
        
    
if __name__ == '__main__':
    
    Candles([4,4,1,3])
    Candles([4,4,1,3])
    Candles([1, 1, 1, 1])
    Candles([])
