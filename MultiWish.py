from numpy import *
from scipy.special import comb
from copy import deepcopy


def m_wishes(m, j):  # Entry for the last column of a conditional-probability-matrix with m open wishes and m+2 fails, 
    # all open wishes used
    w_two = (e1 * (a ** j * b ** (m - j) * c * comb(m, j, True) +
                   a ** (j + 1) * b ** (m - j - 1) * d * comb(m, j + 1, True) +
                   a ** j * b ** (m - j + 1) * comb(m + 1, j, True)) +
             a * (a ** (j-1) * b ** (m - j + 2) * comb(m + 1, j - 1, True) +
                  a ** (j-1) * b ** (m - j + 1) * c * (m + 1) * comb(m, j - 1, True) +
                  a ** j * b ** (m - j) * d * (m + 1) * comb(m, j, True) +
                  a ** (j - 1) * b ** (m - j) * c ** 2 * m * comb(m - 1, j - 1, True) +
                  a ** j * b ** (m - j - 1) * c * d * 2 * m * comb(m - 1, j, True) +
                  a ** (j+1) * b ** (m - j - 2) * d ** 2 * m * comb(m - 1, j + 1, True)))
    return w_two


def wish_stop(m, j):
    # Entry for the second to second-to-last column of a conditional-probability-matrix with m open wishes and m+2 fails,
    # "stopped" wish-chains, stopped because of failures, so not all open wishes used
    # if j > 0:
    w_stop = (e1 * (a ** j * b ** (m - j) * c * comb(m, j, True) +
                    a ** (j + 1) * b ** (m - j - 1) * d * comb(m, j + 1, True)) +
              a * (a ** (j - 1) * b ** (m - j) * c ** 2 * m * comb(m - 1, j - 1, True) +
                   a ** j * b ** (m - j - 1) * c * d * 2 * m * comb(m - 1, j, True) +
                   a ** (j + 1) * b ** (m - j - 2) * d ** 2 * m * comb(m - 1, j + 1, True)))
    # else:
    #    w_stop = (e1 * (a ** j * b ** (m - j) * c * int(comb(m, j, True)) +
    #                    a ** (j + 1) * b ** (m - j - 1) * d * int(comb(m, j + 1, True))) +
    #              a * (a ** (j - 1) * b ** (m - j) * c ** 2 * m * int(comb(m - 1, j - 1, True)) +
    #                   a ** j * b ** (m - j - 1) * c * d * 2 * m * int(comb(m - 1, j, True)) +
    #                   a ** (j + 1) * b ** (m - j - 2) * d ** 2 * m * int(comb(m - 1, j + 1, True))))
    return w_stop


def pp2(x1):  # percentage, rounded to 2 numbers after the separator
    if x1 < 0.001:
        return str(round(x1 * 10 ** (- floor(log10(x1))), 2)) + 'e' + str(floor(log10(x1)) + 2) + ' %'
    else:
        return str(round(x1 * 100, 2)) + ' %'


def two_wishes(z_old, x2, y2, z):
    # application of the conditional probabilities on the probabilities of the previous step
    for i in range(z + 1):
        z_old[0][i] = 0
    z_new = 0

    for i in range(z + 1):
        for j in range(z + 1):
            if i == j:
                z_new = z_new + z_old[i][j] * cond_prob0[j][i - x2 + 1][j - y2 + 1]
            elif i - 1 == j:
                z_new = z_new + z_old[i][j] * cond_prob1[j][i - x2 + 1][j - y2 + 1]
            else:
                z_new = z_new + z_old[i][j] * cond_prob2[j][i - x2 + 1][j - y2 + 1]
    return z_new


def check_sum(z):  # to check if the sum of all probabilities is 0
    c_s = deepcopy(cz[z]) / y ** (6 * z + 4)
    for j in range(z + 2):
        divisor = y ** (6 * z + 4 - 3 * j)
        for i in range(1, z + 2):
            c_s = c_s + probabilities_dividend[z][i][j] / divisor
    return c_s


