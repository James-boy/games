# -*- coding:utf-8 -*- 

import pygame
import sys
import time
from pygame.locals import *

class StornPoint():
    def __init__(self, x, y, value, number):
        self.x = x
        self.y = y
        self.value = value
        self.number = number

firstRole = 1
initChesslist = []
initRole = firstRole
resultFlag = 0
k = 0

class Five_Chess():
    def initChessSquare(self, x, y):
        for i in range(15):
            rowlist = []
            for j in range(15):
                pointx = x + j * 41
                pointy = y + i * 41
                sp = StornPoint(pointx, pointy, 0, 0)  # 各格点都属于这个类但是互不影响
                rowlist.append(sp)
            initChesslist.append(rowlist)

    def eventHander(self):
        global initChesslist, initRole, resultFlag, k
        for event in pygame.event.get():
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
                        if x >= point.x - 10 and x <= point.x + 10 and y >= point.y - 10 and y <= point.y + 10:
                            if point.value == 0 and initRole == 1:
                                point.value = 1
                                point.number = k + 1
                                k += 1
                                self.judgeResult(i, j, 1)
                                initRole = 2
                            if point.value == 0 and initRole == 2:
                                point.value = 2
                                point.number = k + 1
                                k += 1
                                self.judgeResult(i, j, 2)
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
                    self.initChessSquare(26, 26)
                    k = 0
                    initRole = firstRole  # 用于保证重新开始后白子先，若要每次黑子先则改为2就行
                # 点击退出时执行如下代码
                if x >= 656 and x <= 716 and y >= 500 and y <= 530:
                    pygame.quit()
                    sys.exit()

    def judgeResult(slef, i, j, value):
        global initChesslist, resultFlag
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

    def show_text(self, screen, txt, place_):
        s_font = pygame.font.Font('字体文件/正楷字体.TTF', 30)
        s_text = s_font.render(txt, True, (0, 0, 0))
        screen.blit(s_text, place_)

    def main(self):
        global initChesslist, resultFlag, initRole, k
        self.initChessSquare(26, 26)
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
        # whiteStorn.get_rect()
        # blackStorn.get_rect()

        while True:
            screen.blit(rightground, (0, 0))
            screen.blit(leftground, (626, 0))
            self.show_text(screen, '悔棋', (656, 300))
            self.show_text(screen, '重新开始', (656, 400))
            self.show_text(screen, '退出', (656, 500))
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
                if point.value == 1:
                    screen.blit(blackStorn, (708, 100))
                    break
                elif point.value == 2:
                    screen.blit(whiteStorn, (708, 100))
                    break
            # 如若赢棋执行以下代码
            if resultFlag > 0:
                initChesslist = []
                self.initChessSquare(26, 26)
                k = 0
                if resultFlag == 1:
                    self.show_text(screen, '白棋赢', (20, 20))
                    self.show_text(screen, '三秒后将重新开始...', (20, 60))
                elif resultFlag == 2:
                    self.show_text(screen, '黑棋赢', (20, 20))
                    self.show_text(screen, '三秒后将重新开始...', (20, 60))
                pygame.display.update()
                time.sleep(3)
                resultFlag = 0
                initRole = firstRole
            pygame.display.update()

            self.eventHander()

if __name__ == '__main__':
    Five_Chess().main()
