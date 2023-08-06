def print_lol(the_list, level):
#   遍历list,取出所有元素
	for item in the_list:
		if isinstance(item, list):
			list_lol(item, level+1)
		else:
            for tab_stop in range(level):
                print("\t", end='')
			print(item)

