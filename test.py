class Tree(object):
    """
    树结构测试
    """
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right


t1 = Tree("A", "B")
t2 = Tree(Tree("A"))
hasp_test = {
    t1: t1,
    '1-tree': t1,
    2: t2,
    21: t2,
    '2-tree': t2,
    '3-tree': Tree(),
    4: Tree()
}

def function(hasp_test:dict):
    first_hash = {}
    # 哈希表key-value翻转
    for key, value in hasp_test.items():
        if value not in first_hash:
            first_hash[value] = [key]
        else:
            temp = first_hash[value]
            temp.append(key)
            first_hash[value] = temp
    
    for key, value in first_hash.items():
        if len(value) != 1:
            for each in value:
                if type(each) == type(''):
                    first_hash[key] = each
        elif len(value) == 1:
            first_hash[key] = value[0]
    second_hash = {}
    for key, value in first_hash.items():
        second_hash[value] = key
    return second_hash

def add_new():
    """
    增加新的key
    """
    pass

if __name__ == "__main__":
    hasp_test['3'] = hasp_test[4]
    new_dict = {}
    new_dict = function(hasp_test)
    hasp_test.clear()
    hasp_test = new_dict.copy()
    new_dict.clear()
