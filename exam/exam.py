# 'hello, {name}!'と出力してください 。
import math
def hello(name):
    print('hello, ' + name + '!')

# sentence の文字数を出力してください
def length(sentence):
    print(len(sentence))


# sentence の2文字目から5文字目まで(5文字目は含まない)を出力してください
def slicing2to5(sentence):
    i = sentence
    print(i[2:5])

# number の符号を出力してください。ただし、0は'0'と出力してください
def number_sign(number):
    n = number
    if n == 0:
        print('0')
    elif n > 0:
        print('+')
    else:
        print('-')


# number が素数なら'ok',そうでないなら'ng'と出力してください
def prime_number(number):
    if number > 3 and (number % 2 == 0 or number % 3 == 0 or number == 1):
        print('ng')
    else:
        print('ok')
# 1からnumberまでの合計を出力してください
def sum_from_1_to(number):
    count = 0
    for i in range(1, number + 1):
        count += i
    print(count)


# numberの階乗(factorial)を出力してください
def factorial(number):
    count2 = 1
    for i in range(1, number + 1):
        count2 *= i
    print(count2)

# リストdataの各要素(整数)を3乗した結果をリスト型として返してください
def cubic_list(data):
    list=[]
    for i in (data):
        list.append(i ** 3)
    return list
# 底辺x,高さyの直角三角形(right angled triangle)の残り1つの辺の長さを返してください
def calc_hypotenuse(x, y):
    v = (x**2) + (y**2)
    return math.sqrt(v)




 # 底辺x,斜辺vの直角三角形の残り1つの辺の長さを返してください
def calc_subtense(x, v):
    return math.sqrt((v**2) - (x**2))

# 三辺の長さがそれぞれx,y,zの三角形の面積を返してください
def calc_area_triangle(x, y, z):
    s = ((x+y+z)/2)
    v = (s-x) * (s-y) * (s-z)
    return math.sqrt(s*v)

# 引数a,b,cを小数点以下2桁表示で空白切りで表示してください
def point_two_digits(a, b, c):
    print('{:.2f} {:.2f} {:.2f}'.format(a, b, c))



# リストdataの内容を小さい順でソートした結果を返してください
def list_sort(data):
    data.sort()
    return data

# 文字列の並びを逆にしたものを返してください
def reverse_string(sentence):
    you = sentence[::-1]
    return you

# dateから2016年4月1日までの日数を返してください
def days_from_date(point):
    from datetime import date
    birthday = date(2016, 4, 1)
    popo = point
    life = birthday - popo
    return life.days
