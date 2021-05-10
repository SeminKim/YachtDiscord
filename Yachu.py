import random
import discord


class Yachu():

    def __init__(self):
        self.score = [0] * 15
        self.dice = [0] * 5
        self.locked = [False] * 5
        self.phase = 0
        self.isAlive = [True] * 12
        self.turn = 0
        print("새 야추게임 생성")
        return

    def lock(self, num):
        if not 0<num<6: raise ValueError
        self.locked[num - 1] = True

    def unlock(self, num):
        if not 0<num<6: raise ValueError
        self.locked[num - 1] = False

    def lockAll(self):
        self.locked = [True] * 5

    def unlockAll(self):
        self.locked = [False] * 5

    def isAllLocked(self):
        return self.locked == [True] * 5

    def __setDice__(self, s):
        self.dice = s

    def rollDice(self):
        assert self.phase < 3

        self.phase += 1
        for i in range(5):
            if not self.locked[i]:
                self.dice[i] = random.randint(1, 6)
        return str(self.dice)

    def getScoreBoard(self):
        def valueFiller(ind):
            if self.isAlive[ind - 1]:
                return '0*'
            else:
                if ind < 7:
                    return str(self.score[ind - 1])
                else:
                    return str(self.score[ind + 1])

        embed = discord.Embed(title=f"점수판    ({self.turn}/12)", color=0xff0000)
        embed.add_field(name="1. Aces", value=valueFiller(1), inline=True)
        embed.add_field(name="2. Deuces", value=valueFiller(2), inline=True)
        embed.add_field(name="3. Threes", value=valueFiller(3), inline=True)
        embed.add_field(name="4. Fours", value=valueFiller(4), inline=True)
        embed.add_field(name="5. Fives", value=valueFiller(5), inline=True)
        embed.add_field(name="6. Sixes", value=valueFiller(6), inline=True)
        embed.add_field(
            name=f'---------------------------------------\nSubtotal: {self.score[6]}              Bonus: {self.score[7]}',
            value="(63점 이상이면 보너스 35점)", inline=False)
        embed.add_field(name="---------------------------------------", value="특수족보", inline=False)
        embed.add_field(name="A. Choices", value=valueFiller(7), inline=True)
        embed.add_field(name="B. Four Cards", value=valueFiller(8), inline=True)
        embed.add_field(name="C. Full House", value=valueFiller(9), inline=True)
        embed.add_field(name="D. S. Straight", value=valueFiller(10), inline=True)
        embed.add_field(name="E. L. Straight", value=valueFiller(11), inline=True)
        embed.add_field(name="F. Yacht", value=valueFiller(12), inline=True)
        embed.add_field(name="---------------------------------------\nTotal", value=str(self.score[14]), inline=True)
        return embed

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
        if ind < 6:
            temp = 0
            for i in self.dice:
                if i == ind+1 : temp += i
            self.score[ind] = temp
            self.score[6] = self.subtotal()
            self.score[7] = self.checkBonus()


        elif ind == 6:
            self.score[8] = self.diceSum()

        elif ind == 7:
            if self.isFourCards():
                self.score[9] = self.diceSum()
            else:
                self.score[9] = 0

        elif ind == 8:
            if self.isFullHouse():
                self.score[10] = self.diceSum()
            else:
                self.score[10] = 0

        elif ind == 9:
            if self.isSmallStraight():
                self.score[11] = 15
            else:
                self.score[11] = 0

        elif ind == 10:
            if self.isLargeStraight():
                self.score[12] = 30
            else:
                self.score[12] = 0

        elif ind == 11:
            if self.dice[0] == self.dice[1] == self.dice[2] == self.dice[3] == self.dice[4]:
                self.score[13] = 50
            else:
                self.score[13] = 0

        else:
            return

        self.score[14] = sum(self.score[6:14])
        self.phase = 0
        self.locked = [False] * 5
        self.isAlive[ind] = False
        self.turn += 1

    def isAvailable(self, ind):
        try:
            if not 0 <= ind <= 11: return False
            return self.isAlive[ind]
        except:
            return False


# demo for console
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
