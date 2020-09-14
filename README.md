# 使用 python fastapi+vue 快速搭建网站

# 概述

传统网站由一个 web 框架完全承担，例如基于 nodejs 的 express，koa，基于 python 的 django，tornado。新型网站演变为用 vue 开发前端系统，使用 api 框架开发后端 api 请求接口的模式。本文就介绍一下后端使用 python 的 fastapi 框架开发 api 接口，前端使用 vue 框架开发界面的方式快速开发网站。

# 搭建 fastapi 服务

首先建立一个项目文件夹，并建立两个子文件夹 backend 和 frontend。后端的代码将放置在 backend 文件夹中，前端的代码放在 frontend 文件夹里。

## 安装 fastapi

```bash
cd backend
pip install fastapi uvicorn
```

## 编写 api 接口文件 backend/app/**init**.py

```python
from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
```

## 运行后端服务

```bash
uvicorn app:app --reload --host 0.0.0.0
```

## 验证是否运行成功

curl [http://127.0.0.1:8000/items/5?q=somequery](http://127.0.0.1:8000/items/5?q=somequery)

## 查看自动生成文档

[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

# 搭建 vue 前端

这里我们采用了 ant design pro vue 作为我们的脚手架。

```bash
cd frontend
git clone --depth=1 https://github.com/vueComponent/ant-design-vue-pro.git .
yarn install
yarn serve
```

完成后，前端系统就运行在 8000 端口了。但此时，我们看到的前端只是一个静态网站，并没有动态内容。所有和后端的交互都是通过 mock 方式模拟的。在正式环境中，这些请求需要和之前搭建的 fastapi 后端交互完成。

## 添加 hello world 页面

在 frontend/src/views/helloworld 目录下，加入我们的页面 HelloWorld.vue

```vue
<template>
  <div>
    <h1>hello world</h1>
  </div>
</template>
```

将 hello 页面加入路由，修改 frontend/src/config/router.config.js,把 asyncRouterMap 修改为如下内容

```javascript
export const asyncRouterMap = [
  {
    path: "/",
    name: "index",
    component: BasicLayout,
    meta: { title: "menu.home" },
    redirect: "/helloworld",
    children: [
      // helloworld
      {
        path: "/helloworld",
        name: "hello-world",
        component: HelloWorld,
        meta: {
          title: "menu.hello",
          icon: "folder",
          permission: ["dashboard"],
        },
      },
    ],
  },
  {
    path: "*",
    redirect: "/404",
    hidden: true,
  },
];
```

此时，菜单的名字将显示 menu.hello，原因是我们没有在国际化中添加对 menu.hello 词条的翻译选项，我们修改 frontend/src/locales/lang/en-US.js 增加如下选项

```javascript
const locale = {
  message: '-',
  'menu.home': 'Home',
  'menu.dashboard': 'Dashboard',
  'menu.hello': 'Hello', // 新增的内容
```

同样修改 frontend/src/locales/lang/zh-CN.js

```javascript
const locale = {
  message: '-',
  'menu.home': '主页',
  'menu.hello': '问候', // 新增的内容
```

这样，我们就能看到正确的支持多语言的版本了。

## 添加对 API 请求

在 frondend/src/api/hello.js 中添加和 hello 相关的 api

```javascript
import { axios } from "@/utils/request";

const api = {
  Hello: "hello",
};

export default api;

export function getHello() {
  return axios.get(api.Hello, {});
}
```

为了调试方便，我们使用 mock 功能在没有后端联调情况下模拟后端操作, 修改 frontend/src/views/helloworld/HelloWorld.vue

```vue
<template>
  <div>
    <h1>{{ loading }}</h1>
    <h1>{{ data }}</h1>
  </div>
</template>

<script>
import { getHello } from "@/api/hello";
import { PageView } from "@/layouts";

export default {
  name: "HelloWorld",
  components: {
    PageView,
  },
  data() {
    return {
      data: [],
      loading: false,
    };
  },
  mounted() {
    this.fetch();
  },
  watch: {
    $route(to, from) {
      this.fetch();
    },
  },
  computed: {
    title() {
      return `hello, world`;
    },
  },
  methods: {
    fetch() {
      this.loading = true;
      return getHello()
        .then((data) => {
          this.loading = false;
          this.data = data;
        })
        .catch((err) => {
          this.$notification.error({
            duration: null,
            message: err,
          });
          this.loading = false;
        });
    },
  },
};
</script>
```

这样，访问首页时就能够看到后台模拟 mock 接口传回的数据。

# 将 vue 编译，由 fastapi 托管

编译 vue 代码，生成的产品正式代码在 dist 目录下

```vue
yarn install && yarn run lint --no-fix && yarn run build --mode production
```

把编译好的 dist 代码全部移动到 backend 的 public 目录下。这个过程我们可以使用 bash 脚本自动化

```bash
#!/bin/bash
function fvtlog() {
    echo 【 FastAPIVueTemplate Build 】====\> $@
}

build_dir=$(pwd)
client_dir=$(pwd)/frontend
server_dir=$(pwd)/backend

ENV=$1
ENV="${ENV:-production}"

function buildClient() {
    fvtlog "start building client for FastAPIVueTemplate..."
    cd $client_dir
    yarn install && yarn run lint --no-fix && yarn run build --mode $ENV
}

function buildServer() {
    fvtlog "start build server for FastAPIVueTemplate"
    rm -rf $server_dir/public
    cd $build_dir
    mv $client_dir/dist $server_dir/public
}

buildClient
buildServer
```

此时，我们需要配置 fastapi 完成以下的路由

1. 对/api 请求使用 fastapi 的处理逻辑
1. 对/api 下的其他未实现请求返回 404
1. 对所有其他请求尝试加载 public 目录下的资源文件，若失败，则加载 index.html，但路径仍保持请求路径。

这就是 vue 文件托管的 html5 history mode [https://router.vuejs.org/guide/essentials/history-mode.html](https://router.vuejs.org/guide/essentials/history-mode.html)

修改 backend/app/**init**.py 为如下内容

```python
import os.path
import time
from fastapi import  FastAPI
from fastapi.staticfiles import StaticFiles

# Use this to serve a public/index.html
from starlette.responses import FileResponse
from starlette.responses import PlainTextResponse

app = FastAPI()

@app.post("/api/auth/login")
def get_auth_login():
    data = {
        'id': 'id_001',
        'name': 'admin',
        'username': 'admin',
        'password': '',
        'avatar': 'https://gw.alipayobjects.com/zos/rmsportal/jZUIxmJycoymBprLOUbT.png',
        'status': 1,
        'telephone': '',
        'lastLoginIp': '27.154.74.117',
        'lastLoginTime': 1534837621348,
        'creatorId': 'admin',
        'createTime': 1497160610259,
        'deleted': 0,
        'roleId': 'admin',
        'lang': 'zh-CN',
        'token': '4291d7da9005377ec9aec4a71ea837f'
    }
    return dict(result=data, message='', code=200, _status=200)

@app.get("/api/user/info")
def get_user_info():
    info = {
        'id': '4291d7da9005377ec9aec4a71ea837f',
        'name': '天野远子',
        'username': 'admin',
        'password': '',
        'avatar': '/avatar2.jpg',
        'status': 1,
        'telephone': '',
        'lastLoginIp': '27.154.74.117',
        'lastLoginTime': 1534837621348,
        'creatorId': 'admin',
        'createTime': 1497160610259,
        'merchantCode': 'TLif2btpzg079h15bk',
        'deleted': 0,
        'roleId': 'admin',
        'role': {}
    }
    role = {
        'id': 'admin',
        'name': '管理员',
        'describe': '拥有所有权限',
        'status': 1,
        'creatorId': 'system',
        'createTime': 1497160610259,
        'deleted': 0,
        'permissions': [{
        'roleId': 'admin',
        'permissionId': 'dashboard',
        'permissionName': '仪表盘',
        'actions': '[{"action":"add","defaultCheck":false,"describe":"新增"},{"action":"query","defaultCheck":false,"describe":"查询"},{"action":"get","defaultCheck":false,"describe":"详情"},{"action":"update","defaultCheck":false,"describe":"修改"},{"action":"delete","defaultCheck":false,"describe":"删除"}]',
        'actionEntitySet': [{
            'action': 'add',
            'describe': '新增',
            'defaultCheck': False
        }, {
            'action': 'query',
            'describe': '查询',
            'defaultCheck': False
        }, {
            'action': 'get',
            'describe': '详情',
            'defaultCheck': False
        }, {
            'action': 'update',
            'describe': '修改',
            'defaultCheck': False
        }, {
            'action': 'delete',
            'describe': '删除',
            'defaultCheck': False
        }],
        'actionList': None,
        'dataAccess': None
    }]}
    info['role'] = role
    return dict(result=info, message='', code=200, _status=200)

@app.post("/api/auth/2step-code")
def auth_2step_code():
    return { 'stepCode': 0 }

@app.get("/api/hello")
def hello():
    return {'message': 'hello world when '+str(int(time.time()))}

@app.get("/api/{wildcard}")
async def get_api_404():
    return PlainTextResponse("api not found")

@app.get("/")
async def get_index():
    return FileResponse('public/index.html')

@app.get("/{whatever:path}")
async def get_static_files_or_404(whatever):
    # try open file for path
    file_path = os.path.join("public",whatever)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    return FileResponse('public/index.html')

```

有几个要点：

1. app.get 的参数是路径名，注意和顺序相关，优先匹配最早的符合。另外，如果要匹配的参数中包括/，那么需要在参数后加：path 修饰符
1. 按照顺序分别匹配/api 路径，根目录，然后将所有未匹配请求发送给最后一个函数。如果找到静态文件则返回其内容，否则就直接用 index.html 的内容返回。vue 会处理具体的路由渲染规则。
1. ant design pro 本身自带权限控制系统，但是需要注意的是，原有的 mock 文件中的响应是需要加上包装的，比如 result 等于 mock 中 builder 的参数。这个没有文档提及，这块浪费了很多调试时间。
1. 还有一些接口没有实现，这个文件只是包含了刚好能够让登陆用户进入系统的最小 api 需要的接口

# 总结

总体而言，fastapi+vue 的部署方式简单高效，能满足一般应用类网站特别是中台的开发需求。但在开发过程中需要注意将 vue 的编译文件托管给 fastapi 时的相关配置。

项目地址：[https://github.com/elprup/fastapi-vue-template](https://github.com/elprup/fastapi-vue-template)

# 相关引用

golang+vue 的实现例子 [https://github.com/Sloaix/Gofi](https://github.com/Sloaix/Gofi)
