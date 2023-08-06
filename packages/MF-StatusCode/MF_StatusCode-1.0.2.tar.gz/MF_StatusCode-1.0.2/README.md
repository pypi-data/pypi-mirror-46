# 状态代码包

## 项目描述

蝰蛇软件工作室 - 状态管理包

工作室内部项目使用的python包

项目地址 https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_statusCode_python

## 安装

```sh
# 版本号可自行更改
# 只供内部使用。若无权限访问请联系开发者
pip install https://git-codecommit.us-west-2.amazonaws.com/v1/repos/MF_statusCode_python#1.0.0
```

## 测试

### 测试指令

运行自动化测试

```sh
coverage run test.py
```

### 测试覆盖查询

```sh
coverage report
```

### 测试覆盖生成html

```sh
coverage html -d covhtml --omit=env/*,tests/*
```