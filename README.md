# PasteBin
## 介绍
众所周知，在 QQ、微信里发大段文字或代码是十分折磨的。比如说大段文字会让其他人阅读观感十分差，比如说在微信里你不能正常地发送一段 XML。那么我们可以考虑做一个网页，用户可以先将内容传上去，然后生成一个网址，然后把网址发到群里给其他人访问。
## 需求
- [x] 上传一段文字，生成这段文字对应的网址，其他人访问这个网址就能看到这段文字
- [x] 密码保护：没有密码无法正常解密
- [ ] 点对点加密：网址中可以添加浏览器不会向网络中发送的 fragment 部分，使得尽管生成的网址是 http，中间人也无法直接知道解密密钥
- [x] 阅后即焚：请求过一次这个网址就失效
- [x] 有效期限制：比如说一天之后就没了
## 实现

### 本地环境

>Python 3.9.7  
>Django 3.2.5  
>SQLite 3.37.0

### 使用
提前装好django，进到目录里
> $ python manage.py makemigrations app  
> $ python manage.py migrate app  
> $ python manage.py runserver  

然后访问 http://127.0.0.1:8000/app 就可以使用了
### 数据库

|    字段    |    类型    | 描述                                       |
|:--------:|:--------:|:-----------------------------------------|
|   text   | varchar  | 储存文本内容                                   |
|  index   |  bigint  | 用来查找数据、提供给用户的索引                          |
|  delete  | integer  | 阅后即焚相关判断<br/>（0：未设置阅后即焚；1：设置阅后即焚；-1：已销毁） |
|   date   | integer  | 一定时间后过期相关判断<br/>（10位时间戳表示过期日期）           |
| password | integer  | 16位MD5处理后的密码（在前端用js处理）                   |

### app里为PasteBin的相关代码
**app/**  
由index处理  
返回index.html  
**app/text**  
由add_text处理，仅接受POST  
1. 生成随机数作为索引，在数据库中查询是否有重复的
2. 往数据库中写入相关数据
3. 返回拼接的网址（index.html）  

**app/text/text**  
 由search_from_index处理，仅接受GET  
1. 根据索引查询是否有记录
2. 判断password是否为空文本的MD5值
3. 判断POST请求里password与数据库中存的password是否对应
4. 判断阅后即焚相关功能
5. 判断一定时间后失效相关功能
6. 返回文本内容（text.html） 

