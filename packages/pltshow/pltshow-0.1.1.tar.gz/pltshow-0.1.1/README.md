# pltshow-python
python sdk for pltshow


## Example

```python
import pandas as pd
import pltshow
username = '....'
password = '.....'
plt = pltshow.Client(username, password)

df = pd.DataFrame(....)
plt.show(df)
```
then open www.pltshow.com in browser, login and then your chart will be there
