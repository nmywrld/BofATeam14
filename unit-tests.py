from buyOrderNode import buyOrderNode
from sellOrderNode import sellOrderNode

def test():
    smaller_buy = buyOrderNode(1, "order_id1", "insturment_1", 500, "client_!", '5', "Buy", 'Y', '5')
    bigger_buy = buyOrderNode(1, "order_id1", "insturment_1", 500, "client_!", '4', "Buy", 'Y', '5')
    assert smaller_buy < bigger_buy, "comparator is wrong!"

if __name__ == "__main__":
    test()
    print("Everything passed")