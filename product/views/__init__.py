from product.views.create_comment import CreateComment
from product.views.get_item import GetItem
from product.views.get_list import GetList


class SingleItem(CreateComment, GetItem):
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
