# PhysicsExp
### USTC Physics Experiments Data Processing Tools

### 中科大大物实验数据处理工具

#### Comes with NO WARRENTY

The package is also released on [pypi](https://pypi.org/project/physicsexp/).

This README is shown in both pypi package and github repo, but is designed for github only. 

For readers from pypi, [here](https://github.com/ustcpetergu/PhysicsExp) please. 

- The github repo(ustcpetergu/PhysicsExp) includes: physicsexp python package(directory `physicsexp`), my experiment data(in directory `Experiments`, archived by semester), some misc files and automation scripts. 

- The pypi package(physicsexp) only includes the main python package, but that's enough and easy to use. 

最终目的是建造一套用于自动化处理大物实验数据、绘制图像、生成可打印文档、将文档提交到在线打印系统的工具；针对常用数据处理需求实现简化和自动化，只要简单的几行代码，就能完成通用的绘图、拟合、不确定度计算等大物实验常用任务。
理想与现实差距还很大，目前仅仅包装了一些matplotlib绘图库和文件输入简化重复劳动。

### A Simple Guide

#### The easy way 

Create a virtualenv(here named test-env)

```
python -m venv test-env
```

Activate it

```
./test-env/Scripts/activate.bat
```

Install the package from pypi, (optional) use mirror to accelerate

```
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple physicsexp
```

Run the scripts you downloaded from github in the virtualenv

```
python path/to/plot.py
```

You'll see graphs poped out and saved to .png, a generated gen.docx ready to print, and calculations(if any) printed to output. Then you can modify the code or write your own code to process data!

#### For advanced users 

Assuming you are using Windows.

**Change the command to make then work on your device! Don't just copy & paste!**

 **Prepare to build**

Set up environment to build and release python packages, detailed guide can be found on pypi website. 

**Build**

```
python setup.py sdist bdist_wheel
```

Then the packaged wheel file can be found at `./dist/physicsexp-0.0.1-py3-none-any.whl`(Name may be different)

**Install**

**This package haven't been tested as it should and I don't know what will happen after installation.**

**So use a virtualenv is recommended. **

Create a virtualenv(here named test-env)

```
python -m venv test-env
```

Activate it

```
./test-env/Scripts/activate.bat
```

Install the wheel (Use USTC mirror to accelerate, and it will download and install other required packages)

```
pip install -i https://mirrors.ustc.edu.cn/pypi/web/simple path\to\physicsexp-0.0.1-py3-none-any.whl
```

Wait a moment for the installation to finish.

**Use**

Launch python in your venv

```
python
```

Import the package (`from xxx import *` may be bad, don't imitate me)

```
>>> from physicsexp.mainfunc import *
>>> from physicsexp.gendocx import *
>>>
```

Enjoy. 

### Usage

Wanna know how to use? Read the source code yourself, see templates at `physicsexp/Template/` and examples at `Experiments/`(Most of them are already outdated and cannot be run, if you really need to run them, maybe a `git reset` is the last way) , or contact developer.

But most of the time neither of these works. 

**And can using these tools boost your efficiency? I don't know, but probably can't. **

**Finally, think twice before wasting time on this project, instead, enjoy your life, learn some real physics, and find a (boy|girl)friend. **

