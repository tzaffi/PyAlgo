from bisect import bisect_right
from typing import Dict


class DecisionGrid:
    """
    In a model depending on two numerical features each of which is positively correlated
    with a positive outcome, there could be a simple monotonic boundary that determines
    the prediction. Though this sort of situation can be handled with a decision tree,
    a decision tree is non-ideal as the natural ordering of the second variable could get lost,
    and this is an unnecessarily complex data structure.
    It suffices to represent such a predictor using a 2 arrays.

    For example, suppose we are trying to predict whether a customer who tastes a grape
    will then purchase a bunch of those grapes. We assume two variables:
    * n - the number of grapes that can be purchased for $1
    * s - sweetness of grape from 0-10 as described by customer
    (I intentionally used n instead of cost, as I want each feature to be positively correlated
    with likelihood of purchase)

    Let's assume that the following cutoffs are used for predicting purchase:
    * 0 <= s < 2    - purchase when 20 <= n
    * 2 <= s < 6    - purchase when 10 <= n
    * 6 <= s < 8    - purchase when 5 <= n
    * 8 <= s        - purchase regardless of price

    This grid can be represented as follows:
    y
    20|********
    10|XX******
     5|XXXX****
     0|XXXXXX**
    --+0 2 6 8 x
    """

    def __init__(self, cutoffs: Dict[float, float], verbose: bool = False):
        self.cutoffs = cutoffs
        self.x_cuts = sorted(cutoffs.keys())
        self.y_cuts = [self.cutoffs[x] for x in self.x_cuts]
        self.verbose = verbose

        if self.verbose:
            print(f"x_cuts: {self.x_cuts}")
            print(f"y_cuts: {self.y_cuts}")

    def __str__(self) -> str:
        assert 0 < min(self.x_cuts) and 0 < min(self.y_cuts), "string representation assumes positive lowest cuts"
        xs, ys = [0] + self.x_cuts, self.y_cuts + [0]
        x_width = max(map(lambda x: len(str(x)), xs)) + 1
        y_width = max(map(lambda x: len(str(x)), ys))

        def make_box(x_y):
            x, y = x_y
            return ("*" if self.is_approved(x, y) else "X") * x_width

        def make_row(y):
            return f"{y:>{y_width}d}|{''.join(map(make_box, ((x,y) for x in xs)))}"

        rows = ["y"]
        rows.extend(map(make_row, ys))
        last_row = "-" * y_width
        last_row += "+"
        last_row += "".join((f"{str(x):{x_width}s}" for x in xs))
        last_row += "x"
        rows.append(last_row)
        return "\n".join(rows)

    def is_approved(self, x: float, y: float) -> bool:
        return (idx := bisect_right(self.x_cuts, x)) == len(self.y_cuts) or self.y_cuts[idx] <= y
