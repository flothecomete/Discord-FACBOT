from typing import Optional
import discord
import log
from edt import EDT
import menu as mn

class DDLRestaurants(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180, log):
        super().__init__(timeout=timeout)
        self.log = log

    @discord.ui.select(
        placeholder = "Veuillez choisir un restaurant !",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="Le Lac",
                value="le-lac",
                description="Le restaurant Le Lac, situé non loin de la FAC DEG."
            ),
            discord.SelectOption(
                label="Le Borsalino",
                value="pizzeria-le-borsalino",
                description="La pizzeria Le Borsalino est au rez-de-chaussée du restaurant Le Lac."
            ),
            discord.SelectOption(
                label="Le Forum",
                value="le-forum",
                description="Le Forum se situe à côté du Cône de Radio Campus."
            ),
            discord.SelectOption(
                label="L'anatidé",
                value="lanatide",
                description="Le restaurant L'anatidé est à côté de la bibliothèque de Sciences."
            ),
            discord.SelectOption(
                label="Le Bistrot",
                value="le-bistrot",
                description="Le Bistrot de l'Étudiant est situé au rez-de-chaussée du Forum."
            ),
            discord.SelectOption(
                label="Le Café'bulle",
                value="cafebulle",
                description="Le Café'bulle se trouve dans Le Bouillon."
            )
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select):
        self.log.write("User " + interaction.user.name + " clicked on " + select.values[0] + " from " + interaction.guild.name + ".\n")
        menu = mn.screenshot(select.values[0])
        await interaction.response.send_message(content=menu, ephemeral=True)

class DDLEDT(discord.ui.View):
    def __init__(self, *, timeout: float | None = 180, log):
        super().__init__(timeout=timeout)
        self.log = log

    @discord.ui.select(
        placeholder = "Veuillez choisir votre formation !",
        min_values = 1,
        max_values = 1,
        options = [
            discord.SelectOption(
                label="L3 INFORMATIQUE",
                value="L3 INFORMATIQUE",
                description=""
            ),
            discord.SelectOption(
                label="L3 MIAGE",
                value="L3 MIAGE",
                description=""
            ),
            discord.SelectOption(
                label="L3 PHYSIQUE",
                value="L3 PHYSIQUE",
                description=""
            )
        ]
    )
    async def select_callback(self, interaction: discord.Interaction, select):
        self.log.write("User " + interaction.user.name + " clicked on " + select.values[0] + " from " + interaction.guild.name + ".\n")
        pass

