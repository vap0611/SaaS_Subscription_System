from plans import add_plan, view_plans, update_plans, delete_plan

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