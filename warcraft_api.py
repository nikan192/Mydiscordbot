import requests
import json


#setting the object to get the info from user
class request_person :

    def __init__(self , user_region , user_realm , user_name) :
        
        print("in init")
        self.region_char = user_region
        self.realm_char = user_realm
        self.name_char = user_name
        self.data = ''
        return

    def get_request(self) -> bool:
        #using api of raider io getting character info putting it into json
        print("in req")
        url = f'https://raider.io/api/v1/characters/profile?region={self.region_char}&realm={self.realm_char}&name={self.name_char}&fields=gear%2Ctalents:categorized%2Cguild%2Ccovenant%2Cmythic_plus_scores_by_season:current%2Craid_progression%2Cmythic_plus_ranks'
        print(url)
        headers = {'accept': 'application/json'}
        requset_resp = requests.get(url , headers=headers)

        #if http request is true and 200 we can begin with putting json into some file
        if requset_resp.status_code != 200 :
            return False
        elif requset_resp.status_code == 200 :
            print("req is good")
            #load json and sent it to sort in the list
            self.data = json.loads(requset_resp.content)
            print(self.data['profile_url'])
            return True
    def get_url_profile(self) -> str :
        yield self.data['profile_url']
    
    def get_name(self) -> str :
        yield self.data['name']
    
    def get_faction(self) -> str :
        yield self.data['faction']
    
    def get_race(self) -> str :
        yield self.data['race']

    def get_class(self) -> str :
        yield self.data['class']

    def get_active_spec_role(self) -> str :
        yield self.data['active_spec_role']

    def get_active_sepc_name(self) -> str :
        yield self.data['active_spec_name']

    def items(self) -> str :
        dic = {}

        for i in self.data['gear']['items'].keys() :
            dic[i] = list()
            dic[i].append(str(self.data['gear']['items'][i]['name']))
            dic[i].append(str(self.data['gear']['items'][i]['item_level']))
            dic[i].append(str(self.data['gear']['items'][i]['item_quality']))

        string = str()

        for i in dic.keys() :
            string += str(f'''{i} :  Name  :  {dic[i][0]}  Item level  :  {dic[i][1]}  Item quality  :  {dic[i][2]}\n''')

        yield string

    def talents(self) -> str :
            
            string = str()
            for i in self.data['talentLoadout']['spec_talents']:
                for j in i.values():
                    if isinstance(j, dict):
                        for i in j.values() :
                            if isinstance(i , list) :
                                for k in i :
                                    if isinstance(i , list) :
                                        for x in i :
                                            if isinstance(x , dict) :
                                                for o in x.values() :
                                                    if isinstance(o , dict) :
                                                        string += (f'{o["name"]} : {o["rank"]} \n')


            yield string
    

    def total_score_item(self) -> str :
        yield self.data['gear']['item_level_equipped']


    def raid_progress(self) -> str :

        content = str('')

        dic = {}

        for i in self.data['raid_progression'].keys() :
            dic[i] = []

        for i in self.data['raid_progression'].keys() :
            for j in self.data['raid_progression'][i].items() :
                dic[i].append(j)
        
        for i in dic.keys() :
            content += str('\n')
            content += str(i) + str(' : ') + str('\n')
            for j in dic[i] :
                content += str(j) + str(' ')
            
            content = content.replace("(", chr(0)).replace(")", chr(0)).replace(",", chr(0))

            lines = content.splitlines()

            pairs = [line.split() for line in lines]

            fixed_content = "\n".join([" ".join(pairs) for pairs in pairs])

        yield fixed_content

    def mythic_scores(self) -> str :

        scores = dict()

        string = str()

        for i , j in self.data['mythic_plus_scores_by_season'][0]['scores'].items() :
            scores[i] = j
        
        for i in self.data['mythic_plus_scores_by_season'][0]['scores'].keys() :
            string += f'\n{i.capitalize()} : {str(self.data["mythic_plus_scores_by_season"][0]["scores"][i])} \n'

        yield string

    def mythic_rank(self) -> str :
        dic = dict(self.data['mythic_plus_ranks'].items())
        string = str()

        for key, value in dic['overall'].items():
            string += f'Overall {key.capitalize()}: {value}\n'
            string += '\n'
        
        if 'class' in dic.keys() :
            for key, value in dic['class'].items():
                string += f'Class {key.capitalize()}: {value}\n'
                string += '\n'
        
        if 'tank' in dic.keys() :
            for key, value in dic['dps'].items():
                string += f'DPS {key.capitalize()}: {value}\n'
                string += '\n'

        if 'tank' in dic.keys() :
            for key, value in dic['tank'].items():
                string += f'Tank {key.capitalize()}: {value}\n'
                string += '\n'

        if 'healer' in dic.keys() :
            for key, value in dic['healer'].items():
                string += f'Healer {key.capitalize()}: {value}\n'
                string += '\n'

        yield string
    
    def get_banner_url(self) -> str :
        yield self.data['thumbnail_url']