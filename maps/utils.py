
epsilon = 0.000000000001

   
def calcSize(number):
#     return pow(math.ceil(math.log(number)/math.log(2)))
    power = 1
    while(power < number):
        power = power*2
    return power
def resultsFromJson(str):
    if str['status'] == 'OK':
        return str['results']
def float_equal(a,b):
    return abs(a - b) <= epsilon