#!/usr/bin/env python
# -*-coding:utf-8-*-
"""
HTTP-API Python SDK(Python2、python3)
 * Created by PyCharm.
 * User: yugao
 * version 2.2.3
 * Note: HTTPSDK for Python(适用于版本2.2.2插件):用于解析插件消息、构造返回数据，以及HTTP推送（发起HTTP请求）
 * Contact: 开发者邮箱 admin@ksust.com
"""

import sys

version = sys.version_info.major
if version == 2:
    # reload(sys) # python2请配置相应编码
    # sys.setdefaultencoding('utf8')
    # sys.setdefaultencoding('gb18030')
    import urllib
    from httplib import HTTPConnection, BadStatusLine
elif version == 3:
    import urllib.parse
    import urllib.request
    from http.client import HTTPConnection, BadStatusLine

import hashlib
import json
import os
import time
import uuid
import requests


class MessageGet:
    def __init__(self):
        dic = {}
        self.__dic = dic
        self.Myqq = dic.get('Myqq')
        self.Type = dic.get('Type')
        self.SubType = dic.get('SubType')
        self.From = dic.get('From')
        self.Group = dic.get('Group')
        self.Discuss = dic.get('Discuss')
        self.QQ = dic.get('QQ')
        self.ObjectQQ = dic.get('ObjectQQ')
        self.Msg = dic.get('Msg')
        self.ID = dic.get('ID')
        self.Data = dic.get('Data')

    def parse(self, json_str):
        if type(json_str) == 'bytes' or isinstance(json_str, bytes):
            json_str = json_str.decode('utf-8')
        if version == 2:
            dic = json.loads(urllib.unquote(json_str))
        elif version == 3:
            dic = json.loads(urllib.parse.unquote(json_str))
        self.__dic = dic
        self.Myqq = dic.get('Myqq')
        self.Type = int(dic.get('Type'))
        self.SubType = int(dic.get('SubType'))
        self.From = dic.get('From')
        self.Group = dic.get('Group')
        self.Discuss = dic.get('Discuss')
        self.QQ = dic.get('QQ')
        self.ObjectQQ = dic.get('ObjectQQ')
        self.Msg = dic.get('Msg') if type(dic.get('Msg')) == 'dic' else str(dic.get('Msg'))
        self.ID = dic.get('ID')
        self.Data = dic.get('Data')

        return self

    def __str__(self):
        return json.dumps(self.__dic)


