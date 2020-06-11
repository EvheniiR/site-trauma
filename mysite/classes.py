class Product(object):
    """info about name of pruduct, link and image"""
    def __init__(self, product_id, name, link, image, cost):
        self.product_id = product_id
        self.name = name
        self.link = link
        self.image = image
        self.cost = cost

    @staticmethod
    def from_db_row(cell_list):
        return Product(product_id=cell_list[0], name=cell_list[1], link=cell_list[2], image=cell_list[3], cost=cell_list[4])


class Category(object):
    """info about name of category, id, link and image"""
    def __init__(self, category_id, name, link, image):
        self.category_id = category_id
        self.name = name
        self.link = link
        self.image = image

    @staticmethod
    def from_db_row(cell_list):
        return Category(category_id=cell_list[0], name=cell_list[1], link=cell_list[2], image=cell_list[3])


class Certificate(object):
    """docstring for Certificate"""
    def __init__(self, name, image):
        self.name = name
        self.image = image

    @staticmethod
    def from_db_row(cell_list):
        return Certificate(name=cell_list[0], image=cell_list[1])
        

class NavItem(object):
    """info about items of navigation"""
    def __init__(self, name, link):
        self.name = name
        self.link = link

        
class Navigation(object):
    def __init__(self, highlight):
        self.highlight = highlight
        self.nav_items = []

    def push(self, elem):
        self.nav_items.append(elem)

    def __len__(self):
        return len(self.nav_items)


class User(object):
    def __init__(self, user_id, login):
        self.user_id = user_id
        self.login = login
        self.shopping_cart = {}

    def push(self, key, value):
        self.shopping_cart[key] = value


    