---
name: wechat-reader
description: 读取微信群聊记录，提取任务、决策、需求信息。触发词：「读取群聊」「微信记录」「剧组群」。
---

# WeChat Reader Skill

读取"多参宗外传-剧组"群聊记录的工具。

## 服务状态

服务运行在 `http://127.0.0.1:5030`

**注意**：微信重启后需要重新启动服务：
```bash
cd ~/wechat-mac-reader && ~/go/bin/chatlog server --config ./data &
```

## 查询命令

### 获取今天的消息
```bash
curl -s "http://127.0.0.1:5030/api/v1/chatlog?talker=54344232897@chatroom&limit=100&time=2026-04-06"
```

### 获取指定日期的消息
```bash
curl -s "http://127.0.0.1:5030/api/v1/chatlog?talker=54344232897@chatroom&limit=100&time=2026-04-05"
```

### 获取最近30条消息（不带时间参数会报错）
```bash
curl -s "http://127.0.0.1:5030/api/v1/chatlog?talker=54344232897@chatroom&limit=30&time=2026-04-06"
```

## 群信息

- **群名**：多参宗外传-剧组
- **wxid**：54344232897@chatroom
- **用途**：AI视频创作素材提取

## 服务管理

启动服务：
```bash
cd ~/wechat-mac-reader && ~/go/bin/chatlog server --config ./data &
```

检查服务状态：
```bash
curl -s http://127.0.0.1:5030/health
```

查看日志：
```bash
tail -f ~/wechat-mac-reader/data/chatlog.log
```

## 注意事项

1. 服务仅监听 localhost:5030，无安全风险
2. 微信重启后需要重新提取密钥并启动服务
3. 图片和视频通过 `http://127.0.0.1:5030/video/xxx` 或 `/image/xxx` 访问
