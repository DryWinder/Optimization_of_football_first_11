import psycopg2 # бібліотека для роботи з БД PSQL

username = 'postgres' # дані для підключення до Бази Даних
password = 'root1'
database = 'student01_DB'
host = 'localhost'
port = '5432'

conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port) # з'єднання з БД

cur = conn.cursor()

# Допоміжна функція, для обрання найкращих кандидатів на позиції
# Результат роботи функції - Прізвище гравця
def find_best_player(dict, num_of_players):
    # Якщо кількість гравців, яку обрав користувач менша за кіс-ть доступних гравців на цю позицію,
    # то програма повідомить про це
    if(len(dict) < num_of_players):
        player = " У вас недостатньо гравців на цю позицію. Ви маєте обрати інший план на гру або поставити гравця іншого профілю"

# Якщо все гаразд, то обираємо найкращих кандидатів
    else:
        name = list(dict.keys())
        rating = list(dict.values())
        player = ""

        for i in range(num_of_players):
            position = rating.index(max(rating))
            player += name[position]
            rating[position] = 0
    return player



# Goalkeepers
# Основна функція, шо обчислює рейтинги голкіперам
# Результат роботи функції - Виведення рейтингу голкіперів, повертає прізвище воротаря з найвищим рейтингом
def select_goalkeeper():

    cur.execute("SELECT COUNT(*) FROM arsenal WHERE player_positon = 'Goalkeeper'")
    number_of_keepers = cur.fetchone()[0]
    result = {}

    while number_of_keepers != 0:
        cur.execute("""SELECT TRIM(player_name), TRIM(status), starts, clean_sheets, goals_conceded, goals_conceded_per_90, expected_goals_conceded FROM arsenal 
                            WHERE player_positon = 'Goalkeeper'""")

        data = cur.fetchall()[number_of_keepers-1]
        #print(data)
        if(data[2] != 0): #Якщо гравець виходив на поле, тоді проводимо обрахунки
            formula = 6+0.04*(10/data[5] + (data[3]/data[2])*10 + data[6]-data[4])
            player_name = data[0] + " GK "
            result[player_name] = round(formula,2)

        else: #Якщо ж гравець ні разу не зіграв - його рейтинг 0.0
            player_name = data[0]
            result[player_name] = 0.0

        number_of_keepers = number_of_keepers - 1

    rating = list(result.values())
    if(max(rating) < 6.4): #6.4 вважаємо мінімальним показником, якщо немає жодного воротаря з рейтингом > 6.4, тоді тренер має задуматися на придбанням нового голкіпера
        print("Можливо треба спробувати іншого воротаря")

    print("Goalkeepers: ")
    print(result)

    return find_best_player(result, 1)

#print(select_goalkeeper())

