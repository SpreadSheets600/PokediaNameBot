import re
import discord
from discord.ext import commands
from utilities.solver import solve_hint
from utilities.identify import predict_pokemon_from_url
from utilities.collector import get_collectors_for_pokemon
from utilities.predict import extract_pokemon_name, get_pokemon_sprite_url


class PredictorCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.id == 1338124574583427092:
            print("Message Received!")

            if "That's not the correct Pokémon! Guess the Pokémon correctly!".lower() in message.content.lower():
                embed = discord.Embed(
                    title = "Wrong Pokémon",
                    description="## Pokémon Is Wrong! Please Use `p!h` To Get Hints.",
                    color=0xFFCA7B,
                )

                await message.reply(embed=embed, mention_author=False)

            elif "Here's your hint".lower() in message.content.lower():
                match = re.search(
                    r"here's your hint:\s*`(.+?)`",
                    message.content.lower(),
                    re.IGNORECASE,
                )

                if match:
                    hint_pattern = match.group(1)
                    matches = solve_hint(hint_pattern)

                    if matches:
                        embed = discord.Embed(
                            title="🧩 Pokémon Hint Solve",
                            description=f"## Possible Matches :\n {'\n'.join(matches)}",
                            color=0xFFCA7B,
                        )

                        await message.reply(embed=embed, mention_author=False)

                    else:
                        embed = discord.Embed(
                            title="🧩 Pokémon Hint Solve",
                            description=f"### Unable To Solve Hint!",
                            color=0xFFCA7B,
                        )

                        await message.reply(embed=embed, mention_author=False)

            elif message.embeds:
                if (
                        message.embeds
                        and message.embeds[0].title
                        and "wild" in message.embeds[0].title.lower()
                    ):
                        print("[ + ] A Pokémon Spawned - Attempting To Predict")

                        image_url = message.embeds[0].image.url

                        name = extract_pokemon_name(image_url)
                        sprite = get_pokemon_sprite_url(image_url)

                        if not name:
                            predictions = await predict_pokemon_from_url(image_url)
                            top_prediction = max(predictions, key=lambda x: x[1])
                            name, score = top_prediction

                        embed = discord.Embed(
                            title="🔮 Pokémon Prediction",
                            description=f"## Pokémon : {name.capitalize()}",
                            color=0xFFCA7B,
                        )
                        embed.set_thumbnail(url=sprite)
                        embed.set_footer(text="AI Prediction May Not Be Accurate")

                        user_ids = get_collectors_for_pokemon(name)

                        if user_ids:
                            mentions = []
                            for user_id in user_ids:
                                try:
                                    mentions.append(f"<@{user_id}>")
                                except Exception as e:
                                    print(f"Failed to fetch user {user_id}: {e}")

                            mention_text = "### 🐾 This Pokémon Is On Your Collection List!\n" + ", ".join(mentions)
                        else:
                            mention_text = ""

                        await message.reply(
                            content=mention_text if mention_text else None,
                            embed=embed,
                            mention_author=False
                        )


def setup(bot):
    bot.add_cog(PredictorCOG(bot))
