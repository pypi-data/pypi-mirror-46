安装包：
pip install kafka-utils-netease

使用：
MsgSender和MsgRecver各有四个版本，分别为multi-thread版本，gevent-multi-thread版本，gevent-single-thread版本和light-weight版本。

multi-thread版本需要monkey.patch_all()才可以兼容gevent。其余无需patch_all()

light-weight版本适用于大量需要同步发送和接收消息的场合，其余版本适用于异步发送和接收数据的场合。