print("In this calculation it is assumed that every caster able to cast Wish has a Simulacrum of himself (or another \
caster able to cast Wish) which can also cast Wish. If a Simulacrum suffers the stress of wishing and is unable to \
ever cast Wish again, it's assumed that the caster who cast this Simulacrum into existence is also unable to ever cast \
Wish again, otherwise this whole calculation is unnecessary^^ ")
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
Wish-related stress as x in y (recommended values are x = 1 and y = 3): ")
        x = int(input("x = "))
        y = int(input("y = "))
        print("Please enter the number of casters n who are able to cast Wish by themselves (values <= 50 are \
recommended, unless your computer is fast and has a big RAM - program not optimized for RAM space): ")
        n = int(input("n = "))
        print("How many Wishes w would you like to cast?")
        w = int(input("w = "))

    a = (y * y - x * x) * (y - x)  # (10000-33*33)*67  #(9-1*1)*2
    b = (y * y - x * x) * x  # (10000-33*33)*33  #(9-1*1)*1
    c = x * x * (y - x)  # 33*33*67  #1*1*2
    d = x ** 3  # 33*33*33  #1*1*1
    e1 = b + c  # 367026    # 10
    f = y ** 3  # 100**3  #27

    # n matrices for n casters, of the exact dividends of the probabilities for a certain result with m casters,
    # (0 to m) "open" (= unused) wishes and (0 to m) "fails" (= number of casters unable to ever cast Wish again),
    # open Wishes are counted in the column number, fails in the row number;
    # for example, after the first caster cast their Wish, there is one open Wish (their Simulacrum),
    # and either 0 (2/3 chance) or 1 (1/3 chance) fail(s)
    probabilities_dividend = [[[0 for i1 in range(n + 1)] for j1 in range(n + 1)] for k1 in range(n)]

    # matrix of conditional probabilities where the column-number denotes how much the number of "open" Wishes
    # changes after the next caster is through, from +1 to -(all the open Wishes)
    # and where the row-number denotes how the number of "fails" changes after the next caster is through,
    # from + 1 to -(number of open Wishes + 2)
    # AND for all higher numbers of fails;
    # (if the casters cast ideally, the number of fails has to be higher than the number of open wishes)
    # for example, after the first caster cast their Wish, there is one conditional-probability-matrix for the condition
    # of 1 fail and 1 open Wish, and this matrix describes how the probabilities shift for two casters, meaning:
    # the number of open Wishes could shift -1 down to 0 (if the first caster regains their  ability to cast, has to use
    # both their Wishes, and the second caster has to use both their Wishes, too), could shift 0 and stay a 1 open Wish
    # (if either the first or the second caster have to use both their Wishes), or could shift +1 up to 2 (if the second
    # caster gives the first caster back their ability to cast Wish with their first Wish);
    # the number of "fails" could shift -1 down to 0, could stay at 1 (if the second caster gives the first 2 rerolls
    # with advantage and both fail, or if the second caster loses his ability to cast Wish again ("fails"), but enables
    # the first caster to cast Wish again, and the same happens again to the first caster and then again to the second
    # caster, or some other variations), or +1 up to 2 (if the second caster suffers stress on his first Wish and the
    # reroll for the first caster is bad, too (1/27 chance on top of the original 1/3 chance));
    # this example is for a different conditional-probability matrix (cond-prob0[1], actually), since the conditional-
    # probability-matrix for 1 open wishes and 3 fails (cond_prob2[1]) doesn't come up until there were 3 casters
    cond_prob2 = [[[0 for i0 in range(n + 2)] for j0 in range(n + 4)] for k0 in range(n + 1)]

    # first probability matrix input manually
    probabilities_dividend[0][0][1] = y - x
    probabilities_dividend[0][1][1] = x

    # first conditional probabilities are input manually, because I don't think the formula works...
    cond_prob2[0][0][0] = d
    cond_prob2[0][0][1] = c * d
    cond_prob2[0][1][0] = b
    cond_prob2[0][1][1] = a * d + c * b + c * c
    cond_prob2[0][2][1] = a * c + a * b + c * a
    cond_prob2[0][3][1] = a ** 2

    for i0 in range(1, n + 1):  # till the layer dimension i0 = n calculate the matrix entries for each matrix
        cond_prob2[i0][0][0] = d
        cond_prob2[i0][0][1] = e1 * d
        cond_prob2[i0][1][1] = e1 * c
        for i1 in range(2, i0 + 1):  # the rows are shifted one to the left, n = i1 - 1
            for i2 in range(i1 + 1):  # the columns are shifted one "upward", j = i2 - 1
                cond_prob2[i0][i2][i1] = int(wish_stop(i1 - 1, i2 - 1))  # if not all open wishes are used

        for i3 in range(0, i0 + 4):
            cond_prob2[i0][i3][i0 + 1] = int(m_wishes(i0, i3 - 1))  # if all open wishes are used

    # matrix of conditional probabilities with (number of rows) "open" wishes n and (number of columns) "fails" n+1
    cond_prob1 = deepcopy(cond_prob2)

    # modify cond_prob2, because of stops of "early" successes,
    # where not all open wishes were needed to undo all the fails
    for i0 in range(n + 1):
        cond_prob1[i0][i0 + 3][i0 + 1] = 0
        cond_prob1[i0][i0 + 2][i0 + 1] = cond_prob1[i0][i0 + 2][i0 + 1] - a ** (i0 + 1) * e1
        cond_prob1[i0][i0 + 1][i0 + 1] = cond_prob1[i0][i0 + 1][i0 + 1] - a ** (i0 + 1) * d
        cond_prob1[i0][i0 + 2][i0] = a ** (i0 + 1)

    # matrix of conditional probabilities with (number of rows) "open" wishes n and (number of columns) "fails" n
    cond_prob0 = deepcopy(cond_prob1)
    # modify cond_prob2, because of stops of "early" successes,
    # where not all open wishes were needed to undo all the fails
    cond_prob0[0][1][0] = y - x
    cond_prob0[0][2][0] = 0
    cond_prob0[0][0][1] = 0
    cond_prob0[0][1][1] = 0
    cond_prob0[0][2][1] = 0

    for i0 in range(1, n + 1):
        cond_prob0[i0][i0 + 2][i0 + 1] = 0  # cutting away the last row
        cond_prob0[i0][i0 + 2][i0] = 0  # cutting away the last row

        cond_prob0[i0][i0 + 1][i0] = a ** i0 * e1 * i0  # 0 fails, n-1 open wishes used
        cond_prob0[i0][i0 + 1][i0 - 1] = a ** i0  # 0 fails, n-2 open wishes used

        # all open wishes used
        cond_prob0[i0][i0 - 1][i0 + 1] = cond_prob0[i0][i0 - 1][i0 + 1] - a ** i0 * d * d
        cond_prob0[i0][i0][i0 + 1] = cond_prob0[i0][i0][i0 + 1] - a ** i0 * e1 * i0 * d - a ** i0 * e1 * d * 2
        cond_prob0[i0][i0 + 1][i0 + 1] = (cond_prob0[i0][i0 + 1][i0 + 1] - a ** i0 * e1 * i0 * e1
                                          - a ** i0 * (b * b + c * c + a * d + b * c * 2))

    for i0 in range(1, n):  # here's where the rubber hits the road and the probability dividends are calculated
        # the calculation happens incrementally, step by step that is, the 'seed' was input manually
        for i1 in range(i0 + 2):
            for i2 in range(i0 + 2):
                probabilities_dividend[i0][i1][i2] = two_wishes(deepcopy(probabilities_dividend[i0 - 1]), i1, i2, i0)

    cz = [0 for i in range(n)]  # dividends of the probabilities for zero fails for n casters
    cz_relative = zeros(n)  # chances for zero fails for n casters
    cf = [0 for i in range(n)]  # dividends of the probabilities for at least one fail for n casters
    cf_relative = zeros(n)  # chances for at least one fail for n casters

    cz[0] = (y - x) * f
    cf[0] = x * f
    cz_relative[0] = cz[0] / (y * f)
    cf_relative[0] = cf[0] / (y * f)

    print("1 caster has a ", pp2(cf_relative[0]), " chance of never being able to cast Wish again after suffering \
Wish-related stress. For ", w, " stressful Wishes this chance becomes ", pp2(1 - cz_relative[0] ** w), ".", sep="")

    for i0 in range(1, n):  # calculate the dividends of the chance for zero fails
        cz[i0] = cz[i0 - 1] * f ** 2
        for i1 in range(3):
            cz[i0] = cz[i0] + probabilities_dividend[i0][0][i1] * f ** i1

        cf[i0] = y ** (i0 * 6 + 4) - cz[i0]  # calculate the dividends of the chance for at least one fail
        cz_relative[i0] = cz[i0] / (y ** (i0 * 6 + 4))
        cf_relative[i0] = cf[i0] / (y ** (i0 * 6 + 4))

    for i5 in range(1, n):
        cf1_w = (1 - cz_relative[i5] ** w) * 100  # percent chance for at least one fail after wishing w times
        if cf1_w > 10 ** - 11:  # exactly
            print(i5 + 1, " casters have a ", pp2(cf_relative[i5]), " chance of at least one caster never being able \
to cast Wish again if the first caster Wishes for something that causes Wish-related stress. For ", w, " stressful \
Wishes the cumulative chance for this becomes ", pp2((1 - cz_relative[i5] ** w)), ".", sep="")
        else:  # approximately, but without the values becoming zero
            print(i5 + 1, " casters have a ", pp2(cf_relative[i5]), " chance of at least one caster never being able \
to cast Wish again if the first caster Wishes for something that causes Wish-related stress. For ", w, " stressful \
Wishes the cumulative chance for this becomes ", pp2(w * cf_relative[i5]), ".", sep="")

    rep0 = input("Repeat? (y/n) ")
    if rep0 == "y":
        rep = True
    else:
        rep = False
