# 快速创建一个FastAPI项目

> [Demo](https://apidemo.reviy.top/docs)

## 安装环境

推荐版本：python3.9

```shell
pip install -r requirements.txt
```

## 启动项目

> 直接运行主程序(会使用configs/config.yml中的配置)
>
> ```shell
> python main.py
> ```

> 使用uvicorn
>
> ```shell
> uvicorn main:app --reload
> ```

## 访问接口文档

地址：http://@server.host:@server.port/docs (server对应configs/config.yml里的server)

例：[http://0.0.0.0:8080/docs](http://0.0.0.0:8080/docs "接口文档")

## 部署到vercel

> 参考链接：[【Vercel】通过Vercel部署fastapi服务 | IntoTheDark&#39;s Blog](https://intothedark.top/posts/35463/)

# 项目结构

## applications-路由子应用

添加子应用参考applications/index，将子应用放到applications下，然后在main.py中的routers添加Router

## configs-项目配置信息

## databases-项目数据库

## utils-常用工具

### auth-认证功能

### database-数据库管理

### middleware-中间件

### router-路由管理

## auth_init.py-初始化管理员用户

> 如果要用Oauth认证就改好用户信息再运行

## Dockerfile-用于创建Docker image

## main.py-主程序

## requirements.txt-所需要安装的包

## vercel.json-vercel配置文件
