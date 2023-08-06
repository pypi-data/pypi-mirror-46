# htjs-apisdk-python

## 安装

    pip install -U htjs-apisdk
    
## 使用

```python
import requests
from htjs_apisdk import HtjsApiSdkClient

ak_id = '{此处填入你的access_key_id}'
ak_secret = '{此处填入你的access_key_secret}'

test_url = 'https://api.htjs.net/test/helloworld?x=123&y=456#z=789'


htjs_api = HtjsApiSdkClient(ak_id, ak_secret)

headers = htjs_api.get_signed_headers('GET', test_url)
res = requests.get(test_url, headers=headers)
print(res.content)

headers = htjs_api.get_signed_headers('POST', test_url)
res = requests.post(test_url, headers=headers)
print(res.content)

headers = htjs_api.get_signed_headers('PUT', test_url)
res = requests.put(test_url, headers=headers)
print(res.content)

headers = htjs_api.get_signed_headers('DELETE', test_url)
res = requests.delete(test_url, headers=headers)
print(res.content)

headers = htjs_api.get_signed_headers('PATCH', test_url)
res = requests.patch(test_url, headers=headers)
print(res.content)
```
