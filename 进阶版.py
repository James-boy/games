# 小经验，一开始不知道输入的是什么且必须输入数据时，可以全部设为0.如类的__init__参数
# 设置一个类，用于保存落子信息，子的位置，是否落子，落什么子，和第几个落子，
# 第几个落子信息加上之前的落什么子等信息用于悔棋
# 子的位置，是否落子和落什么子等可用于其他，如判断输赢
# 反正这个类用处很大

import pygame
import sys
import time
from pygame.locals import *

# 用于记录棋盘信息，每个位置落子情况
initChesslist = []

# 用于保证每次重新开始等情况第一个落子均为某颜色的子，为1表示每次第一个落子为白子，为2表示每次第一个落子为黑子
firstRole = 1        # 此处 1 表示第一个落白子

# 上一个变量用于每次重新开始时进行调参，整个程序中不变。而下面这个变量可在函数运行过程中不断变化
initRole = firstRole

# 用于判断是否结束
resultFlag = 0

# 用于记录刚刚落的是第几子
k = 0
''''# 用于记录每一步棋盘信息，用于悔棋
map = []
for i in range(15*15 + 1):
    for j in range(15):
        map.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        
def map_(i, j, value):
    global map, k
    map[k][i][j] = value
    map[k + 1] = map[k]
    k+=1
用这个悔棋不失为一种方法，不过我想到了其他的，如后面的number 节约资源'''

# 用一个类来描述某棋盘格点的信息，x表示该格点横坐标，y表示该格点纵坐标，
# 0 表示未落子，1 表示落了白子，2 表示落了黑子， number用于表示从开始第几个子
class StornPoint():
    def __init__(self, x, y, value, number):
        self.x = x
        self.y = y
        self.value = value
        self.number = number

# 该函数用于得到棋盘初始信息
def initChessSquare(x, y):
    for i in range(15):
        rowlist = []
        for j in range(15):
            pointx = x + j*41
            pointy = y + i*41
            sp = StornPoint(pointx, pointy, 0, 0)  # 各格点都属于这个类但是互不影响
            rowlist.append(sp)
        initChesslist.append(rowlist)


# 此函数用于判断鼠标点击位置，若该位置某范围内存在格点，将格点信息进行更改，便于后续画图
# 同时该函数调用了后一个函数，用于判断是否有五子相连，如果有，则返回某句话，同时返回一个resultFlag值
def eventHander():
    for event in pygame.event.get():
        global initRole, initChesslist, k
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            i = 0
            j = 0
            for temp in initChesslist:
                for point in temp:
                    # 此处用于判断鼠标位置在哪个格点附近
                    if x >= (point.x - 10) and x <= (point.x + 10) and \
                            y >= (point.y - 10) and y <= (point.y + 10):
                        if point.value == 0 and initRole == 1:
                            point.value = 1
                            point.number = k + 1
                            k += 1
                            judgeResult(i, j, 1)
                            initRole = 2
                        if point.value == 0 and initRole == 2:
                            point.value = 2
                            point.number = k + 1
                            k += 1
                            judgeResult(i, j, 2)
                            initRole = 1
                    j += 1
                i += 1
                j = 0
            # 鼠标点击悔棋时进行如下代码，遍历列表，查看前一个落子的信息，并将其信息进行更改
            if x >= 656 and x <= 716 and y >= 300 and y <= 330:
                for temp in initChesslist:
                    for point in temp:
                        if point.number == k:
                            break  # 一检测到就跳出当前循环，不然会检索下一行，可能出现一下消失几个棋子
                    if point.number == k and point.value == 1:
                        point.value = 0
                        point.number = 0
                        k = k - 1
                        initRole = 1
                        break
                    if point.number == k and point.value == 2:
                        point.value = 0
                        point.number = 0
                        k = k - 1
                        initRole = 2
                        break

            # 点击重新开始时执行如下代码
            if x >= 656 and x <= 776 and y >= 400 and y <= 430:
                initChesslist = []
                initChessSquare(26, 26)
                k = 0
                initRole = firstRole  # 用于保证重新开始后白子先，若要每次黑子先则改为2就行
            # 点击退出时执行如下代码
            if x >= 656 and x <= 716 and y >= 500 and y <= 530:
                pygame.quit()
                sys.exit()

