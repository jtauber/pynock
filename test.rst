Nock
====

>>> from nock import *

Everything in Nock is a noun. Nouns are either atoms or cells. Atoms are
unsigned integers. Cells are pairs of Nouns.

There is an internal function wut that tells you if something is an atom
or a cell:

>>> wut(1)
1
>>> wut((1, 2))
0

Another internal function tis tells you if the two nouns in a cell are
equal:

>>> tis((1, 1))
0
>>> tis((1, 2))
1

I don't know what tis should do if you give it an atom. Nor do I know whether
cells containing other cells should recursively pair-wise compare.

The internal function ``lus`` adds one to an atom but leaves a cell untouched:

>>> lus(1)
2
>>> lus((1, 2))
(1, 2)

>>> l(1)
(1, 0)
>>> l(1, 2)
(1, 2)
>>> l(1, 2, 3)
(1, (2, 3))
>>> l(1, 2, 3, 4)
(1, (2, (3, 4)))

>>> slot((1, 5))
5
>>> slot(l(2, 5, 6))
5
>>> slot(l(3, 5, 6))
6
>>> slot((1, l(l(4, 5), l(6, 14, 15))))
((4, 5), (6, (14, 15)))
>>> slot((2, l(l(4, 5), l(6, 14, 15))))
(4, 5)
>>> slot((3, l(l(4, 5), l(6, 14, 15))))
(6, (14, 15))
>>> slot((7, l(l(4, 5), l(6, 14, 15))))
(14, 15)

>>> nock(l(l(l(4, 5), l(6, 14, 15)), 0, 7))
(14, 15)
>>> nock(l(42, 1, 153, 218))
(153, 218)
>>> nock((77, l(2, (1, 42), l(1, 1, 153, 218))))
(153, 218)
>>> nock((57, (0, 1)))
57
>>> nock(((132, 19), (0, 3)))
19
>>> nock((57, l(4, 0, 1)))
58
>>> nock(((132, 19), l(4, 0, 3)))
20
>>> nock((42, l(4, 0, 1)))
43
>>> nock((42, l(3, 0, 1)))
1
>>> nock((42, (l(4, 0, 1), l(3, 0, 1))))
(43, 1)
>>> nock(((132, 19), l(10, 37, l(4, 0, 3))))
20
>>> nock((42, l(7, l(4, 0, 1), l(4, 0, 1))))
44
>>> nock((42, l(8, l(4, 0, 1), (0, 1))))
(43, 42)
>>> nock((42, l(8, l(4, 0, 1), l(4, 0, 3))))
43
>>> nock((42, l(6, (1, 0), l(4, 0, 1), (1, 233))))
43
>>> nock((42, l(6, (1, 1), l(4, 0, 1), (1, 233))))
233
