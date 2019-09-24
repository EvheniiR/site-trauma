class Product(object):
	"""info about name of pruduct, link and image"""
	def __init__(self, name, link, image):
		self.name = name
		self.link = link
		self.image = image

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
