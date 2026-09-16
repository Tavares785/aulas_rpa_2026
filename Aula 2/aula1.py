def classify_age():
    try:
        # Get age input from the user
        age = int(input("Enter your age: "))
        
        if age < 0:
            print("Please enter a valid positive age.")
        elif age <= 12:
            print("You are a child.")
        elif age <= 59:
            print("You are an adult.")
        else:
            print("You are an older adult (senior).")
            
    except ValueError:
        print("Invalid input. Please enter a whole number.")

# Run the function
classify_age()