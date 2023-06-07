from warcraft_api import request_person

re = request_person('Eu' , 'Arygos' , 'Natureslight')

if re.get_request() == True :
    a = next(re.raid_progress())
else :
    print('failed')

print(a)