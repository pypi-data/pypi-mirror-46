from cova_client_request import covatls 

class Test(object): 
    def __init__(self): 
        super(Test,self).__init__() 
        self.conn = covatls() 
    
    def test1(self): 
        res = self.conn.get("http://127.0.0.1:8080/new_task/1") 
        self.test1_session = self.conn.session_id 

        if res == 'my_func' :
            print("test1 Passed") 

        else: 
            print("test1 doesn't match") 

    def test2(self): 
        data = {"mottakin_bhai" : "BOSS"} 
        res = self.conn.post("http://127.0.0.1:8080/new_task/1", data) 
        self.test2_session = self.conn.session_id 

        if res == 'Pmy_func BOSS' :
            print("test2 Passed") 

        else: 
            print("test2 doesn't match") 

    def test3(self): 
        res = self.conn.get("http://127.0.0.1:8080/init_task/1/2", self.test2_session) 
        
        if res == 'my_func2' :
            print("test3 Passed") 

        else: 
            print("test3 doesn't match") 

    def test4(self): 
        data = {"mottakin_bhai" : " BOSS"} 
        res = self.conn.post("http://127.0.0.1:8080/init_task/1/2/", data, self.test1_session) 

        if res == 'Pmy_func2 BOSS' :
            print("test4 Passed") 

        else: 
            print("test4 doesn't match") 
    
    def test5(self):
        data = {'datahash': 'bc03f4e15c8a9779f10cd74d6c63d15d9338820406baa0014996fa1b452afeb5', 'code_bin': "import time\nMAX_INT_MOD = 2 ** 256\nNUM = 8e4\n\ndef vm_func(n = NUM, M = MAX_INT_MOD):\n\n    now_time = time.time()\n\n    num = 1000000007\n    n = int(n)\n    \n    for i in range(1, n):\n        num = (num * num) % M\n\n    print(num)\n\n    print('Total Time : ' + str(time.time() - now_time))\n\n    return str(time.time())\n\nraise __COVA__.ReturnData(vm_func())\n", 'timeout': '1000', 'public_key': '-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDgYYgNLizFrqhfOEEkLIoP1dBo\nQKkOgUqUq5VPlkxrs6vtWaZua9YqrPFwMUTv9keF589+8eC33B+crOodblgn3qIY\nhEGrPjObr6yWzKWGtrpzYUKA502XH5LyfmTxEgiA+p2hs/sOIYMFLPaoJc5ut07b\n9Cm+eE/L50slo0oshQIDAQAB\n-----END PUBLIC KEY-----'}
        address = "http://cova0@ns544952.ip-66-70-180.net:10002/data_user/init_task/0"
        res = covatls().post(address, data)

    def run(self): 
        # self.test1() 
        # self.test2() 
        # self.test3() 
        # self.test4() 
        print(covatls().get("http://ns544952.ip-66-70-180.net:10000/status_ok"))
        self.test5()

obj = Test() 
obj.run()     
