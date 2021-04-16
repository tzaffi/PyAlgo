from contextlib import redirect_stdout
import io

from data_structures.avl_tree import sbbst


def test_basic():
    ST = sbbst()
    nums = [128, 131, 4, 134, 135, 10, 1, 3, 140, 14, 142, 145, 146, 147, 149]  # random numbers
    for num in nums:
        ST.insert(num)
    # It also works out: ST = sbbst(nums)
    print(ST)
    print("Number of elements:", ST.getSize())
    print("Height:", ST.getHeightTree())
    print("Min val:", ST.getMinVal())
    print("Max val:", ST.getMaxVal())
    print("3rd smallest val:", ST.kthsmallest(3))
    print("2nd largest val:", ST.kthlargest(2))
    print("Pre Order:", ST.inOrder())
    print("In Order:", ST.preOrder())
    print("Post Order:", ST.postOrder())
    ST.delete(128)
    ST.delete(140)
    print(ST)
    ST.insert(55)
    print(ST)
    print("Number of elements:", ST.getSize())
    # assert False


def test_large_list():
    large_list = [41, 8467, 6334, 6500, 9169, 5724, 1478, 9358, 6962, 4464, 5705, 8145, 3281, 6827, 9961, 491, 2995, 1942, 4827, 5436, 2391, 4604, 3902, 153, 292, 2382, 7421, 8716, 9718, 9895, 5447, 1726, 4771, 1538, 1869, 9912, 5667, 6299, 7035, 9894, 8703, 3811, 1322, 333, 7673, 4664, 5141, 7711, 8253, 6868, 5547, 7644, 2662, 2757, 37, 2859, 8723, 9741, 7529, 778, 2316, 3035, 2190, 1842, 288, 106, 9040, 8942, 9264, 2648, 7446, 3805, 5890, 6729, 4370, 5350, 5006, 1101, 4393, 3548, 9629, 2623, 4084, 9954, 8756, 1840, 4966, 7376, 3931, 6308, 6944,
                  2439, 4626, 1323, 5537, 1538, 6118, 2082, 2929, 6541, 4833, 1115, 4639, 9658, 2704, 9930, 3977, 2306, 1673, 2386, 5021, 8745, 6924, 9072, 6270, 5829, 6777, 5573, 5097, 6512, 3986, 3290, 9161, 8636, 2355, 4767, 3655, 5574, 4031, 2052, 7350, 1150, 6941, 1724, 3966, 3430, 1107, 191, 8007, 1337, 5457, 2287, 7753, 383, 4945, 8909, 2209, 9758, 4221, 8588, 6422, 4946, 7506, 3030, 6413, 9168, 900, 2591, 8762, 1655, 7410, 6359, 7624, 537, 1548, 6483, 7595, 4041, 3602, 4350, 291, 836, 9374, 1020, 4596, 4021, 7348, 3199, 9668, 4484, 8281, 4734, 53, 1999]

    ST = sbbst()
    window = 20
    win = large_list[:window]
    for n in win:
        ST.insert(n)

    assert ST.getMaxVal() == max(win)
    assert ST.getMinVal() == min(win)

    for i in range(1, len(large_list) - window):
        falls_out, comes_in = large_list[i-1], large_list[i + window - 1]
        ST.delete(falls_out)
        ST.insert(comes_in)

        win = large_list[i:i+window]
        print(f"falls_out, comes_in = {falls_out}, {comes_in}")
        print(win)
        assert ST.getMaxVal() == max(win), win
        assert ST.getMinVal() == min(win), win
