# rankSever
使用django建立一个玩家分数排行榜服务

## 服务上传分数接口
  http://127.0.0.1:8000/upload
  该接口需包含两个参数：
  client_name: 客户端名称
  score: 0～10000000之间的一个数字
  example: http://127.0.0.1:8000/upload/?client_name=111&score=1234

## 查询排名接口
http://127.0.0.1:8000/search
该接口需包含三个参数：
client_name: 客户端名称
start: 要查询排名范围的起始位置
end: 要查询排名范围的结束位置
example: http://127.0.0.1:8000/search/?client_name=7777&start=3&end=10

