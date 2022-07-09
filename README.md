# Pgzrun-BiFiT
_made by Ninecloud Latest:2022/7/9_  
_本来不想写README，github一催就写得停不下来了_  
基于[Python](https://www.python.org)中的[Pygame-Zero](https://pygame-zero.readthedocs.io)  
***
## 基本玩法
玩家分为红/蓝两队，在踏板上战斗  
每一方初始拥有10生命，某一方血量归零则另一方胜利  
此时主键盘回车键重新开始
## 键位
* 红队键位：AD移动，W跳跃，空格射击子弹
* 蓝队键位：左右键移动，上键跳跃，小键盘Enter键射击子弹
## 高精尖玩法
### 各种子弹
* [Bullet](images/pistol.png):碰到敌人造成1伤害。
* [IceRocket](images/icerocket.png):发射后飞到屏幕顶端，等待0.75秒后向随机一个敌人落下，碰到敌人或踏板时发出冰冻气场，造成2伤害并冰冻1秒。作为接得准的奖励，直接碰到火箭的玩家额外被造成2伤害。
### 踏板上的道具
* [Heal](images/heal.png):碰到的玩家可以恢复2生命值。玩家生命无上限。
* [Shield](images/shield.png):碰到后玩家获得3秒无敌。不会受到任何伤害，但会被冰冻或击飞。
* [IceRocket](images/ice.png):碰到后发射一枚冰冻火箭。
***
## 感谢其它工具
* [Github](https://github.com):源代码托管
* [kooriookami](https://tools.kooriookami.top/#/pixel-art):第二版画作
* [Python](https://www.python.org)，尤其[Pgzrun](https://pygame-zero.readthedocs.io)