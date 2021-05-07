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
    * 8 <= s        - purchase regardless of price
    * 6 <= s < 8    - purchase when 5 <= n
    * 2 <= s < 6    - purchase when 10 <= n
    * 0 <= s < 2    - purchase when 20 <= n

    This grid can be represented as follows:
    y=n
    20|😎😎😎😎😎😎😎
    10|😡😎😡😎😎😡😎
     5|😡😎😡😎😎😡😎
     0|😡😎😡😎😎😡😎
    --+ 0 2 6-8-
    """
