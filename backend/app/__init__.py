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
