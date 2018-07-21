# fckjdp

1,项目开发过程中需要使用新的依赖,可以使用如下命令下载

pip install XXX 安装XXX

2,在项目开发的过程中,每使用一个新的依赖的时候,都必须把对应的依赖版本添加到requirements文件中

pip freeze > requirements.txt

3,在把项目移植到新的环境的时候使用如下命令来导入依赖

pip install -r requirements.txt

本项目编程规范:

1,类的名字必须使用驼峰格式,（类名字中不能含有数字！！！）
eg：UserName

2,类的参数每个单词小写并使用_分割（不能出现大写字母）
eg:up_to_down

3,方法参数的逗号后面要有空格间隔,方法参数里面的=两边不能出现空格
eg:up_to_down = models.CharField(max_length=10, verbose_name=u'昨日涨停今日受益', null=True, blank=True)
