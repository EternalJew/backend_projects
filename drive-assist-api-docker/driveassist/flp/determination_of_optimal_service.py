# Алгоритм який має в собі дані про сервіси 
# і на основі отриманих поломок сам сповістить 
# сервіс який розташований найближче і 
# найоптимальніше що потрібна допомога

from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpBinary
import math

# Функція для розрахунку евклідової відстані між двома точками
def calculate_distance(loc1, loc2):
    return math.sqrt((loc1[0] - loc2[0]) ** 2 + (loc1[1] - loc2[1]) ** 2)

# Геолокації технічних служб (місто Рівне, умовні координати)
facilities = {
    0: (50.6199, 26.2516),  # Центр
    1: (50.6214, 26.2448),  # Північ
    2: (50.6193, 26.2683),  # Схід
    3: (50.6050, 26.2399),  # Захід
    4: (50.6100, 26.2600)   # Південь
}

# Геолокації точок поломок (умовні координати для Рівного)
demands = {
    i: (50.61 + (i * 0.001), 26.25 + (i * 0.002)) for i in range(25)
}

# Вартість розміщення сервісу в кожній точці
facility_costs = {
    0: 1000,  # Центр
    1: 900,   # Північ
    2: 1100,  # Схід
    3: 950,   # Захід
    4: 1050   # Південь
}

# Розрахунок матриці відстаней між сервісами і місцями поломок
distance_matrix = [
    [calculate_distance(facilities[i], demands[j]) for j in demands] for i in facilities
]

# Ініціалізація проблеми
problem = LpProblem("Facility_Location", LpMinimize)

# Змінні
x = LpVariable.dicts("Facility", facilities.keys(), cat=LpBinary)
y = LpVariable.dicts("Assignment", [(i, j) for i in facilities for j in demands], cat=LpBinary)

# Цільова функція: мінімізуємо вартість розміщення сервісів та витрати на відстань
problem += lpSum(facility_costs[i] * x[i] for i in facilities) + lpSum(distance_matrix[i][j] * y[(i, j)] for i in facilities for j in demands)

# Обмеження: кожна точка поломки має бути обслугована
for j in demands:
    problem += lpSum(y[(i, j)] for i in facilities) == 1

# Обмеження: якщо сервіс не відкрито, він не може обслуговувати точку
for i in facilities:
    for j in demands:
        problem += y[(i, j)] <= x[i]

# Обмеження на кількість відкритих сервісів (5 служб)
problem += lpSum(x[i] for i in facilities) == 5

# Розв'язання
problem.solve()

# Виведення результатів
for i in facilities:
    if x[i].varValue == 1:
        print(f"Сервіс розташовано в точці {i} з координатами {facilities[i]}")

for i in facilities:
    for j in demands:
        if y[(i, j)].varValue == 1:
            print(f"Місце поломки {j} обслуговується сервісом {i}")
