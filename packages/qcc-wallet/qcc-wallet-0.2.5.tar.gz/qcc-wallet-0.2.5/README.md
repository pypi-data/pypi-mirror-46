
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
./bootstrap.sh start
或者：
bash bootstrap.sh start

前台运行：
./bootstrap.sh run
或者：
bash bootstrap.sh run
```

### API文档
- [https://documenter.getpostman.com/view/5245402/S1ETRwW9](https://documenter.getpostman.com/view/5245402/S1ETRwW9)
