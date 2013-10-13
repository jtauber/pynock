A **noun** is either an **atom** (an unsigned integer) or a *cell*. A **cell** is an ordered pair of *nouns*.
The first *noun* in the cell is called the **head** and the second *noun* in the cell is called the **tail**,
i.e. `[head tail]`.

Nock evaluation (`*`) crashes (hangs) if given an *atom* so it should be given a *cell*. The components of a cell
given to `*` are the **subject** and the **formula**, i.e. `*[subject formula]`.

A *formula* must also be a *cell* otherwise `*` will crash.

Line 19 of the Nock spec handles the case where a *formula* starts with a *cell*. Lines 21 thru 33 handle the
case where the *formula* starts with an *atom* between `0` and `10`.

`*` will crash if given a *formula* that starts with an atom greater than `10`.

Because *nouns* are either *atoms* or *cells* and *cells* are pairs of *nouns*, the only structure in Nock is a binary
tree of unsigned integers.

`[0 n]` is a *formula* that, when applied to one of these trees, evaluates to a particular leaf or subtree given by `n`.
It is therefore a tree-addressing formula. This is implemented by lines 12 thru 17 plus 21 of the spec.

`[1 a]` is a *formula* that, when applied to anything, evaluates to `a`. In other words, it is a *constant function*.

`[2 [b c]]` is a *formula* that, when applied to `a`, first applies `c` to `a` then applies the *product* to
the *product* of applying `b` to `a`.

`[3 b]` is a *formula* that, when applied to `a`, first applies `b` to `a` then evaluates to `0` if the *product* is a
*cell* and `1` if the *product* is an *atom*.

`[4 b]` is a *formula* that, when applied to `a`, first applies `b` to `a` then, if the *product* is an *atom*,
evaluates to that *atom* plus one.

`[5 b]` is a *formula* that, when applied to `a`, first applies `b` to `a` then, evaluates to `0` if the *product*
is a *cell* with equal components and `1` if the *product* is a *cell* with non-equal components.

I presume it crashes if the *product* of applying `b` to `a` is an atom.

`[6 [b [c d]]]` is a *formula* that, when applied to `a`,  is equivalent to `c` if `*[a b]` is `0` and `d` if `*[a b]` is
`1`. It is therefore a basic `if` construct.

Much of the complexity is due to handling the case where `b` is neither `0` nor `1` (crashing rather than giving a bogus
result that tries to apply a subtree of `c` or `d` to `a`).

