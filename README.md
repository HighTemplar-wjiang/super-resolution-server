# super-resolution-server
A deep-learning based super resolution server. 

### Dependency
```shell
pip install fastapi opencv-python opencv-contrib-python
```

### Quick-start
```shell
cd server
uvicorn fastapi_server:app --host 0.0.0.0 --reload
```
