#关于
Terry-toolkit常用函数整理的工具包

## 安装
```
pip3 install Terry_toolkit
```


## 使用
 

```

from Terry-toolkit import file

tfile=file.File()


## 生成依赖

pip3 freeze > requirements.txt


## 提交包
python3 setup.py sdist
# #python3 setup.py install
python3 setup.py sdist upload


## 构建文档
```
mkdir docs
cd docs
sphinx-quickstart
cd ../

#使用这个

sphinx-apidoc -f -o docs/source/ Terry_toolkit  -e --ext-autodoc --ext-githubpages --ext-viewcode --ext-todo
cd docs
#不需要 sphinx-build -b html source build 
make html
```



其它库推荐

cacheout  #函数缓存
pip install MagicBaidu