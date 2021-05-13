from Yachu import Yachu
from prettytable import PrettyTable

Indices = ["1.Aces", "2.Deuces", "3.Threes", "4.Fours", "5.Fives", "6.Sixes", "Subtotal", "Bonus", "7.Choices",
           "8.Four Cards",
           "9.Full House", "10.S.Straight", "11.L.Straight", "12.Yachu", "Total"]


class MultiYachu():
    def __init__(self):
        self.player_one = Yachu()
        self.player_two = Yachu()
        return

    def getScoreBoard(self):
        x = PrettyTable(["", f'{self.name1} ({self.yachu1.turn}/12)', f'{self.name2} ({self.yachu2.turn}/12)'])
        x._set_horizontal_char("─")
        x._set_vertical_char("│")
        x._set_junction_char("·")
        x.align = "l"
        for i in range(15):
            if i < 6:
                score1 = self.yachu1.score[i]
                score2 = self.yachu2.score[i]
                if self.yachu1.isAlive[i]: score1 = "0*"
                if self.yachu2.isAlive[i]: score2 = "0*"
                x.add_row([Indices[i], score1, score2])

            if i == 6 or i == 7: x.add_row(["-> " + Indices[i], self.yachu1.score[i], self.yachu2.score[i]])

            if 7 < i < 14:
                score1 = self.yachu1.score[i]
                score2 = self.yachu2.score[i]
                if self.yachu1.isAlive[i - 2]: score1 = "0*"
                if self.yachu2.isAlive[i - 2]: score2 = "0*"
                x.add_row([Indices[i], score1, score2])

            if i == 14: x.add_row(["-> " + Indices[i], self.yachu1.score[i], self.yachu2.score[i]])

        return "```\n" + str(x) + "\n```"

    def getFinalScore(self):
        assert self.player_one.getTurn() == self.player_two.getTurn() == 12
        return (self.player_one.getTotal(), self.player_two.getTotal())