class HTTPSDK():
    __TEMP_DIR = os.path.join(os.getcwd(), 'temp\\msgForward\\')

    __returnDataCell = {
        "ID": '-1',
        "Type": -1,
        "SubType": 0,
        "StructureType": 0,
        "Group": "",
        "QQ": "",
        "Msg": "",
        "Send": 0,
        "Data": {}
    }

    # 消息类型
    TYPE_FRIEND_TEMP = 0  # 在线状态临时会话（Pro版可用）
    TYPE_FRIEND = 1  # 好友消息，发送私聊消息
    TYPE_GROUP = 2  # 群消息，发送群消息
    TYPE_DISCUSS = 3  # 讨论组消息，发送讨论组消息
    TYPE_GROUP_TEMP = 4  # 群临时会话
    TYPE_DISCUSS_TEMP = 5  # 讨论组临时会话
    TYPE_ACCOUNT = 6  # 收到财付通转账
    TYPE_FRIEND_VERIFY_BACK = 7  # 好友验证回复会话消息（Pro版可用）
    # 请求处理事件
    TYPE_HANDLE_AGREE = 10  # 请求处理_同意
    TYPE_HANDLE_REJECT = 20  # 请求处理_拒绝
    TYPE_HANDLE_IGNORE = 30  # 请求处理_忽略
    # 好友事件
    TYPE_FRIEND_ADDED_SINGLE = 100  # 被单项添加为好友
    TYPE_FRIEND_ADDED = 101  # 某人请求加为好友
    TYPE_FRIEND_ADDED_AGREED = 102  # 被同意加为好友
    TYPE_FRIEND_ADDED_REJECTED = 103  # 被拒绝加为好友
    TYPE_FRIEND_DELETED = 104  # 被删除好友
    TYPE_FRIEND_FILE_OFFLINE = 105  # 收到好友离线文件（Pro版可用）
    TYPE_FRIEND_SIGNATURE_CHANGE = 106  # 好友签名变更
    TYPE_FRIEND_SAY_COMMENT = 107  # 说说被某人评论
    # 群事件
    TYPE_GROUP_FILE_RECV = 218  # 收到群文件
    TYPE_GROUP_IN_WHO_REQUEST = 213  # 某人请求入群
    TYPE_GROUP_IN_ME_INVITED = 214  # 被邀请加入群
    TYPE_GROUP_IN_ME_AGREED = 220  # 被批准入群
    TYPE_GROUP_IN_ME_REJECTED = 221  # 被拒绝入群
    TYPE_GROUP_IN_WHO_INVITED = 215  # 某人被邀请加入群
    TYPE_GROUP_IN_WHO_INVITED_HAS = 219  # 某人已被邀请加入群（群主或管理员邀请成员加群或开启了群成员100以内无需审核或无需审核直接进群，被邀请人同意进群后才会触发）
    TYPE_GROUP_IN_WHO_AGREED = 212  # 某人被批准加入了群
    TYPE_GROUP_QUIT_WHO = 201  # 某人退出群
    TYPE_GROUP_QUITED_WHO = 202  # 某人被管理移除群
    TYPE_GROUP_INVALID = 216  # 某群被解散
    TYPE_GROUP_ADMIN_WHO_BECOME = 210  # 某人成为管理
    TYPE_GROUP_ADMIN_WHO_INVALID = 211  # 某人被取消管理
    TYPE_GROUP_BANED = 203  # 对象被禁言
    TYPE_GROUP_BANED_INVALID = 204  # 对象被解除禁言
    TYPE_GROUP_BANED_ALL = 205  # 开启全群禁言
    TYPE_GROUP_BANED_ALL_INVALID = 206  # 关闭全群禁言
    TYPE_GROUP_ANONYMOUS_OPEN = 207  # 开启匿名聊天
    TYPE_GROUP_ANONYMOUS_CLOSE = 208  # 关闭匿名聊天
    TYPE_GROUP_NOTICE_CHANGE = 209  # 群公告变动
    TYPE_GROUP_CARD_CHANGE = 217  # 群名片变动
    # 操作类型
    TYPE_SEND_LIKE = 20001  # 点赞
    TYPE_SEND_SHAKE = 20002  # 窗口抖动
    TYPE_GROUP_BAN = 20011  # 群禁言（管理）
    TYPE_GROUP_QUIT = 20012  # 主动退群
    TYPE_GROUP_KICK = 20013  # 踢群成员（管理）
    TYPE_GROUP_SET_CARD = 20021  # 设置群名片（管理）
    TYPE_GROUP_SET_ADMIN = 20022  # 设置群管理（群主）
    TYPE_GROUP_HANDLE_GROUP_IN = 20023  # 入群处理（某人请求入群、我被邀请入群、某人被邀请入群）
    TYPE_FRIEND_HANDLE_FRIEND_ADD = 20024  # 加好友处理（是否同意被加好友）
    TYPE_GROUP_ADD_NOTICE = 20031  # 发群公告
    TYPE_GROUP_ADD_HOMEWORK = 20032  # 发群作业
    TYPE_GROUP_JOIN = 20033  # 主动申请加入群

    TYPE_DIS_CREATE = 20041  # 创建讨论组，返回讨论组ID（并且对外部接口支持直接根据好友列表创建讨论组）
    TYPE_DIS_INVITE = 20042  # 邀请加入某讨论组，多个用  # 隔开
    TYPE_DIS_KICK = 20043  # 踢出讨论组成员
    TYPE_DIS_QUIT = 20044  # 退出讨论组
    TYPE_GROUP_INVITE = 20051  # 邀请QQ入群（管理 + 普通成员）

    TYPE_GET_LOGIN_QQ = 20101  # 获取当前QQ
    TYPE_GET_STRANGER_INFO = 20102  # 获取陌生人信息，JSON，昵称，性别，年龄，签名
    TYPE_GET_GROUP_LIST = 20103  # 获取当前QQ群列表，JSON
    TYPE_GET_GROUP_MEMBER_LIST = 20104  # 获取指定群成员列表，JSON
    TYPE_GET_FRIEND_LIST = 20105  # 获取好友列表，JSON
    TYPE_GET_GROUP_NOTICE = 20106  # 获取群公告列表，JSON
    TYPE_GET_DIS_LIST = 20107  # 获取讨论组列表
    TYPE_GET_QQ_LEVEL = 20111  # 获取QQ等级
    TYPE_GET_GROUP_MEMBER_CARD = 20112  # 获取群成员名片
    TYPE_GET_QQ_ONLINE_STATUS = 20113  # 查询QQ是否在线
    TYPE_GET_QQ_IS_FRIEND = 20114  # 查询QQ是否好友
    TYPE_GET_QQ_ROBOT_INFO = 20115  # 获取机器人状态信息，JSON
    TYPE_LIKE_COUNT_GET = 20201  # 获取目标对象赞数目
    TYPE_SET_INPUT_STATUS = 20301  # 置正在输入状态（发送消息取消）
    TYPE_TIMER_SEND = 30001  # 定时任务提交类型

    # 消息子类型
    SUBTYPE_CALLBACK_SEND = 10001  # 提交返回有反馈时，更改原数据中的subtype和msg（数据），向返回地址发送反馈

    def __init__(self):
        self.__returnData = {'data': []}
        self.__SDKType = 0  # SDK模式，0为http提交返回，1为webSocket提交返回模式，2为httpPush推送模式，3为消息转发模式（http协议）
        self.__serverURL = 'http://127.0.0.1:8888'
        self.__serverKey = '123'
        self.__serverSecret = '456'
        self.__callbackSend = False  # 在回调情况下是否开启发送消息，默认否
        # 用于消息转发
        self.__myqq = ''  # 消息转发，机器人QQ
        self.__code = ''  # 消息转发，机器人授权码
        self.__url = 'http://127.0.0.1:2047'  # 消息转发请求，代理服务器http地址
        self.__token = ''  # 消息转发，验证token（由授权码、QQ获取）
        self.__msg = MessageGet()
        pass

    '''
    提交返回模型，无需传入参数
    @:return HTTPSDK
    '''

    @staticmethod
    def httpGet(msg):
        sdk = HTTPSDK()
        sdk.__parseMsg(msg)
        return sdk

    '''
    提交返回（webSocket）模型，传入获取到的原始消息
    @:param msg 获取到的原始消息（RequestBody）
    @:return HTTPSDK
    '''

    @staticmethod
    def webSocket(msg):
        sdk = HTTPSDK()
        sdk.__parseMsg(msg)
        return sdk

    '''
    HTTP推送模型
    @:param URL 推送地址及端口，如http://127.0.0.1:8888
    @:param key 验证key 为空或null则表示不加密
    @:param secret 验证secret 为空或null则表示不加密
    @:return HTTPSDK
    '''

    @staticmethod
    def httpPush(URL, key=None, secret=None):
        sdk = HTTPSDK()
        sdk.__SDKType = 2
        sdk.__serverURL = URL
        sdk.__serverKey = key
        sdk.__serverSecret = secret
        return sdk

    '''
    消息转发推送模型
    @:param qq 机器人QQ
    @:param code 该机器人QQ的授权码，统一管理平台：http://work.ksust.com
    @:return HTTPSDK
    '''

    @staticmethod
    def msgForwardPush(qq, code):
        sdk = HTTPSDK()
        sdk.__SDKType = 3
        sdk.__myqq = qq
        sdk.__code = code
        sdk.__url, sdk.__token = sdk.__getMsgForwardPushToken(qq, code)
        return sdk

    def __parseMsg(self, msg):
        self.__msg = MessageGet().parse(msg)

    '''
    *添加功能，原始方法：为了保持一致，此处参数使用大驼峰命名
    @ param Type
    @ param int SubType
    @ param int StructureType
    @ param string Group
    @ param string QQ
    @ param string Msg
    @ param string Data
    @ param int Send
    @ return mixed
    '''

    def __addDataCell(self,
                      Type,
                      SubType=0,
                      StructureType=0,
                      Group='',
                      QQ='',
                      Msg='',
                      Data=None,
                      Send=0):
        data = self.__returnDataCell
        data['ID'] = str(uuid.uuid1())
        data['Type'] = Type
        data['SubType'] = SubType
        data['StructureType'] = StructureType
        data['Group'] = Group
        data['QQ'] = QQ
        data['Msg'] = Msg
        data['Data'] = Data
        data['Send'] = Send
        # 避免浅拷贝问题
        data = json.dumps(data)
        self.__returnData['data'].append(json.loads(data))
        if self.__SDKType == 2:
            res = self.__sendPushData()
            try:
                res = json.loads(res)
                if isinstance(res, dict):
                    return res['Result']
                return res
            except:
                return res
        elif self.__SDKType == 3:
            sendData = self.__returnData['data'][0]
            self.__returnData = {'data': []}
            returnJson = json.loads(
                self.__sendMsgForwardPush(self.__url, 3, 'user-' + self.__myqq, 'plugin-' + self.__myqq, self.__token,
                                          sendData))
            if (returnJson.get('status') == -1):
                # 清空缓存
                f = open(os.path.join(self.__TEMP_DIR, "msgForward-" + self.__myqq), 'w')
                f.write('{}')
                f.flush()
                f.close()
            res = returnJson['data']
            try:
                res = json.loads(returnJson['data'])
                if isinstance(res, dict):
                    return res['Result']
            except:
                pass
            return res
        # 回调模式返回消息
        if self.isCallback():
            if not self.__callbackSend:
                self.__returnData = {'data': []}
            return self.getMsg().Msg
        return '1'

    def __sendPushData(self):
        url = self.__serverURL
        self.__returnData['time'] = int(time.time())
        verify_str = str(self.__serverKey) + str(self.__returnData['time']) + str(self.__serverSecret)
        self.__returnData['verify'] = hashlib.md5(verify_str.encode('UTF-8')).hexdigest()
        json_data = json.dumps(self.__returnData)
        self.__returnData = {'data': []}
        headers = {"Content-Type": "application/json"}
        result = '{}'
        try:
            host = "127.0.0.1"
            port = 8080
            url = self.__serverURL
            if not url.replace("://", "").__contains__(":"):
                port = 80
                host = url.replace("://", ":").split(":")[1]
            else:
                port = int(url.replace("://", "").split(":")[1])
                host = url.replace("://", ":").split(":")[1]

            client = HTTPConnection(host, port)
            client.request('POST', '', body=json_data, headers=headers)
            result = client.getresponse().read().decode('utf-8')
        except BadStatusLine as e:
            # 某些插件版本中 push 没有包含标注你的HTTP头，这里进行编码转换！！！
            # RFC 2616 Section 3.7.1 says that text default has a default charset of iso-8859-1.
            result = e.line.encode('iso-8859-1').decode('utf-8')

        finally:
            return result

    def __getMsgForwardPushToken(self, qq, code):
        token = ''
        url = 'http://127.0.0.1:2047'
        filePath = os.path.join(self.__TEMP_DIR, "msgForward-" + qq)
        tokenKey = 'msgForwardToken-' + qq
        urlKey = 'msgForwardURL-' + qq
        if not os.path.exists(self.__TEMP_DIR):
            # 使用makedirs，由于可能创建多级目录
            os.makedirs(self.__TEMP_DIR)
        if not os.path.exists(filePath):
            f = open(filePath, 'w')
            f.write('{}')
            f.flush()
            f.close()
        # 检查 缓存
        f = open(filePath, 'r')
        values = json.loads(f.read())
        if values.get('time') is None or int(time.time()) - values.get('time') > 60 * 60 * 24:
            # 获取，缓存
            verifyData = self.__sendMsgForwardPush('http://qq.ksust.com/api/tool.php?func=get_server_dst'
                                                   , 3, 'user-' + qq, 'plugin-' + qq, code)
            verifyData = json.loads(verifyData)
            if verifyData.get('status') == 1:
                token = verifyData.get('data').get('token')
                url = 'http://' + verifyData.get('data').get('ip') + ':' + str(verifyData.get('data').get(
                    'http-port')) + '/api/user/request'
                # 写入文件缓存
                verify = {}
                verify['token'] = token
                verify['url'] = url
                verify['time'] = int(time.time())
                f.close()
                f = open(filePath, 'w')
                f.write(json.dumps(verify))
                f.flush()
                f.close()
        else:
            token = values.get('token')
            url = values.get('url')

        return url, token

    '''
    消息转发请求协议封装
    @:return 请求结果，json str
    '''

    def __sendMsgForwardPush(self, url, code, src, dst, token, dataIn={}):
        data = {}
        data['id'] = int(time.time())
        data['code'] = code
        data['src'] = src
        data['dst'] = dst
        data['time'] = int(time.time())
        data['token'] = token
        data['data'] = json.dumps(dataIn)

        return requests.post(url, json=data).content.decode('utf-8')

    '''
    获取接收到的消息（结构化）
    @:return JSON/MessageGet对象
    '''

    def getMsg(self):
        return self.__msg

    '''
    # 当前消息体是否为插件反馈（用于提交返回模型下获取群列表等）
    # 若是，则默认不能够返回消息。若需要返回消息，调用setCallbackSend(true)
    @ return boolean
    '''

    def isCallback(self):
        return self.getMsg().SubType == self.SUBTYPE_CALLBACK_SEND

    '''
    # 是否在插件反馈情况下返回消息（提交返回），默认否。
    @:param boolean callbackSend默认false
    '''

    def setCallbackSend(self, callbackSend=False):
        self.__callbackSend = callbackSend

    '''
    # 获取返回数据：已格式化，作为最后直接的输出返回.同时重置已发送消息（清空）
    @:return string 消息文本(json_encode)
    '''

    def toJsonString(self):
        ret = json.dumps(self.__returnData)
        self.__returnData = {'data': []}
        return ret

    #  接下来为具体功能，每添加一个功能就增加一条消息

    #  消息发送  #
    '''
    # 用发送消息方法（为解决某些平台兼容问题）
    @:param int type 消息类型，见TypeEnum（如1为好友消息，2为群消息，3为讨论组消息，4为群临时消息等）
    @:param string group
    @:param string qq
    @:param string msg
    @:param int structureType 消息结构类型 0普通消息，1 XML消息，2 JSON消息
    @:param int subType XML、JSON消息发送方式下：0为普通（默认），1为匿名（需要群开启）
    @:return mixed
    '''

    def sendMsg(self, type, group, qq, msg, structureType=0, subType=0):
        return self.__addDataCell(type, subType, structureType, group, qq, msg, {}, 0)

    '''
    # 发送私聊消息
    @:param string qq
    @:param string msg
    @:param int structureType 消息结构类型 0普通消息，1 XML消息，2 JSON消息
    @:param int subType XML、JSON消息发送方式下：0为普通（默认），1为匿名（需要群开启）
    @:return mixed
    '''

    def sendPrivdteMsg(self, qq, msg, structureType=0, subType=0):
        return self.__addDataCell(self.TYPE_FRIEND, subType, structureType, '', qq, msg, {}, 0)

    '''
    # 发送群消息
    @:param string groupId
    @:param string msg
    @:param int structureType 消息结构类型 0普通消息，1 XML消息，2 JSON消息
    @:param int subType XML、JSON消息发送方式下：0为普通（默认），1为匿名（需要群开启）
    @:return mixed
    '''

    def sendGroupMsg(self, groupId, msg, structureType=0, subType=0):
        return self.__addDataCell(self.TYPE_GROUP, subType, structureType, groupId, '', msg, {}, 0)

    '''
    # 发送讨论组消息
    @:param string discuss
    @:param string msg
    @:param int structureType 消息结构类型 0普通消息，1 XML消息，2 JSON消息
    @:param int subType XML、JSON消息发送方式下：0为普通（默认），1为匿名（需要群开启）
    @:return mixed
    '''

    def sendDiscussMsg(self, discuss, msg, structureType=0, subType=0):
        return self.__addDataCell(self.TYPE_DISCUSS, subType, structureType, discuss, '', msg, {}, 0)

    '''
    # 向QQ点赞
    @:param string qq
    @:param int count 默认为1，作为消息的 Msg项
    @:return mixed
    '''

    def sendLike(self, qq, count=1):
        return self.__addDataCell(self.TYPE_SEND_LIKE, 0, 0, '', qq, count, {}, 0)

    '''
    # 窗口抖动
    @:param string qq
    @:return mixed
    '''

    def sendShake(self, qq):
        return self.__addDataCell(self.TYPE_SEND_SHAKE, 0, 0, '', qq, '', {}, 0)

    #  群操作、事件处理  #

    '''
    # 群禁言（管理）
    @:param string groupId 群号
    @:param string qq 禁言QQ，为空则禁言全群
    @:param int time 禁言时间，单位秒，至少10秒。0为解除禁言
    @:return mixed
    '''

    def setGroupBan(self, groupId, qq='', time=10):
        return self.__addDataCell(self.TYPE_GROUP_BAN, 0, 0, groupId, qq, time, {}, 0)

    '''
    # 主动退群
    @:param string groupId
    @:return mixed
    '''

    def setGroupQuit(self, groupId):
        return self.__addDataCell(self.TYPE_GROUP_QUIT, 0, 0, groupId, '', '', {}, 0)

    '''
    # 踢人（管理）
    @:param string groupId
    @:param string qq
    @:param boolean neverIn 是否不允许再加群
    @:return mixed
    '''

    def setGroupKick(self, groupId, qq, neverIn=False):
        return self.__addDataCell(self.TYPE_GROUP_KICK, 0, 0, groupId, qq, 1 if (neverIn == True) else 0, {}, 0)

    '''
    # 设置群名片
    @:param string groupId
    @:param string qq
    @:param string card
    @:return mixed
    '''

    def setGroupCard(self, groupId, qq, card=''):
        return self.__addDataCell(self.TYPE_GROUP_SET_CARD, 0, 0, groupId, qq, card, {}, 0)

    '''
    # 设置管理员(群主)
    @:param string groupId
    @:param string qq
    @:param boolean become true true为设置，false为取消
    @:return mixed
    '''

    def setGroupAdmin(self, groupId, qq, become=False):
        return self.__addDataCell(self.TYPE_GROUP_SET_ADMIN, 0, 0, groupId, qq, 1 if (become == True) else 0, {}, 0)

    '''
    # 处理加群事件，是否同意
    @:param string groupId
    @:param string qq
    @:param boolean agree 是否同意加群
    @:param int type 213请求入群  214我被邀请加入某群  215某人被邀请加入群 。为0则不管哪种
    @:param string msg 消息，当拒绝时发送的消息
    @:return mixed
    '''

    def handleGroupIn(self, groupId, qq, agree=True, type=0, msg=''):
        return self.__addDataCell(self.TYPE_GROUP_HANDLE_GROUP_IN, type, 0, groupId, qq, 1 if (agree == True) else 0,
                                  msg, 0)

    '''
    # 是否同意被加好友
    @:param string qq
    @:param boolean agree 是否同意
    @:param string msg 附加消息
    @:return mixed
    '''

    def handleGroupIn(self, qq, agree=True, msg=''):
        return self.__addDataCell(self.TYPE_FRIEND_HANDLE_FRIEND_ADD, 0, 0, '', qq, 1 if (agree == True) else 0, msg,
                                  0)

    '''
    # 发群公告（管理）
    @:param string groupId
    @:param string title 内容
    @:param string content 消息
    @:return mixed
    '''

    def addGroupNotice(self, groupId, title, content):
        return self.__addDataCell(self.TYPE_GROUP_ADD_NOTICE, 0, 0, groupId, '', title, content, 0)

    '''
    # 发群作业（管理）。注意作业名和标题中不能含有#号
    @:param string groupId
    @:param string homeworkName 作业名
    @:param string title 标题
    @:param string content 内容
    @:return mixed
    '''

    def addGroupHomework(self, groupId, homeworkName, title, content):
        return self.__addDataCell(self.TYPE_GROUP_ADD_HOMEWORK, 0, 0, groupId, '', homeworkName + '#' + title, content,
                                  0)

    '''
    # 主动申请加入群
    @:param string groupId 群号
    @:param string reason 加群理由
    @:return mixed
    '''

    def joinGroup(self, groupId, reason=''):
        return self.__addDataCell(self.TYPE_GROUP_JOIN, 0, 0, groupId, '', reason, 0, 0)

    '''
    # 创建讨论组
    @:param string disName 讨论组名。并作为创建后第一条消息发送（激活消息）
    @:param array qqList 需要添加到讨论组的QQ号列表
    @:return mixed 讨论组ID
    '''

    def disGroupCreate(self, disName, qqList=[]):
        qqListStr = ''
        first = True
        for qq in qqList:
            if not first:
                qqListStr += "#"
            qqListStr += qq
            first = False
        return self.__addDataCell(self.TYPE_DIS_CREATE, 0, 0, '', '', disName, qqListStr, 0)

    '''
    # 退出讨论组
    @:param string disGroupId 讨论组ID
    @:return mixed
    '''

    def disGroupQuit(self, disGroupId):
        return self.__addDataCell(self.TYPE_DIS_QUIT, 0, 0, disGroupId, '', '', 0, 0)

    '''
    # 踢出讨论组
    @:param string disGroupId 讨论组ID
    @:param array qqList 欲踢出的QQ号列表
    @:return mixed
    '''

    def disGroupKick(self, disGroupId, qqList=[]):
        qqListStr = ''
        first = True
        for qq in qqList:
            if not first:
                qqListStr += "#"
            qqListStr += qq
            first = False
        return self.__addDataCell(self.TYPE_DIS_KICK, 0, 0, disGroupId, '', qqListStr, 0, 0)

    '''
    # 添加讨论组成员
    @:param string disGroupId 讨论组号
    @:param array qqList 欲添加的QQ号列表
    @:return mixed
    '''

    def disGroupInvite(self, disGroupId, qqList=[]):
        qqListStr = ''
        first = True
        for qq in qqList:
            if not first:
                qqListStr += "#"
            qqListStr += qq
            first = False

        return self.__addDataCell(self.TYPE_DIS_INVITE, 0, 0, disGroupId, '', qqListStr, 0, 0)

    '''
    # 邀请QQ入群（管理+群员）
    @:param string groupId 群号
    @:param string qq QQ
    @:return mixed 状态
    '''

    def groupInvite(self, groupId, qq):
        return self.__addDataCell(self.TYPE_GROUP_INVITE, 0, 0, groupId, '', qq, 0, 0)

    #  获取信息：注意获取反馈消息，通过ID识别  #

    '''
    # 获取陌生人信息
    @:param string qq
    @:return mixed
    '''

    def getStrangerInfo(self, qq):
        return self.__addDataCell(self.TYPE_GET_STRANGER_INFO, 0, 0, '', qq, '', {}, 0)

    '''
    # 获取当前登录QQ isCallback情况
    @:return mixed
    '''

    def getLoginQQ(self):
        return self.__addDataCell(self.TYPE_GET_LOGIN_QQ, 0, 0, '', '', '', {}, 0)

    '''
    # 获取当前QQ群列表
    @:return mixed
    '''

    def getGroupList(self):
        return self.__addDataCell(self.TYPE_GET_GROUP_LIST, 0, 0, '', '', '', {}, 0)

    '''
    # 获取当前登录QQ好友列表
    @:return mixed
    '''

    def getFriendList(self):
        return self.__addDataCell(self.TYPE_GET_FRIEND_LIST, 0, 0, '', '', '', {}, 0)

    '''
    # 获取指定群群成员列表
    @:param string groupId
    @:return mixed
    '''

    def getGroupMemberList(self, groupId):
        return self.__addDataCell(self.TYPE_GET_GROUP_MEMBER_LIST, 0, 0, groupId, '', '', {}, 0)

    '''
    # 获取群公告
    @:param string groupId
    @:return mixed
    '''

    def getGroupNotice(self, groupId):
        return self.__addDataCell(self.TYPE_GET_GROUP_NOTICE, 0, 0, groupId, '', '', {}, 0)

    '''
    # 获取对方QQ赞数量
    @:param qq
    @:return mixed
    '''

    def getLikeCount(self, qq):
        return self.__addDataCell(self.TYPE_LIKE_COUNT_GET, 0, 0, '', qq, '', {}, 0)

    '''
    # 获取讨论组列表
    @:return mixed
    '''

    def getLDisGroupList(self):
        return self.__addDataCell(self.TYPE_GET_DIS_LIST, 0, 0, '', '', '', {}, 0)

    '''
    # 获取QQ等级
    @:param string qq QQ
    @:return mixed
    '''

    def getQQLevel(self, qq):
        return self.__addDataCell(self.TYPE_GET_QQ_LEVEL, 0, 0, '', qq, '', {}, 0)

    '''
    # 查看群成员名片
    @:param string groupId 群号
    @:param string qq QQ
    @:return mixed 名片
    '''

    def getGroupMemberCard(self, groupId, qq):
        return self.__addDataCell(self.TYPE_GET_QQ_LEVEL, 0, 0, groupId, qq, '', {}, 0)

    '''
    # 查询QQ是否在线
    @:param string qq QQ
    @:return mixed 是否在线
    '''

    def getQQIsOline(self, qq):
        return self.__addDataCell(self.TYPE_GET_QQ_ONLINE_STATUS, 0, 0, '', qq, '', {}, 0)

    '''
    # 查询QQ是否好友
    @:param string qq QQ
    @:return mixed 是否好友
    '''

    def getQQIsFriend(self, qq):
        return self.__addDataCell(self.TYPE_GET_QQ_IS_FRIEND, 0, 0, '', qq, '', {}, 0)

    '''
    # 获取当前QQ机器人状态信息（如是否在线）
    @:return mixed 结构信息
    '''

    def getQQRobotInfo(self):
        return self.__addDataCell(self.TYPE_GET_QQ_ROBOT_INFO, 0, 0, '', '', '', {}, 0)

    '''
    # 置正在输入 状态，发送消息撤销
    @:param string qq QQ
    @:return mixed 状态
    '''

    def setInputStatus(self, qq):
        return self.__addDataCell(self.TYPE_SET_INPUT_STATUS, 0, 0, '', qq, '', {}, 0)
