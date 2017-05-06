def play_number(number):
    if number == 0:
        print("lol")
    else:
        if number < 0:
            print 'minus'
        number = abs(number)
        numberString = list(str(number))
        for digit in numberString:
            print(digit)
            
play_number(-440)
            
