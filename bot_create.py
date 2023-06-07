import discord
#from web_server_loop import keep_alive       this library is nor required because i used it to run my bot in repl without getting shutdow
import os
import warcraft_api
import datetime
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix='$' , intents = discord.Intents.all())

@bot.event
async def on_ready() :
    sys = await bot.tree.sync()
    print(f'{len(sys)} commands has been synced !')
    total = bot.tree.get_commands()
    print(f'{len(total)} total commands we have !')


@bot.tree.command(name='search_character' , description='this command search for character and show very quick and basic info of character !')
@app_commands.describe(region = 'Region of character !' , realm = 'Realm of character' ,character_name = 'Character name of player !')
async def searching(interaction : discord.Interaction , region : str , realm : str , character_name : str) :
    
    region_t = region.title()

    realm_t = realm.title()

    character_name_t = character_name.title()

    warcraft_data = warcraft_api.request_person(region_t , realm_t , character_name_t)
    
    if warcraft_data.get_request() == True :
        
        embed = discord.Embed(title='Quick info :information_source:' ,description= 'Quick info of player that you searched !' , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow())

        embed_p = discord.Embed(title=f'Click here to go to player profile:information_source:' ,url=next(warcraft_data.get_url_profile()) , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=next(warcraft_data.get_banner_url()))

        embed.add_field(name='Name : ' , value=next(warcraft_data.get_name()))

        embed.add_field(name='Race :' , value=next(warcraft_data.get_race()))

        embed.add_field(name='Role' , value=next(warcraft_data.get_active_spec_role()))

        embed.add_field(name='Class :' , value=next(warcraft_data.get_class()))

        embed.add_field(name='Active Spec :' , value=next(warcraft_data.get_active_sepc_name()))

        embed.add_field(name='Total item score :' , value=next(warcraft_data.total_score_item()))

        await interaction.response.send_message(embeds=[embed_p , embed])

    else :

        await interaction.response.send_message('There is no player with this info or request has been failed !')

    pass



@bot.tree.command(name='search_mythic' , description='search for mythic score of player !')
@app_commands.describe(region = 'Region of character !' , realm = 'Realm of character' ,character_name = 'Character name of player !')
async def mythic_search(interaction : discord.Interaction , region : str , realm : str , character_name : str) :

    region_t = region.title()

    realm_t = realm.title()

    character_name_t = character_name.title()

    warcraft_data = warcraft_api.request_person(region_t , realm_t , character_name_t)
    
    if warcraft_data.get_request() == True :

        embed = discord.Embed(title='Mythic information of player :information_source:' ,description= 'Mythic score and class score of player !' , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow())

        embed_p = discord.Embed(title='Click here to go to player profile:information_source:' ,url=next(warcraft_data.get_url_profile()) , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=next(warcraft_data.get_banner_url()))

        embed.add_field(name='Name : ' , value=next(warcraft_data.get_name()))

        embed.add_field(name='Mythic score : ' , value=next(warcraft_data.mythic_scores()))

        embed.add_field(name='Mythic rank : ' , value=next(warcraft_data.mythic_rank()))

        await interaction.response.send_message(embeds=[embed_p , embed])

        pass

    pass



@bot.tree.command(name='search_item' , description='search for item level of player !')
@app_commands.describe(region = 'Region of character !' , realm = 'Realm of character' ,character_name = 'Character name of player !')
async def item_search(interaction : discord.Interaction , region : str , realm : str , character_name : str) :

    character_name_t = character_name.title()

    realm_t = realm.title()

    region_t = region.title()

    warcraft_data = warcraft_api.request_person(region_t , realm_t , character_name_t)

    if warcraft_data.get_request() == True :
    
        embed_url = discord.Embed(title='Click here to go to player profile:information_source:' , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow() , url=next(warcraft_data.get_url_profile()))

        embed = discord.Embed(title='Item information of player :information_source:' ,description= 'Item score and information of item of player !' , color=discord.Color.purple() , timestamp=datetime.datetime.utcnow())

        embed.set_thumbnail(url=next(warcraft_data.get_banner_url()))

        embed.add_field(name='Name : ' , value=next(warcraft_data.get_name()) , inline=False)

        embed_item = discord.Embed(title='Items : ' , description=next(warcraft_data.items()) , color=discord.Color.purple())

        await interaction.response.send_message(embeds=[embed_url , embed , embed_item])

        pass

    pass


@bot.tree.command(name="creator" , description="About my creator")
async def send_creator_info(interaction : discord.Interaction) :
    embed_info = discord.Embed(title='Info of my creator : ' , description= str('This bot created by nikan using python as first project with network and using and sorting collection of data for other usage \n it is some common bot with very short of usage if you found it interesting and wanna ask questin dm to me 1ironwill1#4147'))
    await interaction.response.send_message(embed=embed_info)
    pass


keep_alive()
bot.run(os.getenv('DISCORD_KEY'))