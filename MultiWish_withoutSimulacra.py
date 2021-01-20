from numpy import *


def one_wish(list_before_with_zeros):
    list_before = trim_zeros(list_before_with_zeros)
    # noinspection PyUnusedLocal
    list_plus1 = [0 for i in range(len(list_before) + 1)]
    n_plus = len(list_before) + 1
    for i in range(n_plus):		# also von 0 bis n
        if i == 0:  # first element (zero fails), p- from one fail
            list_plus1[i] = list_before[i + 1] * a
        elif i == 1 and i+1 < n_plus-1:  # second element, one fail, no p+ from zero fails
            list_plus1[i] = list_before[i + 1] * a + list_before[i] * e
        elif i == (n_plus - 2) and i-1 > 0:  # second-to-last element, no p- from n fails
            list_plus1[i] = list_before[i] * e + list_before[i - 1] * d
        elif i == n_plus-1:  # last element, p- from n fails
            list_plus1[i] = list_before[i - 1] * d
        else:  # middle elements, p+ from (n-1) fails, p0 from n fails, p- from (n+1) fails
            list_plus1[i] = list_before[i + 1] * a + list_before[i] * e + list_before[i - 1] * d
    return list_plus1  # list_plus


def pp2(x1):  # percentage, precise to 2 numbers after the separator
    if x1 < 0.001:
        return str(round(x1 * 10 ** (- floor(log10(x1))), 2)) + 'e' + str(floor(log10(x1)) + 2) + ' %'
    else:
        return str(round(x1 * 100, 2)) + ' %'


print("In this calculation it is assumed that Simulacrums are not allowed. ")
print("It is also assumed that one of the events that can be redone with a Wish is the loss of the ability to ever \
again cast Wish due to Wish-related stress, but that the Wish which caused the stress isn't undone itself. ")
print("Mechanically this means that a second Wish-caster can give somebody else advantage on their re-roll on whether \
or not they will lose the ability to cast Wish ever again, if necessary, that a third caster can give a second \
caster advantage on their re-roll, if necessary, and so on. ")
print("Furthermore it's assumed that all casters help each other perfectly, which means one Wish per day for the best \
chance of everybody continuing to be able to cast Wish again. ")
rep = True

while rep:

    x, y, n, w = 1, 3, 4, 14  # standard values

    print("Standard probability for never being able to cast Wish again if the caster suffered Wish-related stress is \
1 in 3, standard assumption for number of casters is  4, standard assumption for number of Wishes cast in this way is \
14 (resistance to all damage 13 types + 1 free Wish). Do you wish to change these values?")
    yn = input("y/n: ")
    if yn == 'y':
        print("Please enter the probability for never being able to cast Wish again if the caster suffered \
Wish-related stress as x in y: ")
        x = int(input("x = "))
        y = int(input("y = "))
        print("Please enter the number of casters n who are able to cast Wish by themselves: ")
        n = int(input("n = "))
        print("How many Wishes w would you like to cast?")
        w = int(input("w = "))

    a = (y * y - x * x) * (y - x)  # list0[0]  # (10000-33*33)*67  #(9-1*1)*2
    b = (y * y - x * x) * x  # list0[1]  # (10000-33*33)*33  #(9-1*1)*1
    c = x * x * (y - x)  # list0[2]  # 33*33*67  #1*1*2
    d = x ** 3  # list0[3]  # 33*33*33  #1*1*1
    e = b + c

    f = y ** 3  # 100**3  #27

    # create an empty matrix to store the values of the dividend
    z1 = [[0] * (n + 1) for i in range(n)]

    list1 = ([y - x, x])  # ([67, 33])
    list2 = ([a, b + c, d])

    for i1 in range(len(list1)):  # first row: done manually, elements: y-x, x
        z1[0][i1] = list1[i1]

    for i2 in range(len(list2)):  # second row done manually, elements: a, b + c, d
        z1[1][i2] = list2[i2]

    for i0 in range(2, n):
        # here's where the rubber hits the road and the function is called
        list_after1 = trim_zeros(one_wish(z1[i0 - 1]))
        for i3 in range(len(list_after1)):  # len(list_after)
            z1[i0][i3] = list_after1[i3]

    # Calculate chance for zero failures, depending on the number of wizards n
    cz1 = [0 for i in range(n)]
    cf1 = [0 for i in range(n)]
    cz_relative1 = zeros(n)
    cf_relative1 = zeros(n)

    cz1[0] = y - x
    cf1[0] = x
    cz_relative1[0] = cz1[0] / y
    cf_relative1[0] = cf1[0] / y

    print("1 caster has a ", pp2(cf_relative1[0]), " chance of never being able to cast Wish again. For ", w, " Wishes \
this chance becomes ", pp2(1 - cz_relative1[0] ** w), ".", sep="")

    for i4 in range(1,
                    n):  # calculating the actual values for zero failures by a step by step addition, and then division
        cz1[i4] = cz1[i4 - 1] * f + x * z1[i4][0]
        cf1[i4] = y ** (3 * i4 + 1) - cz1[i4]
        cz_relative1[i4] = cz1[i4] / (y ** (3 * i4 + 1))
        cf_relative1[i4] = cf1[i4] / (y ** (3 * i4 + 1))

    for i5 in range(1, n):
        cf1_w = (1 - cz_relative1[i5] ** w) * 100
        if cf1_w > 10 ** - 11:
            print(i5 + 1, " casters have a ", pp2(cf_relative1[i5]), " chance of at least one caster never being able \
to cast Wish again. For ", w, " Wishes this chance becomes ", pp2(1 - cz_relative1[i5] ** w), ".", sep="")
        else:
            print(i5 + 1, " casters have a ", pp2(cf_relative1[i5]), "% chance of at least one caster never being able \
to cast Wish again. For ", w, " Wishes this chance becomes ", pp2(w * cf_relative1[i5]), ".", sep="")

    rep0 = input("Repeat? (y/n) ")
    if rep0 == "y":
        rep = True
    else:
        rep = False
