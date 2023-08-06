def list_lol(the_list):
#   遍历list,取出所有元素
	for item in the_list:
		if isinstance(item, list):
			list_lol(item)
		else:
			print(item)

