
### Python支持版本：
支持python3.5及以上版本

### 环境初始化：
```
sh create-venv.sh
. venv/bin/activate
pip install -r requirements.txt
```

### 运行：
```
. venv/bin/activate
python main.py --env=dev --logging=debug --log_file_prefix=log/fengcun.log
```
或者
```
后台运行：
sh bootstrap.sh start

前台运行：
sh bootstrap.sh run
```

### API文档
- [https://documenter.getpostman.com/view/5245402/S1ETRwW9](https://documenter.getpostman.com/view/5245402/S1ETRwW9)

### 其他
* 1. 不需要将对某些资源的访问API分成管理端和客户端，只需要通过不同的授权文件就可以区别，比如对普通用户可以配以通用授权，VIP用户授予高级授权即可；