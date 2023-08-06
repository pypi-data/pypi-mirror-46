Get Taiwan's stock info in real-time

## Install:

```
pip install tw-stock
```
## Example:

```
from tw_stock.stock import get_realtime
print(get_realtime(2330))
```
## Return:

```
{
    "low_price": "233.00", 
    "high_price": "235.00", 
    "now_date": "20190527", 
    "now_time": "09:31:01", 
    "now_amount": "9355", 
    "now_diff": "0.0", 
    "now_price": "233.00", 
    "now_percent": "0.0", 
    "stock_name": "台積電", 
    "stock_no": "2330"
}
```
