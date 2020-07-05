# DnsPod API 多节点DDNS 脚本

本脚本基于DnsPod的API实现DDNS，在`Python 3.7.6`测试通过

## 使用方法：
### 安装依赖：
 `pip3 install -r requirements.txt`
### 编辑配置
编辑`config.py`文件，根据注释配置参数

请注意 domain_id、record_id、sub_domain 参数的配置

参数官方解释文档 [https://www.dnspod.cn/docs/records.html#record-modify](https://www.dnspod.cn/docs/records.html#record-modify)
#### 获取 `login_token`
[获取密钥](https://www.dnspod.cn/console/user/security)
`DNSPOD > 用户中心 > 安全设置 > API Token`

使用英文 , 将 `ID` 和 `Token` 连接起来即公共请求参数 `login_token`
#### 获取 domain_id
`curl 'https://dnsapi.cn/Domain.List' -d 'login_token=<your_login_token>&format=json'`

根据响应中的 `domains` 得到域名对应的 `domain_id`
#### 获取 record_id
`curl 'https://dnsapi.cn/Record.List' -d 'login_token=<your_login_token>&format=json&domain_id=<your_domain_id>'`

根据响应中的 `records` 得到子域名记录对应的 `record_id`
#### sub_domain
sub_domain 主机记录, 如 www，可选，如果不传，默认为 @
#### node_info
多个节点请根据格式添加，支持IP/CNAME

### 启动方法
`python3 ddns.py`