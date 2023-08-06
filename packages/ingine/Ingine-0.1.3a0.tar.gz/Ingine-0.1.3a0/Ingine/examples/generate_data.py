import seabattle_engine as sb
import random as rnd

# инициализация поля
GameField = sb.SBGameField()

for k in range(10000):
    GameField.clean()

    # инициализация кораблей
    for i in range(1, 5):
        for j in reversed(range(5 - i)):
            ship = sb.SBGameShip(length = i, field = GameField)
            ship.randompos()

    for i in range(rnd.randint(1, 130)):
        GameField.ai_hit()

    file = open('data.py', 'a')
    file.write(GameField.op_oneline()+';'+GameField.oneline()+'\n')
    print(k, '%')
    file.close()
