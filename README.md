jiedu日志可视化工具说明
========

## 0. 介绍

这个工具是用Flask搭建的简略web服务器，期望能够借助网页，直观的查看jiedu对话日志中一些统计信息（比如查看对话中，系统和用户语义交互的大致过程）。或许还可以用来分析异常？分析用户习惯？

主要环境：Python 2.7+, Flask, d3js

参考网站：

[https://d3js.org/](https://d3js.org/)

[http://www.ourd3js.com/wordpress/](http://www.ourd3js.com/wordpress/)

[http://docs.jinkan.org/docs/flask/](http://docs.jinkan.org/docs/flask/)


## 1. 如何打开网页并可视化观察数据？

#### Step1. 进入 "jiedu_log" 目录，运行 `python server.py`

> 如果本机5000端口已经被占用想要修改端口为6000，请打开 `server.py` 文件，修改 `app.run(host='0.0.0.0')` 为 `app.run(host='0.0.0.0', port=6000)` 

#### Step2. 打开浏览器，输入网址 `localhost:5000` 

> 如果修改了端口，则打开相应端口的网址。网页大概的样子：![](jiedu_display.jpg)

#### Step3. 网页左侧 *"目录"* 随便选一个，比如 `jiedu1`，下面领域随便选一个，比如`multi` ，则可在右侧大框框中看到一个树状结构。

> 
1. 鼠标移动到任意节点可以查看该节点上的统计数据；
2. 空心节点表明节点被展开，实心节点表面节点未展开；
3. 点击右侧 `legend` 可查看不同颜色节点的含义；
4. 方形节点是用户动作，圆形节点是系统动作；
5. 节点之间连线的粗细表明成功率（success）的大小；
6. 每一列节点按照转义概率（count）的大小排序，节点越大表明count越大（非线性）；
7. 鼠标移动到右侧大框框时，滚动鼠标滚轮可放大缩小页面；
8. 拖动图像的方法：在大框框内空白处点击并按住不放->按住不放移动到另一点->松开鼠标；
9. 当把某个节点一直展开直到尾节点时，点击查看日志可以查看处在“展开路径”上的所有日志。

#### Step4. 如果有新的数据想要可视化显示，比如叫 `xxx.json` ，怎么可视化？

> 
1. 直接在目录 "logs" 下面找个子目录放入该文件即可，比如放到 "logs/jiedu1"下，重新进行Step1、Step2、Step3，就能在 `jiedu1` 目录下找到 `xxx` ，点击即可；
2. 或在目录 "logs" 新建一个子目录比如 `haha` 再把该文件放进去，重新进行Step1、Step2、Step3，就能在 `haha` 目录下找到 `xxx` ；
3. 或通过正在运行的网页左下角的上传控件上传，上传的文件会被保存成 "logs/uploads/tree.json" 文件，并立即显示在右侧大框框。此方法最好只做临时查看，小心文件覆盖导致麻烦。
> 
请保证新文件以 `.json` 为后缀，且格式正确。不然网站估计会崩。。。
> 
注意：只有相应的原始日志也在服务器存放时，才能在网页上某个尾节点查看日志。比如 `jiedu1/multi.json` 同一级应该有个文件夹 `jiedu1/multi` 存放对应所有日志。

## 2. 如何生成能够被网页正确读取的数据？

#### Step1. `dialogue_jiedu.py`

假设现在有了jiedu给的原始数据 `all.txt` ，我们先将其拆分成单独json文件并存放到指定目录下。
脚本 `dialogue_jiedu.py` 的开头定义了若干个不同的目录，你可能需要修改 `root_dir` 和 `log_file_raw` 这两个变量。
拆分后对于每个领域我们会得到一个叫 "dialogs" 的文件夹，里面是不同领域的对话日志，每个对话单独一个文件。

#### Step2. `count_dialogue.py`

假设经过Step1我们得到了multi领域的一个文件夹，我们把该文件夹与 `count_dialogue.py` 放在同一目录，修改脚本中的领域为 `domain="multi"` （脚本中的 `filter_num` 根据情况修改）。运行该脚本可以得到 `multi.json` 。
该json文件可以被网站正确读取，将该multi文件夹与multi.json放在服务器同一目录下可以在网页上查看日志，具体上面Step4已经提到了。

#### Summary. 数据的完整目录结构是类似下面这样的

```
├── logs
│   ├── jiedu1
│   │   ├── multi.json
│   │   ├── multi
│   │   │   ├── 0001518e33279302b9000003.json
│   │   │   ├── 0001518f33279302cb000003.json
│   │   │   ├── 0001519033279302a1000003.json
│   │   │   ├── 0001519033279302af000003.json
│   │   │   ├── ......
│   │   ├── music.json
│   │   ├── music
│   │   │   ├── xxxxxxxxxxxxxxxxxxxxxxxx.json
│   │   │   ├── yyyyyyyyyyyyyyyyyyyyyyyy.json
│   │   │   ├── zzzzzzzzzzzzzzzzzzzzzzzz.json
│   │   │   ├── ......
│   │   ├── ......
│   └── uploads
│       ├── tree.json
│       └── ......
......
```

## 其他

有些目录下可能会有叫 `sample_dialogue.py` 的脚本，是用来在某一领域的所有log中随机采样指定个数日志的。与可视化无关。。。


----------

> Written with [StackEdit](https://stackedit.io/).
