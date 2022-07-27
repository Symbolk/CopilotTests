import six
def paging(response, max_results):
    """Returns WAPI response page by page

    Args:
        response (list): WAPI response.
        max_results (int): Maximum number of objects to be returned in one page.
    Returns:
        Generator object with WAPI response split page by page.
    """
    i = 0
    while i < len(response):
        yield response[i:i + max_results]
        i = i + max_results

def test_paging():
    """
    Check the corretness of paging
    """
    assert list(paging([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3)) == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]
    assert list(paging([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 4)) == [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10]]
    assert list(paging([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)) == [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
    assert list(paging([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 6)) == [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10]]
    assert list(paging([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 7)) == [[1, 2, 3, 4, 5, 6, 7], [8, 9, 10]]

