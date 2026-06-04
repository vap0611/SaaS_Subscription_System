from plans import add_plan, view_plans, update_plans, delete_plan 
from customers import add_customer, view_customers, update_customers, delete_customer
def plan_module():
    while True:
        print("Plan Module")
        print("1. Add plan\n 2. View Plan \n 3. Update plan\n 4. Delete plan\n  5. Exit \n")
        ch= int(input("Enter your choice"))
        match ch:
            case 1:
                add_plan()
            case 2: 
                view_plans()
            case 3:
                update_plans()
            case 4: 
                delete_plan()
            case 5: 
                print("Thank you for using the system")
                break
            case _:
                print("Invalid choice") 
def customer_module():
    while True:
        print("Customers Module")
        print("1. Add Customer\n 2. View Customers \n 3. Update Custmoers\n 4. Delete Customers\n  5. Exit \n")
        ch= int(input("Enter your choice"))
        match ch:
            case 1:
                add_customer()
            case 2: 
                view_customers()
            case 3:
                update_customers()
            case 4: 
                delete_customer()
            case 5: 
                print("Thank you for using the system")
                break
            case _:
                print("Invalid choice") 


while True:
    print("You want to login as: \n 1. Admin \n 2. Staff\n3.Exit \n")
    choice1 = int(input("Enter your choice :"))
    if choice1 == 1:
        user =input("Enter user name")
        passwd = input("Enter password")
        if user == "admin123" and passwd == "admin@123":
            print("Welcome Admin ! You can access all the modules")
            print("Which module you want to access? \n 1. Plan Module \n 2. Customer module \n 3. Exit \n")
            choice2 = int(input("Enter your choice: "))
            match choice2:
                case 1: 
                    plan_module()
                case 2: 
                    customer_module()
                case 3:
                    print("Thank you for using our service !!")
                    break
                case _:
                    print("Invalid Choice !")
        else:
            print("Invalid User name or password !!")
    
    elif choice1 == 2:
        user =input("Enter user name")
        passwd = input("Enter password")
        if user == "staff123" and passwd == "staff@123":
            print("Welcome Staff ")
            print("Which module you want to access? \n 1. Customer Module \n 2. Exit \n")
            choice2 = int(input("Enter your choice: "))
            match choice2:
                case 1: 
                    customer_module()
                case 2:
                    print("Thank you for using our Service ")
                    break

                case _:
                    print("Invalid Choice !")
        else:
            print("Invalid username or password !!")
    elif choice1 == 3:
        print('Quitting !! ')
        break  
    else:
        print("Invalid input !! ")  

    
        

        
