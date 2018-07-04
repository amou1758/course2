from account.models import User


class MyPagination(object):
    def __init__(self, totalCount, currentPage, perPageItemNum=30, maxPageNum=10, url=None):
        # 总条目数
        self.total_count = totalCount
        # 当前页
        try:
            v = int(currentPage)
            if v <= 0:
                self.current_page = 1
            else:
                self.current_page = v
        except Exception as e:
            self.current_page = 1
        # 每页显示多少
        self.per_page_item_num = perPageItemNum
        # 显示多少页码
        self.per_page_numb = maxPageNum
        # 加入跳转url
        self.url = url

    def start(self):
        return (self.current_page - 1) * self.per_page_item_num

    def end(self):
        return self.current_page * self.per_page_item_num

    @property
    def num_pages(self):
        a, b = divmod(self.total_count, self.per_page_item_num)
        if b == 0:
            return a
        return a + 1
