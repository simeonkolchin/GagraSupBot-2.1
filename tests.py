list_d = {}
p = int(input())
for nambrs in range(p):
    stroka = input().split(': ')
    if stroka[0] not in list_d:
        list_d[stroka[0]] = (stroka[1], stroka[2])
    else:
        if int(list_d[stroka[0]][1]) < int(stroka[2]):
            list_d[stroka[0]] = (stroka[1], stroka[2])
for name_1, name_2 in list_d.items():
    print(f'{name_1} - {name_2[0]}')