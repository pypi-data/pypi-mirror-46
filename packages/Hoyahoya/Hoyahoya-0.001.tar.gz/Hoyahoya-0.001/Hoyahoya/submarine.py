class Submarine: #ประกาศ Class
    '''
    ------------------Print Document---------------------
    ---------------------------------------
    '''
    def __init__(self,price=10000,budget=1000000): #ประกาศ เหมือน this ใน php  เป็นค่าเริ่มต้นของ Function  ในทุก function ต้องมี self
        
        self.caption = 'Prawit'  #ใน class init ต้องมี self นำหน้าเพื่อเอาไปใช้ function อื่นได้
        self.sub_name = 'Uncle I'
        self.price = price #Million
        self.kilo = 0
        self.budget = budget #budget /ลำ
        self.totalcost = 0
    def Missile(self):
        print('We are Department Of Missile')

    def Calcommission(self):
        pc = 10 #10%
        percent = self.price * (pc /100)
        print('Loong! You Got: {} Million Bath'.format(percent)) #.format คือการ place ตัวแปรไปในช่อง
    
    def Goto(self,enemypoint,distance):
        print(f"Let 's go to : {enemypoint} Distance: {distance} KM.")  # f คือ format แบบย่อ
        self.kilo = self.kilo+distance
        self.Fual() #เป็นการเรียกใช้ Function ที่อยู่ใน Class

    def Fual(self):
        diesel = 20 #20 /lite
        cal_fual_cost = self.kilo * diesel 
        print('Current Feul Cost : {:,d} Bath'.format(cal_fual_cost)) #format ตัวเลข {:,d}
        self.totalcost +=cal_fual_cost
    @property  # ถ้ามี property ต้องมี return  โดย property เป็นคำนาม
    def BudgetRemaining(self):
        '''
        ---------
        ถ้ามี property ต้องมี return  โดย property เป็นคำนาม
        ---------
        '''
        remaining = self.budget - self.totalcost
        print('BudgetRemain : {:,.2f}'.format(remaining))
        return remaining

class ElectricSubmarine(Submarine): #class ที่มีการสอบทอบ
    def __init__(self,price=10000,budget=1000000):
        self.sub_name = 'Uncel 3'
        self.batterydistance = 100000 #submarine can go 100000 km/100%
        super().__init__(price,budget) #super คือคำสั่งที่ใช้ในการสืบทอด Class Submarine เหมือนการ Copy
    
    def Battery(self):
        allbattery = 100
        calculate = (self.kilo/self.batterydistance) * 100 
        print('We have Battery Remaining: {}%'.format(allbattery - calculate))    

    def Fual(self):

        kilowatcost = 5 #20 /lite
        cal_fual_cost = self.kilo * kilowatcost 
        print('Current Power Cost : {:,d} Bath'.format(cal_fual_cost)) #format ตัวเลข {:,d}
        self.totalcost +=cal_fual_cost   

#print(__name__)
if __name__ == '__main__': #ให้รันได้เฉพาะไฟล์ของตัวเองเท่านั้น

    tesla = ElectricSubmarine(40000,2000000)
    print(tesla.caption)
    print(tesla.budget)
    tesla.Goto('japan',10000)
    print(tesla.BudgetRemaining)
    tesla.Fual()
    tesla.Battery()
'''
print('-------------------------')
kongtabbok = Submarine(40000,2000000)
print(kongtabbok.caption)
print(kongtabbok.budget)
kongtabbok.Goto('japan',10000)
print(kongtabbok.BudgetRemaining)
kongtabbok.Fual()
'''
'''
kongtabreuw = Submarine(65400)  #ประกาศตัวแปรสำหรับเรียกใช้งาน Class Submarine
print(kongtabreuw.caption)
print(kongtabreuw.sub_name)
print('-------------------------')

kongtabreuw.Calcommission()

##################################
print('------------Sub No 2-----------------')
kongtabbok = Submarine(70000)
print('Before...............')
print(kongtabbok.caption)
print('After.........')
kongtabbok.caption = 'Srivara' #สามารถเปลี่ยน ค่า ที่อยู่ใน Class ได้
print(kongtabbok.caption)

print('---------------------------')

kongtabreuw.Goto('Chaina',8000)
print(kongtabreuw.kilo)

print("----------------")
kongtabreuw.Fual()

print('-------------------')
current_budget = kongtabreuw.BudgetRemaining # เวลาเรียกใช้ property ไม่ต้องมี () เพราะเป็นคำนาม
print(current_budget * 0.2)
'''