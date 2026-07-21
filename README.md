# Tank Trouble

这是一个基于 `pygame` 的本地双人坦克对战游戏，包含简单的碰撞检测、墙体反弹和自定义地图编辑功能。

## 功能简介

- 本地双人对战
- 坦克移动与旋转
- 子弹发射与碰撞检测
- 墙壁碰撞回退与子弹反弹
- 使用 `maps.json` 加载地图布局
- 内置地图编辑器 `map_editor.py`

## 运行环境

- Python 3.8 及以上
- Windows 系统（当前代码使用 Windows 字体路径加载中文字体）
- 推荐安装 `pygame`

## 安装依赖

```bash
pip install -r requirements.txt
```

> `requirements.txt` 中包含项目依赖以及一些可选开发工具。实际运行游戏时，最重要的是 `pygame`。

## 运行游戏

在项目根目录下运行：

```bash
python tanktrouble.py
```

## 游戏控制

- 玩家1：
  - `W`：前进
  - `S`：后退
  - `A`：左转
  - `D`：右转
  - `Space`：发射子弹
- 玩家2：
  - `↑`：前进
  - `↓`：后退
  - `←`：左转
  - `→`：右转
  - `Enter`（数字键盘）：发射子弹
- `Esc`：退出游戏
- 游戏结束后按 `R` 重新开始

## 地图编辑器

使用 `map_editor.py` 编辑 `maps.json` 中的地图元素。

主要操作：

- 左键：添加/移动元素
- 右键：切换元素类型
- `Shift+右键`：删除元素
- 方向键：调整选中元素大小
- `Ctrl+S`：保存地图

地图文件 `maps.json` 中的元素包含位置、尺寸和类型，用于生成游戏中的墙体。

## 项目结构

- `tanktrouble.py`：游戏主程序
- `sprites.py`：坦克、子弹、墙壁精灵实现
- `map_editor.py`：地图编辑器
- `maps.json`：地图数据
- `requirements.txt`：依赖列表

## 说明

当前项目是一个学习型 `pygame` 小项目，适合用来演示简单的游戏逻辑、碰撞检测和本地双人操作。现有地图可通过 `maps.json` 修改或使用地图编辑器创建新的布局。
