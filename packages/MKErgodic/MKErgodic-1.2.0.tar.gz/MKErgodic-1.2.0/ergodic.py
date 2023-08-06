def print_lol(the_list, indent=False, level=0):
#   深层遍历list,打印所有元素
        for item in the_list:
                if isinstance(item, list):
                        print_lol(item, level+1)
                else:
                        if indent:
                                for tab_stop in range(level):
                                        print("\t",end='')
                        print(item)

