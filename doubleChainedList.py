class DCList: #Double Chained List
	def __init__(self,content, previous = None, next = None): # content : some_type, previous : DCList, next : DCList
		self.content = content
		self.previous = previous
		self.next = next

# ~ node = DCList(1,None,None)
# ~ node2 = DCList(2,None,None)
# ~ node.next = node2
# ~ print(node.content,node.next.content)
