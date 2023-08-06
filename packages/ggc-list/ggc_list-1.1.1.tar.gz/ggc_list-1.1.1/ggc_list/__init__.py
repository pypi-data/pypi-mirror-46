name = "ggc_list"



def  print_list (listObj):
        for item in listObj:
            if isinstance(item,list):
                print_list(item)
            else:
                print(item)