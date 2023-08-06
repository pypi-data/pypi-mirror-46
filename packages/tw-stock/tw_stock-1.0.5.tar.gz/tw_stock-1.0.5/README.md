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
  "stock_no": 2330,
  "now_price": "230.00",
  "low_price": "229.00",
  "high_price": "231.50"
}
```
