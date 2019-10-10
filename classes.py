class Product(object):
	"""info about name of pruduct, link and image"""
	def __init__(self, name, link, image):
		self.name = name
		self.link = link
		self.image = image

	@staticmethod
	def from_db_row(cell_list):
		return Product(name=cell_list[0], link=cell_list[1], image=cell_list[2])

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
	"""docstring for Navigatin"""
	def __init__(self, highlight):
		self.highlight = highlight
		self.nav_items = []

	def push(self, elem):
		self.nav_items.append(elem)

	def __len__(self):
		return len(self.nav_items)