# 用于判断是否有五子相连，如果有，则返回某句话，同时返回一个resultFlag值
def judgeResult(i, j, value):
    global resultFlag
    flag = False
    # 横向赢
    for x in range(i - 4, i + 5):
        if x >= 0 and x + 4 < 15:
            if initChesslist[x][j].value == value and \
                initChesslist[x + 1][j].value == value and \
                initChesslist[x + 2][j].value == value and \
                initChesslist[x + 3][j].value == value and \
                initChesslist[x + 4][j].value == value:
                flag = True
                break
    # 纵向赢
    for y in range(j - 4, j + 5):
        if y >= 0 and y + 4 < 15:
            if initChesslist[i][y].value == value and \
                initChesslist[i][y + 1].value == value and \
                initChesslist[i][y + 2].value == value and \
                initChesslist[i][y + 3].value == value and \
                initChesslist[i][y + 4].value == value:
                flag = True
                break
    # 左上上上！！！方向赢
    for x, y in zip(range(i - 4, i + 5), range(j - 4, j + 5)):
        if x >= 0 and x + 4 < 15 and y >= 0 and y + 4 < 15:
            if initChesslist[x][y].value == value and \
                initChesslist[x + 1][y + 1].value == value and \
                initChesslist[x + 2][y + 2].value == value and \
                initChesslist[x + 3][y + 3].value == value and \
                initChesslist[x + 4][y + 4].value == value:
                flag = True
                break
    # 左下下下！！！方向赢
    for x, y in zip(range(i - 4, i + 5), range(j + 4, j - 5, -1)):
        if x >= 0 and x + 4 <= 15 and y - 4 >= 0 and y < 15:
            if initChesslist[x][y].value == value and \
                initChesslist[x + 1][y - 1].value == value and \
                initChesslist[x + 2][y - 2].value == value and \
                initChesslist[x + 3][y - 3].value == value and \
                initChesslist[x + 4][y - 4].value == value:
                flag = True
                break
    if flag:
        resultFlag = value
        print('白棋赢' if value == 1 else '黑棋赢')

# 用于展示文本
def show_text(screen, txt, place_):
    s_font = pygame.font.Font('字体文件/正楷字体.TTF', 30)
    s_text = s_font.render(txt, True, (0, 0, 0))
    screen.blit(s_text, place_)

def main():
    global initChesslist, resultFlag, initRole, k
    initChessSquare(26, 26)
    pygame.init()
    pygame.mixer.music.load('music/望江南.wav')
    pygame.mixer.music.set_volume(1)
    pygame.mixer.music.play(loops=-1, start=0.0)
    screen = pygame.display.set_mode((826, 626))
    pygame.display.set_caption('小二的五子棋')
    rightground = pygame.image.load('image/棋盘.jpg')
    leftground = pygame.image.load('image/褐色图片.jpg')
    whiteStorn = pygame.image.load('image/白子.jpg')
    blackStorn = pygame.image.load('image/黑子.jpg')
    #whiteStorn.get_rect()
    #blackStorn.get_rect()

    while True:
        screen.blit(rightground, (0, 0))
        screen.blit(leftground, (626, 0))
        show_text(screen, '悔棋', (656, 300))
        show_text(screen, '重新开始', (656, 400))
        show_text(screen, '退出', (656, 500))
        for temp in initChesslist:
            for point in temp:
                if point.value == 1:
                    screen.blit(whiteStorn, (point.x - 18, point.y - 18))
                elif point.value == 2:
                    screen.blit(blackStorn, (point.x - 18, point.y - 18))
        # 用于在右上角展示下一步应该是哪个子
        for temp in initChesslist:
            for point in temp:
                if point.number == k:
                    break
            if point.number == k and point.value == 1:
                screen.blit(blackStorn, (708, 100))
                break
            elif point.number == k and point.value == 2:
                screen.blit(whiteStorn, (708, 100))
                break
        # 如若赢棋执行以下代码
        if resultFlag > 0:
            initChesslist = []
            initChessSquare(26, 26)
            k = 0
            if resultFlag == 1:
                show_text(screen, '白棋赢', (20, 20))
                show_text(screen, '三秒后将重新开始...', (20, 60))
            elif resultFlag == 2:
                show_text(screen, '黑棋赢', (20, 20))
                show_text(screen, '三秒后将重新开始...', (20, 60))
        pygame.display.update()

        if resultFlag > 0:
            time.sleep(3)
            resultFlag = 0
            initRole = firstRole
        eventHander()

if __name__ == '__main__':
    main()
