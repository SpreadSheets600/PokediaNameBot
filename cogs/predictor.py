import re
import discord
from discord.ext import commands
from utilities.solver import solve_hint
from utilities.identify import predict_pokemon_from_url


class SpawnPredictor(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(message)

        if message.author.id == 727012870683885578:
            print("Message Received!")

            if "Here's your hint".lower() in message.content.lower():
                match = re.search(
                    r"here's your hint:\s*`(.+?)`",
                    message.content.lower(),
                    re.IGNORECASE,
                )

                if match:
                    hint_pattern = match.group(1)
                    matches = solve_hint(hint_pattern)
                    if matches:
                        response = f"🧩 Possible Pokémon: {', '.join(matches)}"

                    embed = discord.Embed(
                        title="🧩 Pokémon Hint Solve",
                        description=f"### Possible Matches :\n {'\n'.join(matches)}",
                        color=0xffca7b,
                    )

                    await message.reply(embed=embed, mention_author=False)

            elif message.embeds:
                if (
                    message.embeds[0].title
                    and "wild" in message.embeds[0].title.lower()
                ):
                    print("[ + ] A Pokémon Spawned - Attempting To Predict")

                    image_url = message.embeds[0].image.url

                    predictions = await predict_pokemon_from_url(image_url)
                    top_prediction = max(predictions, key=lambda x: x[1])

                    name = top_prediction[0]
                    score = top_prediction[1]

                    embed = discord.Embed(
                        title="🔮 Pokémon Prediction",
                        description=f"### Predicted Pokémon : {name}",
                        color=0xffca7b,
                    )

                    await message.reply(embed=embed, mention_author=False)


def setup(bot):
    bot.add_cog(SpawnPredictor(bot))
