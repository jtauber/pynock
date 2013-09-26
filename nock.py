#!/usr/bin/env python3

# []
def l(*lst):
    if len(lst) == 1:
        return(lst[0], 0)
    if len(lst) == 2:
        return lst
    else:
        return (lst[0], l(*lst[1:]))

# *
def nock(noun):
    return tar(noun)

# ?
def wut(noun):
    return 1 if isinstance(noun, int) else 0

# +
def lus(noun):
    return 1 + noun if isinstance(noun, int) else noun

# =
def tis(noun):
    return 0 if noun[0] == noun[1] else 1

# this has a name in Nock so no need to call it fas
# /
def slot(noun):
    if noun[0] == 1:
        return noun[1]
    elif noun[0] == 2:
        return noun[1][0]
    elif noun[0] == 3:
        return noun[1][1]
    elif noun[0] % 2 == 0:
        return slot((2, slot((noun[0] // 2, noun[1]))))
    elif noun[0] % 2 == 1:
        return slot((3, slot(((noun[0] - 1) // 2, noun[1]))))

def tar(noun):
    if isinstance(noun[1][0], int):
        if noun[1][0] == 0:
            return slot((noun[1][1], noun[0]))
        elif noun[1][0] == 1:
            return noun[1][1]
        elif noun[1][0] == 2:
            return nock((nock((noun[0], noun[1][1][0])), nock((noun[0], noun[1][1][1]))))
        elif noun[1][0] == 3:
            return wut(nock((noun[0], noun[1][1])))
        elif noun[1][0] == 4:
            return lus(nock((noun[0], noun[1][1])))
        elif noun[1][0] == 5:
            return tis(nock((noun[0], noun[1][1])))
        elif noun[1][0] == 6:
            return nock(l(noun[0], 2, (0, 1), 2, l(1, noun[1][1][1][0], noun[1][1][1][1]), (1, 0), 2, l(1, 2, 3), (1, 0), 4, 4, noun[1][1][0]))
        elif noun[1][0] == 7:
            return nock(l(noun[0], 2, noun[1][1][0], 1, noun[1][1][1]))
        elif noun[1][0] == 8:
            return nock(l(noun[0], 7, l(l(7, (0, 1), noun[1][1][0]), 0, 1), noun[1][1][1]))
        elif noun[1][0] == 9:
            return nock(l(noun[0], 7, noun[1][1][1], l(2, (0, 1), (0, noun[1][1][0]))))
        elif noun[1][0] == 10:
            if isinstance(noun[1][1][0], int):
                return nock((noun[0], noun[1][1][1]))
            else:
                return nock(l(noun[0], 8, noun[1][1][0][1], 7, (0, 3), noun[1][1][1][0]))
    else:
        # line 17
        return (nock((noun[0], noun[1][0])), nock((noun[0], noun[1][1])))


if __name__ == "__main__":
    assert l(1) == (1, 0)
    assert l(1, 2) == (1, 2)
    assert l(1, 2, 3) == (1, (2, 3))
    assert l(1, 2, 3, 4) == (1, (2, (3, 4)))
    assert wut(1) == 1
    assert wut((1, 2)) == 0
    assert lus(1) == 2
    assert lus((1, 2)) == (1, 2)
    assert tis((1, 1)) == 0
    assert tis((1, 2)) == 1
    assert slot((1, 5)) == 5
    assert slot(l(2, 5, 6)) == 5
    assert slot(l(3, 5, 6)) == 6
    assert slot((1, l(l(4, 5), l(6, 14, 15)))) == l((4, 5), l(6, 14, 15))
    assert slot((2, l(l(4, 5), l(6, 14, 15)))) == (4, 5)
    assert slot((3, l(l(4, 5), l(6, 14, 15)))) == l(6, 14, 15)
    assert slot((7, l(l(4, 5), l(6, 14, 15)))) == (14, 15)
    assert nock(l(l(l(4, 5), l(6, 14, 15)), 0, 7)) == (14, 15)
    assert nock(l(42, 1, 153, 218)) == (153, 218)
    assert nock((77, l(2, (1, 42), l(1, 1, 153, 218)))) == (153, 218)
    assert nock((57, (0, 1))) == 57
    assert nock(((132, 19), (0, 3))) == 19
    assert nock((57, l(4, 0, 1))) == 58
    assert nock(((132, 19), l(4, 0, 3))) == 20
    assert nock((42, l(4, 0, 1))) == 43
    assert nock((42, l(3, 0, 1))) == 1
    assert nock((42, (l(4, 0, 1), l(3, 0, 1)))) == (43, 1)
    assert nock(((132, 19), l(10, 37, l(4, 0, 3)))) == 20
    assert nock((42, l(7, l(4, 0, 1), l(4, 0, 1)))) == 44
    assert nock((42, l(8, l(4, 0, 1), (0, 1)))) == (43, 42)
    assert nock((42, l(8, l(4, 0, 1), l(4, 0, 3)))) == 43
    assert nock((42, l(6, (1, 0), l(4, 0, 1), (1, 233)))) == 43
    assert nock((42, l(6, (1, 1), l(4, 0, 1), (1, 233)))) == 233
