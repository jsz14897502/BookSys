# booksys datebase 说明文档

由于 markdown 语法中没有下划线，所以所有 **下划线** 均用 **加粗** 代替。

[TOC]

## 关系模式及说明

library_user ( id, stu_id , user_name, password, email, phone, holds, cretime, last_time )

primary key : id. 

这个表用来存用户信息，里面预存了下面这条信息。这条信息用来表示图书馆，不做改动 ( 图书馆也是书的所有者 ) 。

```mysql 
('library', 'library', 'library', 'library', 'library', 0, '2018-07-17 15:12:52', '2018-07-17 15:12:52', 0) 
```

表设计如下

| 名           | 类型     | 长度 | 小数点 | 不是null | 含义                                          |
| ------------ | -------- | ---- | ------ | -------- | --------------------------------------------- |
| id           | int      | 11   | 0      | 0        | 这条记录的 ID，给后台查数据以及做外码约束用的 |
| stu_id       | varchar  | 12   | 0      | 0        | 学号                                          |
| user_name    | varchar  | 10   | 0      | 0        | 用户名，私信用的                              |
| password     | varchar  | 16   | 0      | 0        | 密码                                          |
| email        | varchar  | 30   | 0      | 0        | 邮箱                                          |
| phone        | varchar  | 14   | 0      | 0        | 电话                                          |
| holds        | int      | 11   | 0      | -1       | 目前有几本书                                  |
| cretime      | datetime | 6    | 0      | 0        | 账户创建时间                                  |
| last_time    | datetime | 6    | 0      | -1       | 用户最后登录时间                              |
| cancellation | tinyint  | 1    | 0      | 0        | 账户是否注销                                  |



library_book_list ( **id**, isbn, book_name, author, translator, press, price, owner, borrowed_times, state_code )

primary key : id. 

foreign key : owner_id, reference library_user.id. 

book_image 属性存了这本书的图片地址。表设计如下

| 名             | 类型    | 长度 | 小数点 | 不是null | 含义                                          |
| -------------- | ------- | ---- | ------ | -------- | --------------------------------------------- |
| id             | int     | 11   | 0      | 0        | 这条记录的 ID，给后台查数据以及做外码约束用的 |
| isbn           | varchar | 15   | 0      | 0        | 图书的ISBN号                                  |
| book_name      | varchar | 20   | 0      | 0        | 书名                                          |
| author         | varchar | 100  | 0      | 0        | 作者                                          |
| translator     | varchar | 40   | 0      | -1       | 译者                                          |
| press          | varchar | 20   | 0      | 0        | 出版社                                        |
| price          | int     | 11   | 0      | 0        | 价格                                          |
| borrowed_times | int     | 11   | 0      | 0        | 被借次数                                      |
| state_code     | int     | 11   | 0      | 0        | 状态码                                        |
| owner_id       | int     | 11   | 0      | 0        | 拥有者的 ID                                   |
| book_image     | varchar | 100  | 0      | -1       | 书的封面                                      |
| profiles       | varchar | 300  | 0      | -1       | 书的简介                                      |



library_login_record ( id, login_time, user_id )

primary key : id. 

foreign key : user, reference library_user.stu_id

表设计如下

| 名         | 类型     | 长度 | 小数点 | 不是null | 含义                                          |
| ---------- | -------- | ---- | ------ | -------- | --------------------------------------------- |
| id         | int      | 11   | 0      | 0        | 这条记录的 ID，给后台查数据以及做外码约束用的 |
| login_time | datetime | 6    | 0      | 0        | 登录时间                                      |
| user_id    | int      | 11   | 0      | 0        | 登录用户的 ID                                 |



library_request ( **id**, BookName, CreTime, Requester, Owner, ConfirmCode, ExpiryTime )

primary key : id. 

foreign key : book_name, reference library_book_list.book_name. requester, reference library_user.stu_id. owner, reference library_user.stu_id. 

表设计如下

| 名           | 类型     | 长度 | 小数点 | 不是null | 含义                                          |
| ------------ | -------- | ---- | ------ | -------- | --------------------------------------------- |
| id           | int      | 11   | 0      | 0        | 这条记录的 ID，给后台查数据以及做外码约束用的 |
| cretime      | datetime | 6    | 0      | 0        | 请求创建时间                                  |
| confirm_code | smallint | 6    | 0      | 0        | 请求状态码                                    |
| expiry_time  | datetime | 6    | 0      | 0        | 请求过期时间                                  |
| book_name_id | int      | 11   | 0      | 0        | 被请求的书                                    |
| requster_id  | int      | 11   | 0      | 0        | 请求者                                        |



library_borrow ( **id**, BookName, Owner, EndTime, Previous, StateCode )

primary key : id.

foreign key :  book_name, reference library_book_list.book_name. owner, reference library_user.stu_id. state_code, reference library_book_list.state_code. 

表的设计如下

| 名           | 类型     | 长度 | 小数点 | 不是null | 含义                                          |
| ------------ | -------- | ---- | ------ | -------- | --------------------------------------------- |
| id           | int      | 11   | 0      | 0        | 这条记录的 ID，给后台查数据以及做外码约束用的 |
| end_time     | datetime | 6    | 0      | 0        | 借阅结束时间                                  |
| book_name_id | int      | 11   | 0      | 0        | 被借的书的名字                                |
| previous_id  | int      | 11   | 0      | 0        | 上一个借阅者                                  |



## 状态码取值说明

### ConfirmCode 取值说明

- 取值为 0 : 待确认
- 取值为 1 : 确认外借
- 取值为 2 : 拒绝外借
- 取值为 3 : 请求超时



### StateCode 取值说明

- 取值为 0 : 正常借阅中
- 取值为 1 : 借阅超时
- 取值为 2 : 书籍损坏
- 取值为 3 : 书籍丢失



## 触发器说明

### `login_record` 表上的触发器

在用户的此次登录被计入 `login_record` 表时，自动更新 `user` 表中的 `LastTime` 属性；

```mysql
create trigger last_time_update 
after insert 
on login_record
for each row
begin

update user 
set LastTime = NOW()
where StuID = NEW.UserID;

end
```



## 其他信息

1. `request` 表中当多个用户请求借阅同一本书的时候，书籍所有者同意某个请求，同时应该拒绝其他请求。
2. 书籍所有者同意借阅请求之后，`request` 表中被同意的请求应相应加入 `borrow` 表中，表示请求者借到了这本书。

