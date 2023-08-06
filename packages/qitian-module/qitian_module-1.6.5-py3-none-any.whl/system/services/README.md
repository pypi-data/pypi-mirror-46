# Notify Service 方法定义
各方法的处理逻辑如下：
createAnnounce(content, sender)

往Notify表中插入一条公告记录
createRemind(target, targetType, action, sender, content)

往Notify表中插入一条提醒记录
createMessage(content, sender, receiver)

往Notify表中插入一条信息记录
往UserNotify表中插入一条记录，并关联新建的Notify
pullAnnounce(user)

从UserNotify中获取最近的一条公告信息的创建时间: lastTime
用lastTime作为过滤条件，查询Notify的公告信息
新建UserNotify并关联查询出来的公告信息
pullRemind(user)

查询用户的订阅表，得到用户的一系列订阅记录
通过每一条的订阅记录的target、targetType、action、createdAt去查询Notify表，获取订阅的Notify记录。（注意订阅时间必须早于提醒创建时间）
查询用户的配置文件SubscriptionConfig，如果没有则使用默认的配置DefaultSubscriptionConfig
使用订阅配置，过滤查询出来的Notify
使用过滤好的Notify作为关联新建UserNotify
subscribe(user, target, targetType, reason)

通过reason，查询NotifyConfig，获取对应的动作组:actions
遍历动作组，每一个动作新建一则Subscription记录
cancelSubscription(user, target ,targetType)

删除user、target、targetType对应的一则或多则记录
getSubscriptionConfig(userID)

查询SubscriptionConfig表，获取用户的订阅配置
updateSubscriptionConfig(userID)

更新用户的SubscriptionConfig记录
getUserNotify(userID)

获取用户的消息列表
read(user, notifyIDs)

更新指定的notify，把isRead属性设置为true

作者：JC_Huang
链接：https://www.jianshu.com/p/6bf8166b291c
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。