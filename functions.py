

def getUrlofDanawa(searchPage, keyword, pageNum, tab="goods", limit="90"):
    """
    :param searchPage: 검색 양식
    :param tab: 광고제거 여부(goods==제거)
    :param limit: 보여지는 상품 개수
    :param keyword: 검색할 키워드
    :param pageNum: 페이지 번호
    :return:
    """
    return searchPage + "?" + "tab=" + tab + "&limit=" + limit + "&query=" + keyword + "&page=" + str(pageNum)