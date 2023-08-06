---

#### 1.查询条件追加

```
bbsj_dict = {"bxdata_tjsjly": "报备数据"}
Sel_Cond = dict(Sel_Cond, **bbsj_dict)
```
#### 2.去掉tuoken认证 

```
去掉tuoken认证 
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
```

#### 3.数组转字符串与字符串转数组