# Основна функція, шо обчислює рейтинги захисникам
# Результат роботи функції - Виведення рейтингу захисників, повертає прізвища захисників з найвищим рейтингом
# Кількість захисників залежить від користувача - він їх обирає в останній функції програми
def select_defenders(number_of_CB, number_of_WB):
    cur.execute("SELECT COUNT(*) FROM arsenal WHERE player_positon = 'Defender'")
    number_of_defs_in_table = cur.fetchone()[0]
    result_CB = {}
    result_RB = {}
    result_LB = {}

    while number_of_defs_in_table != 0:
        formula = 0.0
        player = "Empty by now"
        cur.execute("""SELECT TRIM(player_name), TRIM(player_position_speciality_short), TRIM(status), starts, clean_sheets, 
        goals_scored, assists, own_goals, yellow_cards, red_cards, goals_conceded_per_90, expected_goals_conceded, 
        expected_goals_conceded_per_90, minutes FROM arsenal 
                            WHERE player_positon = 'Defender'""")

        data = cur.fetchall()[number_of_defs_in_table - 1]
        #print(data)
        #Блок обрахунку рейтингів
        if (data[3] != 0):
            formula = 6 + 0.05*(25 + (data[4] / data[3]) * 10 + 1.5*data[5] + 1.5*data[6] - data[7]/5 - data[8]/10 - data[9]/5 - data[10]*10 - data[12]*10)
            player = " " + data[0] + " " + data[1]


        if(data[3] == 0 and data[13] != 0):
            formula = 6 + 0.01*(11 + data[4]  * 1 + 1.5*data[5] + 1.5*data[6] - data[7] / 5 - data[8] / 10 - data[9] / 5 - data[10] * 10 - data[12] * 12)
            player = " " + data[0] + " " + data[1]


        if (data[13] == 0 and data[3] == 0):
            player = " " + data[0] + " " + data[1]


        if(data[1] == 'CB' and data[2] == 'a'):
            result_CB[player] = round(formula, 2)

        if (data[1] == 'LB' and data[2] == 'a'):
            result_LB[player] = round(formula, 2)

        if (data[1] == 'RB' and data[2] == 'a'):
            result_RB[player] = round(formula, 2)


        number_of_defs_in_table = number_of_defs_in_table - 1

    print("Defenders: ")
    print(result_CB)
    print(result_LB)
    print(result_RB)

    return find_best_player(result_RB, int(number_of_WB/2)) + find_best_player(result_CB, number_of_CB) + find_best_player(result_LB, int(number_of_WB/2))


#print(select_defenders(2, 2))

#Midfielders
# Основна функція, шо обчислює рейтинги півзахисникам
# Результат роботи функції - Виведення рейтингу півзахисників, повертає прізвища півзахисників з найвищим рейтингом
# Кількість півзахисників залежить від користувача - він їх обирає в останній функції програми
def select_midfielders(number_of_CDM, number_of_CM, number_of_CAM, number_of_WM):
    cur.execute("SELECT COUNT(*) FROM arsenal WHERE player_positon = 'Midfielder'")
    number_of_mids_in_table = cur.fetchone()[0]
    result_CDM = {}
    result_CM = {}
    result_CAM = {}
    result_RM = {}
    result_LM = {}

    while number_of_mids_in_table != 0:
        formula = 0.0
        player = "Empty by now"
        cur.execute("""SELECT TRIM(player_name), TRIM(player_position_speciality_short), TRIM(status), starts, minutes,
        goals_scored, assists, yellow_cards, red_cards, ict_index, xG_per_90, xAs_per_90, expected_goal_involvements_per_90
        FROM arsenal WHERE player_positon = 'Midfielder'""")

        data = cur.fetchall()[number_of_mids_in_table - 1]
        #print(data)
        if (data[3] != 0):
            formula = 6 + 0.04 * (
                        (data[5] / data[4]) * 90 * 10 + (data[6] / data[4]) * 90 * 10 - data[7] / 10 - data[8] / 5 +
                        data[9] / 15 + data[10] * 30 + data[11] * 10 + data[12] * 10)
            player = " " + data[0] + " " + data[1]


        if (data[3] == 0 and data[4] != 0):
            formula = 6 + 0.04 * (
                    (data[5] / data[4]) * 90 * 10 + (data[6] / data[4]) * 90 * 10 - data[7] / 10 - data[8] / 5 +
                    data[9] / 15 + data[10] * 30 + data[11] * 10 + data[12] * 10)

            player = " " + data[0] + " " + data[1]

        if (data[3] == 0 and data[4] == 0):
            player = " " + data[0] + " " + data[1]

        if (data[1] == 'CDM' and data[2] == 'a'):
            result_CDM[player] = round(formula, 2)

        if (data[1] == 'CM' and data[2] == 'a'):
            result_CM[player] = round(formula, 2)

        if (data[1] == 'RM' and data[2] == 'a'):
            result_RM[player] = round(formula, 2)

        if (data[1] == 'LM' and data[2] == 'a'):
            result_LM[player] = round(formula, 2)

        if (data[1] == 'CAM' and data[2] == 'a'):
            result_CAM[player] = round(formula, 2)

        number_of_mids_in_table = number_of_mids_in_table - 1

    print("Midfielders: ")
    print(result_CDM)
    print(result_CM)
    print(result_CAM)
    print(result_RM)
    print(result_LM)

    return find_best_player(result_RM, int(number_of_WM / 2)) + find_best_player(result_CDM, number_of_CDM) \
           + find_best_player(result_CM, number_of_CM) + find_best_player(result_CAM, number_of_CAM)\
           + find_best_player(result_LM, int(number_of_WM / 2))

