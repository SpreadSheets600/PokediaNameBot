import discord
from discord.ext import bridge, commands
from utilities.predict import extract_pokemon_name
from utilities.identify import predict_pokemon_from_url


class CommandsCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(
        name="predict",
        description="Predict Pokémon From Image URL Or Attachment",
    )
    async def predict(
        self,
        ctx,
        image_url: str = None,
        image: discord.Attachment = None,
    ):
        await ctx.defer()

        if image_url:
            name = await extract_pokemon_name(image_url)
            if not name:
                predictions = await predict_pokemon_from_url(image_url)
                if not predictions:
                    await ctx.reply("Could Not Identify The Pokémon!", ephemeral=True)
                    return
                top_prediction = max(predictions, key=lambda x: x[1])
                name, score = top_prediction
            else:
                score = None

        elif image:
            if not image.content_type or not image.content_type.startswith("image/"):
                await ctx.reply("Attachment Not An Image!", ephemeral=True)
                return

            predictions = await predict_pokemon_from_url(image.url)
            if not predictions:
                await ctx.reply("Could Not Identify The Pokémon!", ephemeral=True)
                return
            top_prediction = max(predictions, key=lambda x: x[1])
            name, score = top_prediction

        else:
            await ctx.reply(
                "Please Provide An Iage URL Or Attach An Image!", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="🔮 Pokémon Prediction",
            description=f"### Predicted Pokémon : {name}",
            color=0xFFCA7B,
        )
        embed.set_footer(text="AI Prediction May Not Be Accurate")

        await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(CommandsCOG(bot))
