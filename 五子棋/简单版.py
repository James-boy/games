# -*- coding:utf-8 -*-

# 五子棋实现思路：
# 1.设置一个列表用于记录棋盘上所有位置信息（是否有子和黑白子）
# 2.监控鼠标状态，将鼠标落点位置读取，选择关闭界面或者落子。落子的同时将列表上
# 该位置的信息进行改变。并同时判断是否输赢
# 3.主程序，设置画布，然后读取列表，和导入图片（实现落子和背景、结束时的图像不一）。
# 每次更新页面，将列表上数据信息显示为白子或黑子的导入相关图片，同时根据是否结束来改变页面

import pygame
import sys
import time
from pygame.locals import *

# 用于记录棋盘信息，每个位置落子情况
initChesslist = []

# 1 表示是白子，2 表示是黑子
initRole = 1   # 此处 1 表示第一个落白子

# 用于判断是否结束
resultFlag = 0

# 用一个类来描述某棋盘格点的信息，x表示该格点横坐标，y表示该格点纵坐标，
# 0 表示未落子，1 表示落了白子，2 表示落了黑子
class StornPoint():
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value

# 该函数用于得到棋盘初始信息
def initChessSquare(x, y):
    for i in range(15):
        rowlist = []
        for j in range(15):
            pointx = x + j*41   # 上面的15和这里的41也是经过计算的，同样的根据棋盘格点数和每个格子所占像素大小确定
            pointy = y + i*41
            sp = StornPoint(pointx, pointy, 0)  # 各格点都属于这个类但是互不影响
            rowlist.append(sp)
        initChesslist.append(rowlist)

# 此函数用于判断鼠标点击位置，若该位置某范围内存在格点，将格点信息进行更改，便于后续画图
# 同时该函数调用了后一个函数，用于判断是否有五子相连，如果有，则返回某句话，同时返回一个resultFlag值
def eventHander():
    for event in pygame.event.get():
        global initRole
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
                            judgeResult(i, j, 1)
                            initRole = 2
                        if point.value == 0 and initRole == 2:
                            point.value = 2
                            judgeResult(i, j, 2)
                            initRole = 1
                        break
                    j += 1
                i += 1
                j = 0

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

def main():
    global initChesslist, resultFlag, initRole
    initChessSquare(26, 26)   # 这个是经过计算的，根据棋盘照片的大小来写的，
                              # 26是棋盘边缘到第一个格点的像素值大小，(15-1)*41是第一个格点到最后一个格点之间的距离
                              # 总棋盘照片大小为26*2+(15-1)*41=626
    pygame.init()
    screen = pygame.display.set_mode((626, 626))  # 这个根据棋盘图像大小确定
    pygame.display.set_caption('小二的五子棋')
    background = pygame.image.load('image/棋盘.jpg')
    resultStorn = pygame.image.load('image/风景图.jpg')
    whiteStorn = pygame.image.load('image/白子.jpg')
    blackStorn = pygame.image.load('image/黑子.jpg')
    #whiteStorn.get_rect()
    #blackStorn.get_rect()

    while True:
        screen.blit(background, (0, 0))
        for temp in initChesslist:
            for point in temp:
                if point.value == 1:
                    screen.blit(whiteStorn, (point.x - 18, point.y - 18))
                elif point.value == 2:
                    screen.blit(blackStorn, (point.x - 18, point.y - 18))

        if resultFlag > 0:
            initChesslist = []
            initChessSquare(26, 26)
            screen.blit(resultStorn, (0, 0))
        pygame.display.update()

        if resultFlag > 0:
            time.sleep(3)
            resultFlag = 0
            initRole = 1  # 保证每次都是白棋先，如若不用，可再更改
        eventHander()

if __name__ == '__main__':
    main()
