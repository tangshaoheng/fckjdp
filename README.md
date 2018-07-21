# fckjdp

1,项目开发过程中需要使用新的依赖,可以使用如下命令下载

pip install XXX 安装XXX

2,在项目开发的过程中,每使用一个新的依赖的时候,都必须把对应的依赖版本添加到requirements文件中

pip freeze > requirements.txt

3,在把项目移植到新的环境的时候使用如下命令来导入依赖

pip install -r requirements.txt