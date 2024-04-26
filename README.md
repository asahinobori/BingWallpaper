# Bing Wallpaper
![](https://cn.bing.com/th?id=OHR.KalalochTree_ZH-CN9427839259_UHD.jpg&w=1000)2024-04-26: [卡拉洛奇树，又名生命之树，卡拉洛奇海滩，奥林匹克国家公园，华盛顿州，美国 (© Abbie Warnock-Matthews/Shutterstock)](https://cn.bing.com/th?id=OHR.KalalochTree_ZH-CN9427839259_UHD.jpg&rf=LaDigue_UHD.jpg&pid=hp&w=3840&h=2160&rs=1&c=4)

# About
**1) Download bing wallpaper**  
**2) Set desktop wallpaper on Windows system**  
  
# Usage
```
python BinWP.py [-p] [-n num]
```
or
```
pip install pyinstaller
pyinstaller --noconsole --onefile BinWP.py
BinWP.exe [-p] [-n num]
```
to get the exe file work for windows
  
**note:**  
use system crontab to excute it every day

# URL param
| param | description |
| --- | --- |
| format | 返回的数据格式。hp为html格式；js为json格式；其他值为xml格式。 |
| idx | 获取特定时间点的数据。如idx=1表示前一天（昨天），依此类推。经过测试最大值为7。 |
| n | 获取数据的条数。经测试，配合上idx最大可以获取到13天前的数据，即idx=7&n=7。 |
| pid | 未知。pid为hp时，copyrightlink返回的是相对地址。pid不为hp时，没有看到og信息。 |
| ensearch | 指定获取必应【国际版/国内版】的每日一图。当ensearch=1时，获取到的是必应国际版的每日一图数据。默认情况和其他值情况下，获取到的是必应国内版的每日一图数据。
| quiz | 当quiz=1时，返回必应小测验所需的相关数据。 |
| og | 水印图相关的信息。包含了title、img、desc和hash等信息。 |
| uhd | 当uhd=1时，可以自定义图片的宽高。当uhd=0时，返回的是固定宽高（1920x1080）的图片数据。 |
| uhdwidth | 图片宽度。当uhd=1时生效。最大值为3840，超过这个值当作3840处理。 |
| uhdheight | 图片高度。当uhd=1时生效。最大值为2592，超过这个值当作2592处理。 |
| setmkt | 指定图片相关的区域信息。如图片名中包含的EN-CN、EN-US或者ZH-CN等。当域名为global.bing.com时才会有相应变化。值的格式：en-us、zh-cn等。 |
| setlang | 指定返回数据所使用的语言。值的格式：en-us、zh-cn等。 |

# Others
an excellent java implementation: [bing-wallpaper](https://github.com/niumoo/bing-wallpaper)
