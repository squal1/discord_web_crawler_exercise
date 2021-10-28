import discord
import json
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import os
from core.classes import Cog_Extension
import datetime, asyncio

with open("setting.json", mode="r", encoding="utf8") as settingfile:
    settingdata = json.load(settingfile)


user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}


class Baha(Cog_Extension):
    def __init__(self, *args,**kwargs):
        # initialize the class again from super() (core.py)
        super().__init__(*args,**kwargs)

        async def update_latest_page_no():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(836112137599451156)
            while not self.bot.is_closed():

                ##Check if the page number is the latest one
                print("Checking if page number is the latest one.")
                response = requests.get(settingdata["vtuber_gosship"], headers=user_agent)
                soup = BeautifulSoup(response.text, "html.parser")
                article_total_page = soup.select_one('.BH-pagebtnA > a:last-of-type').text
                if settingdata["thread_max_page"] != article_total_page:
                    settingdata["thread_max_page"] = article_total_page
                    settingdata["vtuber_gosship"] = "https://forum.gamer.com.tw/C.php?page={}&bsn=60076&snA=5865232".format(article_total_page)
                    settingdata["article_count"] = "0"
                    print(f"New Page detected! Initializeed article count to 0 and updated page number to {article_total_page}")
                    with open("setting.json", mode='w', encoding="utf8") as settingfile:
                        json.dump(settingdata,settingfile, indent=4)
                print("Checking complete.")
                # wait after a cycle is finished
                await asyncio.sleep(300)

        async def print_content():
            await self.bot.wait_until_ready()
            self.channel = self.bot.get_channel(836112137599451156)
            while not self.bot.is_closed():

                response = requests.get(settingdata["vtuber_gosship"], headers=user_agent)
                soup = BeautifulSoup(response.text, "html.parser")
                content = []
                author = []
                img = []
                urls = []

                #find all atricle contents in a floor
                article_contents = soup.find_all("div", class_="c-article__content")
                for i in article_contents:
                    content.append(str(i.get_text()))

                #find authors
                article_authors = soup.find_all("a", class_="username")
                for i in article_authors:
                    author.append(str(i.get_text()))

                #find all 勇者頭像 in a floor
                images = soup.find_all("a",class_="c-user__avatar gamercard", limit=20)
                for image in images:
                    tmp = str(image.select("img"))
                    img.append(tmp)
                urls = [x[40:-36] for x in img]


                #if length of content != article_count 
                if str(len(content)) != settingdata["article_count"]:
                    
                    content_of_the_floor = content[int(settingdata["article_count"])]
                    author_of_the_floor = author[int(settingdata["article_count"])]
                    url_of_icon = urls[int(settingdata["article_count"])]
                    floor_number = int(settingdata["article_count"]) + ((int(settingdata["thread_max_page"]) -1)* 20)  + 1
                    print(f"Start printing article {floor_number}")

                    #output
                    embed=discord.Embed(color=0x00ffff)
                    embed.set_thumbnail(url=url_of_icon)
                    embed.add_field(name=f"\u200b{author_of_the_floor}", value=f"\u200b#{floor_number}", inline=False)
                    await self.channel.send(embed=embed)
                    await self.channel.send(f"{content_of_the_floor}** **" )
                    await self.channel.send("<------------------------------------------------------------------------>")
                    print("Article printed")

                    #article count + 1 and save in json file
                    settingdata["article_count"] = str(int(settingdata["article_count"])+1)   
                    with open("setting.json", mode='w', encoding="utf8") as settingfile:
                        json.dump(settingdata,settingfile, indent=4)
                

                await asyncio.sleep(20)


            
        
        self.background_task = self.bot.loop.create_task(update_latest_page_no())
        self.background_task2 = self.bot.loop.create_task(print_content())



    @commands.command()
    async def test(self,ctx):
        await ctx.send("Test")
        response = requests.get(settingdata["vtuber_gosship"], headers=user_agent)
        soup = BeautifulSoup(response.text, "html.parser")
        





def setup(bot):
    bot.add_cog(Baha(bot))