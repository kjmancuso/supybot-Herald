```
In [1]: import requests
In [2]: payload = {'chan': '#channel', 'msg': 'Hello world'}
In [3]: r = requests.post('http://path.to/irc_announce', data=payload)
In [4]: r.text
Out[4]: u'OK'
```