Let's try a reduction:

    *[a [6 [b [c d]]]] =>
    *[a [2 [[0 1] [2 [[1 [c d]] [[1 0] [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]]]
    *[*[a [0 1]] *[a [2 [[1 [c d]] [[1 0] [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]]
    *[a *[a [2 [[1 [c d]] [[1 0] [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]]
    *[a *[*[a [1 [c d]]] *[a [[1 0] [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]
    *[a *[[c d] *[a [[1 0] [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]
    *[a *[[c d] [*[a [1 0]] *[a [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]
    *[a *[[c d] [0 *[a [2 [[1 [2 3]] [[1 0] [4 [4 b]]]]]]]]]
    *[a *[[c d] [0 *[*[a [1 [2 3]]] *[a [[1 0] [4 [4 b]]]]]]]]
    *[a *[[c d] [0 *[[2 3] *[a [[1 0] [4 [4 b]]]]]]]]
    *[a *[[c d] [0 *[[2 3] [*[a [1 0]] *[a [4 [4 b]]]]]]]]
    *[a *[[c d] [0 *[[2 3] [0 *[a [4 [4 b]]]]]]]]
    *[a *[[c d] [0 *[[2 3] [0 +*[a [4 b]]]]]]]
    *[a *[[c d] [0 *[[2 3] [0 ++*[a b]]]]]]

If `*[a b]` evaluates to `0` then `++*[a b]` will be `2`. If `*[a b]` evaluates to `1` then `++*[a b]` will be `3`.

This is then used as a tree-address into `[2 3]`. Because `[0 2]` selects the left noun of a cell, `*[[2 3] [0 2]]` is
just `2`. And because `[0 3]` selects the right noun of a cell, `*[[2 3] [0 3]]` is just `3`.

This may seem like an identity operation but it insures the correct behaviour if `b` is neither `0` nor `1`. if `x` is an
atom greater than `3` or if `x` is a cell, `*[[2 3] [0 x]]` crashes.

Why does `*[[2 3] [0 x]]` crash if `x` is a cell? Well no other rule but line 17 applies.

Why does `*[[2 3] [0 x]]` crash if `x` is, say `4`?

    /[4 [2 3]] =>
    /[2 /[2 [2 3]] =>
    /[2 2]

which crashes because, at that point, no other rule but line 17 applies.

We can now use the sanitized tree address into `[c d]` and either get `c` or `d` as appropriate without risk that some
subtree of `c` or `d` will be applied to `a`.

`[7 [b c]]` is a *formula* that, when applied to `a`, first applies `b` to `a` then applies `c` to the *product*.
It is therefore just *function composition*.

Here is a reduction:

    *[a [7 [b c]]] ☞
    *[a [2 [b [1 c]]]] ☞
    *[*[a b] *[a [1 c]]] ☞
    *[*[a b] c]

`[8 [b c]]` is a *formula* that, when applied to `a`, first applies `b` to `a` then applies `c` to the ordered pair of
that *product* and the original *subject* `a`.

In other words: `*[[*[a b] a] c]`

To do a reduction from line 30, we're going to need to make use of line 19, though, because after the first two steps:

    *[a [8 [b c]]] ☞
    *[a [7 [[[7 [[0 1] b]] [0 1]] c]]] ☞
    *[*[a [[7 [[0 1] b]] [0 1]]] c] ☞

we end up needing to know how to apply a *formula* whose *head* is a *cell*, not just an *atom* like we've been
dealing with up until this point.

Line 19 basically says that a *formula* that doesn't start with an *atom* is treated as a list of *formulas* to apply,
kind of like `map` would.

    *[a [[b c] d]]  ☞  [*[a [b c]] *[a d]]

Now we can continue our reduction of line 30:

    *[a [8 [b c]]] ☞
    *[a [7 [[[7 [[0 1] b]] [0 1]] c]]] ☞
    *[*[a [[7 [[0 1] b]] [0 1]]] c] ☞
    *[[*[a [7 [[0 1] b ]]] *[a [0 1]]] c] ☞
    *[[*[*[a [0 1]] b] *[a [0 1]]] c] ☞
    *[[*[a b] a] c]

You may have noticed that the *formula* `[0 1]` is the *identity* operator. That is, `*[a [0 1]]` is `a`. This is clear
from lines 21 and 12.

A **core** is a *cell* whose *tail* is data (possibly containing other *cores*) and whose *head* is code containing one
or more *formulas*. The *head* of a *core* is called the **battery** and the *tail* of a *core* is called the **payload**.

A *formula* in the *battery* of a *core* is called an **arm** of the *core*.

An *arm* is evaluated by applying it to the *core* it's part of, sort of like a method on a Python class taking only
`self`.

`[9 [b c]]` is the *formula* for evaluating *arms*. It is a *formula* that, when applied to `a`, firstly applies `c` to
`a`. The *product* is taken to be a *core* containing within it an *arm* (at address `b`, hence retrievable by `[0 b]`)
that is then applied to the *core* (that *product* as a whole).

Here is the reduction:

    *[a [9 [b c]]] ☞
    *[*[a c] [2 [[0 1] [0 b]]]] ☞
    *[*[*[a c] [0 1]] *[*[a c] [0 b]]] ☞
    *[*[a c] *[*[a c] [0 b]]]