#print(select_midfielders(2,0,1,2))


#One of main functions. It evaluetes ratings for forwards

# Основна функція, шо обчислює рейтинги нападникам
# Результат роботи функції - Виведення рейтингу нападників, повертає прізвище форварда з найвищим рейтингом
def select_forward():
    cur.execute("SELECT COUNT(*) FROM arsenal WHERE player_positon = 'Forward'")
    number_of_forwards = cur.fetchone()[0]
    result = {}

    while number_of_forwards != 0:
        cur.execute("""SELECT TRIM(player_name), TRIM(player_position_speciality_short), TRIM(status), starts, minutes,
               goals_scored, assists, yellow_cards, red_cards, ict_index, xG_per_90, xAs_per_90, expected_goal_involvements_per_90
               FROM arsenal WHERE player_positon = 'Forward'""")

        data = cur.fetchall()[number_of_forwards-1]
        #print(data)
        if (data[3] != 0):
            formula = 6 + 0.03 * (
                    (data[5] / data[4]) * 90 * 10 + (data[6] / data[4]) * 90 * 10 - data[7] / 5 - data[8] / 10 +
                    data[9] / 15 + data[10] * 30 + data[11] * 10 + data[12] * 10)
            player = " " + data[0] + " " + data[1]

        if (data[3] == 0 and data[4] != 0):
            formula = 6 + 0.03 * (
                    (data[5] / data[4]) * 90 * 10 + (data[6] / data[4]) * 90 * 10 - data[7] / 5 - data[8] / 10 +
                    data[9] / 15 + data[10] * 30 + data[11] * 10 + data[12] * 10)

            player = " " + data[0] + " " + data[1]

        if (data[3] == 0 and data[4] == 0):
            player = " " + data[0] + " " + data[1]

        if(data[2] == 'a'):
            result[player] = round(formula,2)

        number_of_forwards = number_of_forwards - 1

    rating = list(result.values())
    #6.4 - supposing that is minimum grade for forward, so if there is no striker with more than 6.4, than coach must be thinking on signing new attacker
    if(max(rating) < 6.4): #6.4 вважаємо мінімальним показником, якщо немає жодного нападника з рейтингом > 6.4, тоді тренер має задуматися на придбанням нового форварда
        print("Можливо треба спробувати іншого нападника")
        #print("Maybe it's time to try other forward")

    print("Forwards: ")
    print(result)

    return find_best_player(result, 1)

#print(select_forward())

#Функція виводить стартовий склад, залежно від схеми
#Function that prints first eleven, depending on schema
def print_first_eleven():
    CB, WB = 2, 2
    CDM, CM, CAM, WM = 2, 0, 1, 2
    print("Availiable players: ")
    goalkeeper = select_goalkeeper()
    defenders = select_defenders(CB, WB)
    midfielders = select_midfielders(CDM, CM, CAM, WM)
    forward = select_forward()

    num_of_players = CB+WB+CDM+CM+CAM+WM + 2
    # Якщо кількість обраних гравців не дорівнює 11, програма повідомить про це
    if(num_of_players != 11):
        print("")
        print("")
        print("Виберіть правильну кількість гравців. У футбол грають 11 гравців з кожного боку, у Вас же кількість гравців - ", num_of_players)

    else:
        print("\n\nСтартовий склад(схема - {0}-{1}-1)".format(CB+WB, CDM+CM+CAM+WM))
        print("Goalkeeper: ", goalkeeper)
        print("Defenders: ", defenders)
        print("Midfielders:", midfielders)
        print("Forward: ", forward)

print_first_eleven()