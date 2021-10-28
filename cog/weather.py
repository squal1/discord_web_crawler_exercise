import discord
import json
import requests
from bs4 import BeautifulSoup
from discord.ext import commands
import os
from core.classes import Cog_Extension
import datetime


with open("setting.json", mode="r", encoding="utf8") as settingfile:
    settingdata = json.load(settingfile)


class Weather(Cog_Extension):

    @commands.command()
    async def now(self,ctx):
        response = requests.get(settingdata["weather_website"])
        soup = BeautifulSoup(response.text, "html.parser")

        # Reply the temperature, weather and current time in Sacramento
        temp = soup.find("span", class_="CurrentConditions--tempValue--3KcTQ").text
        weather = soup.find(class_="CurrentConditions--phraseValue--2xXSr").text
        chance_of_rain = soup.find(class_="CurrentConditions--precipValue--RBVJT").text
        air_quality_index = soup.find(class_="DonutChart--innerValue--k2Z7I").text
        air_quality = soup.find(class_="AirQualityText--severity--1VMr2").text
        humidity = soup.find("span", attrs={"data-testid":"PercentageValue"}).text

        embed=discord.Embed(title=datetime.datetime.utcnow(), color=0x0000ff)
        embed=discord.Embed(title="The weather information right now", url="https://weather.com/weather/today/l/d1be3e5aec1726d0df2d6c19f21655d886415ee60ff0e8f14afe8ff7f57c9e5d", color=0x0000ff, timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AAUvwnjOKMevYpP-kLQt6EijiCfE2NCZSgiSw8jdO5nplcg=s900-c-k-c0x00ffffff-no-rj")
        embed.add_field(name="Temperature", value=temp, inline=True)
        embed.add_field(name="Weather", value=weather, inline=True)
        embed.add_field(name="Humidity", value=humidity, inline=True)
        embed.add_field(name="Air Quality", value=f"{air_quality_index} {air_quality}", inline=True)
        embed.add_field(name="Chance of Rain", value=chance_of_rain, inline=True)
        await ctx.send(embed=embed)


    @commands.command()
    async def five_days(self,ctx):
        response2 = requests.get(settingdata["weather_website2"])
        soup2 = BeautifulSoup(response2.text, "html.parser")
        date_of_next_5days = []
        max_temp_data_5days = []
        min_temp_data_5days = []
        weather_5days = []

        # Reply the temperature in next five days
        Today_temp = soup2.find("span", class_="DailyContent--temp--_8DL5").text
        date = soup2.find_all(class_="DetailsSummary--daypartName--1Mebr", limit = 6)
        for i in date:
            date_of_next_5days.append(str(i.get_text()))
        #date_of_next_5_days[X]] represent the date of X days after
        max_temperature = soup2.find_all(class_="DetailsSummary--highTempValue--3x6cL", limit = 6)
        for i in max_temperature:
            max_temp_data_5days.append(str(i.get_text()))
        #temp_data_5days[X]] represent the temp X days after
        min_temperature = soup2.find_all(class_="DetailsSummary--lowTempValue--1DlJK", limit = 6)
        for i in min_temperature:
            min_temp_data_5days.append(str(i.get_text()))
        weather = soup2.find_all(class_="DetailsSummary--extendedData--aaFeV", limit = 12)
        for i in weather:
            weather_5days.append(str(i.get_text()))

        embed=discord.Embed(title="Weather in 5 days", url="https://weather.com/weather/tenday/l/d1be3e5aec1726d0df2d6c19f21655d886415ee60ff0e8f14afe8ff7f57c9e5d#detailIndex5", color=0x0000ff, timestamp = datetime.datetime.utcnow())
        embed.set_thumbnail(url="https://yt3.ggpht.com/ytc/AAUvwnjOKMevYpP-kLQt6EijiCfE2NCZSgiSw8jdO5nplcg=s900-c-k-c0x00ffffff-no-rj")
        embed.add_field(name=date_of_next_5days[1], value=f"{max_temp_data_5days[1]}/{min_temp_data_5days[1]}\u200b\u200b{weather_5days[2]}", inline=False)
        embed.add_field(name=date_of_next_5days[2], value=f"{max_temp_data_5days[2]}/{min_temp_data_5days[2]}\u200b\u200b{weather_5days[4]}", inline=False)
        embed.add_field(name=date_of_next_5days[3], value=f"{max_temp_data_5days[3]}/{min_temp_data_5days[3]}\u200b\u200b{weather_5days[6]}", inline=False)
        embed.add_field(name=date_of_next_5days[4], value=f"{max_temp_data_5days[4]}/{min_temp_data_5days[4]}\u200b\u200b{weather_5days[8]}", inline=False)
        embed.add_field(name=date_of_next_5days[5], value=f"{max_temp_data_5days[5]}/{min_temp_data_5days[5]}\u200b\u200b{weather_5days[10]}", inline=False)
        await ctx.send(embed=embed)





def setup(bot):
    bot.add_cog(Weather(bot))