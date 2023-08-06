

def find_max(my_list):
    
    max_num = my_list[0]
    for i in my_list:
        if i > max_num:
            max_num = i
    print(f"Maximum number is: {max_num}")
    print(len(my_list))        

        
        

if __name__ == "__main__":
    find_max([100,200,250,500,50])