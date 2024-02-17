# We'll start by creating a function that expects an integer representing hours worked.   
def weeklyPayCalculator(hours_worked):
# We will also initialize base_hours to 40, standard_rate to 20, and overtime_rate to 30.  
    base_hours = 40
    standard_rate = 20
    overtime_rate = 30
# Our function will check if hours_worked exceeds base_hours.  
    if hours_worked > base_hours:
# If hours_worked exceeds base_hours, we will return:  
# (base_hours * standard_rate) + ((hours_worked - base_hours) * overtime_rate)  
        return (base_hours * standard_rate) + ((hours_worked - base_hours) * overtime_rate)
# If hours_worked does not exceed base_hours, we will return: hours_worked *  standard_rate
    else:
        return hours_worked * standard_rate
print(weeklyPayCalculator(60))