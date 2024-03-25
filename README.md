# WeChatRobot
基于[WeChatFerry](https://github.com/lich0821/WeChatFerry) 的微信机器人示例。

## Quick Start

0. 安装 Python，例如 [3.10.11](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)
1. 安装微信 `3.9.2.23`，下载地址在 https://pan.baidu.com/s/1pg3T0jJVZSToCN9em3uLJA?pwd=club
   提取码：club
2. 克隆项目
```sh
git clone https://github.com/Algieba-dean/ClubManagementRobot
```

3. 安装依赖
```sh
# 升级 pip
python -m pip install -U pip
# 安装必要依赖
pip install -r requirements.txt
```

4. 运行

直接运行程序会自动拉起微信：

```sh
python bot.py
# 如果微信未打开，会自动打开微信；如果版本不对，也会有提示；
```

### 修改配置

配置文件 `config.yaml` 是运行程序后自动从模板复制过来的，以下功能默认关闭。

* 为了响应群聊消息，需要添加相应的 `roomId`（打印的消息中方括号里的就是）：
* 以下xxxx@chatroom即为roomId, 管理员的wxid需要从消息打印中抓，不一定就是微信id

```yaml

club_activate_groups:
  {
    "Abbbbb@chatroom": [ # room_id
      "wxid_aaaa",             # group managers
      "wxid_bbbb",
      "wxid_cccc",
    ],
```

### 命令

设计上来讲，参考原作者的功能，给多插件实现留了槽位，原则上是可以实现多个插件共同使用。
由于目前的消息量不多，暂时未使用异步处理（异步处理更为合理）

#### 以下是可用的命令及格式

```shell
.发起活动
活动名称: [小小写作家202308A]
活动开始时间: [2023-08-13]
活动结束时间: [2023-08-16]
活动详情:
任意内容
```

* 该命令用于发起活动
* 该命令仅限**管理员**使用
* **活动名称需要唯一**
* 活动起始时间需要按照给定的格式
* 其余内容任意

```shell
.打卡
活动名称: [小小写作家202308A]
打卡任意内容
```

* 该命令用于参与活动，进行打卡
* 激活机器人的群里任意成员均可使用
* **活动名称**一定要指定正确
* 打卡内容任意

```shell
.更新活动
活动名称: [小小写作家202308A]
活动开始时间: [2023-08-13]
活动结束时间: [2023-08-16]
活动详情:
任意内容
```

* 该命令用于修改发起活动,避免有时候设置错误活动时间
* 该命令仅限**管理员**使用
* **活动名称需要设置正确**
* 活动起始时间需要按照给定的格式
* 其余内容任意

```shell
.活动状态
活动名称: [小小写作家202308A]
```

* 该命令用于查看活动参与情况
* 该命令仅限**管理员**使用
* **活动名称需要设置正确**
* 在群内使用该指令仅仅会显示参与人昵称，管理员私聊的话会显示所有信息，包括打卡内容
