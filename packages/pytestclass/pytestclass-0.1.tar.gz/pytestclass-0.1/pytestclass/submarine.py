class Submarine:

    def __init__(self,price,budget):

        self.Captain ='Prawit'
        self.sub_name ='Uncle I'
        self.price=price #Million
        self.kilo=0
        self.budget=budget
        self.totalcost=0
        
    def Missile(self):
        print('We are Department of Missile')
    
    def calcommission(self):
        percent =10 #10%
        commission=self.price*(percent/100)
        print('Loong get: {} Million Bath'.format(commission))
        
    def calcommission2(self,pc):
        in_pc=pc
        self.percent =in_pc #10%
        commission=self.price*(self.percent/100)
        print('Loong get: {} Million Baht'.format(commission))
    
    def Goto(self,enemypoint,distince):
        #f is ".format"
        print(f'let \'go to {enemypoint} Distince:{distince} KM')
        self.kilo=self.kilo+distince
        self.Fuel()
    
    def Fuel(self):
        deisel=20 # 20 bath/litre
        cal_fuel_cost= self.kilo *deisel
        print(f"current Feul cost:{cal_fuel_cost:,d} Baht")
        self.totalcost+=cal_fuel_cost
        
    @property    
    def budgetremaining(self):
        remaining = self.budget - self.totalcost
        print("Budget Remaining :{:,.2f} Baht".format(remaining))
        return remaining


class Electricsubmarine(Submarine):
    
    def __init__(self,price,budget):
#         self.Captain ='Prayut'
        self.sub_name ='Uncle III' 
        self.battery_distance =1000000
        #can go out 1000000 km / 100 percent
        super().__init__(price,budget)
        
           
    def battery(self):
        allbattery=100
        batteryuse=(1000 *self.kilo )/self.battery_distance
        print("We use battery :{} %".format(batteryuse))
        print("We have battery :{} %".format(allbattery-batteryuse))
        
    def calbettery(self):
        print(self.kilo)
        
    def Fuel(self):
        kilowat=5 # 20 bath/litre
        cal_fuel_cost= self.kilo *kilowat
        print(f"current Power cost:{cal_fuel_cost:,d} Baht")
        self.totalcost+=cal_fuel_cost