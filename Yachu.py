import random


class Yachu():
    score = [0] * 15
    dice = [0] * 5
    locked = [False] * 5
    phase = 0
    isAlive = [True] * 12
    turn = 0

    def __init__(self):
        print("새 야추게임 생성")
        return

    def lock(self, num):
        self.locked[num - 1] = True

    def unlockAll(self):
        self.locked = [False] * 5

    def __setDice__(self, s):
        self.dice = s

    def rollDice(self):
        if self.phase == 3:
            return '기회 끝'
        else:
            self.phase += 1
            for i in range(5):
                if not self.locked[i]:
                    self.dice[i] = random.randint(1, 6)
            return str(self.dice) + '\n{}번 다시 굴릴 수 있습니다'.format(3 - self.phase)

    def getScoreBoard(self):
        return "<현재 턴:{}/12>\n".format(self.turn) + "----점수표----\n1.Aces:{}\n2.Deuces:{}\n3.Threes:{}\n4.Fours:{}\n5.Fives:{}\n6.Sixes:{}\n-------------\nSubtotal:{}\nBonus:{}" \
               "\n(63점 이상이면 보너스)\n-------------\n7.Choice:{}\n8.Four Cards:{}\n9.Full House:{}\n10.S.Straight:{}\n11.L.Straight:{}\n12.Yacht:{}\n-------------\nTotal:{}\n".format(
            *self.score)

    def subtotal(self):
        return sum(self.score[:6])

    def checkBonus(self):
        if self.subtotal() >= 63:
            return 35
        return 0

    def diceSum(self):
        temp = 0
        for die in self.dice:
            temp += die
        return temp

    def isFourCards(self):
        tempDice = self.dice[:]
        tempDice.sort()
        return tempDice[0] == tempDice[1] == tempDice[2] == tempDice[3] or tempDice[1] == tempDice[2] == tempDice[3] == \
               tempDice[4]

    def isFullHouse(self):
        tempDice = self.dice[:]
        tempDice.sort()
        return (tempDice[0] == tempDice[1] == tempDice[2] and tempDice[3] == tempDice[4]) \
               or (tempDice[0] == tempDice[1] and tempDice[2] == tempDice[3] == tempDice[4])

    def isSmallStraight(self):
        numcount = [0] * 6
        for i in range(6):
            if i + 1 in self.dice: numcount[i] = 1
        if numcount[0] * numcount[1] * numcount[2] * numcount[3] == 1: return True
        if numcount[1] * numcount[2] * numcount[3] * numcount[4] == 1: return True
        if numcount[2] * numcount[3] * numcount[4] * numcount[5] == 1: return True
        return False

    def isLargeStraight(self):
        tempDice = self.dice[:]
        tempDice.sort()
        if tempDice == [1, 2, 3, 4, 5] or tempDice == [2, 3, 4, 5, 6]: return True
        return False

    def setScore(self, ind):
        if 0 < ind < 7:
            temp = 0
            for i in self.dice:
                if i == ind: temp += ind
            self.score[ind - 1] = temp
            self.score[6] = self.subtotal()
            self.score[7] = self.checkBonus()


        elif ind == 7:
            self.score[8] = self.diceSum()

        elif ind == 8:
            if self.isFourCards():
                self.score[9] = self.diceSum()
            else:
                self.score[9] = 0

        elif ind == 9:
            if self.isFullHouse():
                self.score[10] = self.diceSum()
            else:
                self.score[10] = 0

        elif ind == 10:
            if self.isSmallStraight():
                self.score[11] = 15
            else:
                self.score[11] = 0

        elif ind == 11:
            if self.isLargeStraight():
                self.score[12] = 30
            else:
                self.score[12] = 0

        elif ind == 12:
            if self.dice[0] == self.dice[1] == self.dice[2] == self.dice[3] == self.dice[4]:
                self.score[13] = 50
            else:
                self.score[13] = 0

        else:
            return

        self.score[14] = sum(self.score[6:14])
        self.phase = 0
        self.locked = [False] * 5
        self.isAlive[ind - 1] = False
        self.turn +=1

    def isAvailable(self,ind):
        try: return self.isAlive[ind-1]
        except: return False

#demo for console
'''
def main():
    yachu = Yachu()
    for i in range(12):
        while yachu.phase < 3:
            print(yachu.getScoreBoard())
            print(yachu.rollDice())

            if yachu.phase == 3:
                ind = int(input('저장할 칸 선택 : '))
            else:
                ind = int(input('저장할 칸 선택, 0은 다시굴림 : '))

            if ind == 0:
                for i in range(5): yachu.unlockAll()
                temp = input('고정할 주사위 선택 - ex) 1 2 4 : ').split()
                for i in temp: yachu.lock(int(i))

            else:
                yachu.setScore(ind)
                break


main()
'''
