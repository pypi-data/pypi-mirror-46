# findit-client

[![image](https://img.shields.io/pypi/pyversions/requests.svg)](https://pypi.org/project/requests/)
[![Build Status](https://travis-ci.org/williamfzc/findit-client.svg?branch=master)](https://travis-ci.org/williamfzc/findit-client)

Client for [findit](https://github.com/williamfzc/findit), with no opencv needed.

## 目的

- 旨在提供超低依赖的findit client，用于适应不同机器（尤其是无法安装opencv）的环境。
- 该client只依赖于http请求，只使用了requests，依赖环境与requests一致。

## 使用

### 服务器部署

参考文档：[这里](https://williamfzc.github.io/findit/#/usage/client+server?id=服务端部署)

### 连接到服务器

本地服务器：

```python
from findit_client import FindItClient

cli = FindItClient(port=9410)
```

远程服务器：

```python
from findit_client import FindItClient

cli = FindItClient(host='123.45.67.8', port=9410)
```

### 获取完全的分析结果

我们希望在本地图片 `screen.png` 中寻找 `wechat_logo.png`（这里假设该图片已存在于服务器）

```python
from findit_client import FindItClient

cli = FindItStandardClient()

result = cli.analyse_with_path('screen.png', 'wechat_logo.png')
print(result)
```

将会返回完整的结果，供开发者自由定制。

### 获取目标点位置

```python
result = cli.get_target_point_with_path(
    'screen.png',
    'wechat_logo.png',
    threshold=0.8,
)
```

当相似度超过0.8时，会返回模板图片的坐标；否则抛出异常。

如果不传入threshold，则会返回最可能的坐标。

### 检查目标是否存在

```python
result = cli.check_exist_with_path(
    'screen.png',
    'wechat_logo.png',
    threshold=0.8,
)
```

当相似度超过0.8时，返回True，否则False。

### 分析 opencv object

为了最小化client的依赖，默认的client并没有支持opencv。如果你希望直接识别opencv对象，你可以使用 `FindItStandardClient` 替代 `FindItClient`。

```python
from findit_client import FindItStandardClient
import cv2

cli = FindItStandardClient()

target_object = cv2.imread('tests/pics/screen.png')
result = cli.analyse_with_object(target_object, 'wechat_logo.png')
print(result)
```

用法基本与path类一致。

## 协议

[MIT](LICENSE)
