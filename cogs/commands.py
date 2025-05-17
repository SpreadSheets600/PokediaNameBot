import discord
from discord.ext import bridge, commands
from utilities.identify import predict_pokemon_from_url
from utilities.predict import extract_pokemon_name, get_pokemon_sprite_name

class CommandsCOG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command(
        name="predict",
        description="Predict Pokémon From Image URL Or Attachment",
    )
    async def predict(self, ctx, image_url: str = None):
        await ctx.defer()

        image = ctx.message.attachments[0] if ctx.message.attachments else None

        if image_url:
            name = extract_pokemon_name(image_url)
            if not name:
                predictions = await predict_pokemon_from_url(image_url)
                top_prediction = max(predictions, key=lambda x: x[1])
                name, score = top_prediction
            else:
                score = None

        elif image:
            if not image.content_type or not image.content_type.startswith("image/"):
                await ctx.reply("Attachment Not An Image!", ephemeral=True)
                return

            predictions = await predict_pokemon_from_url(image.url)
            top_prediction = max(predictions, key=lambda x: x[1])
            name, score = top_prediction

        else:
            await ctx.reply(
                "Please Provide An Image URL Or Attach An Image!", ephemeral=True
            )
            return

        sprite = get_pokemon_sprite_name(name)

        embed = discord.Embed(
            title="🔮 Pokémon Prediction",
            description=f"##  Pokémon : {name.capitalize()}",
            color=0xFFCA7B,
        )

        if sprite:
            embed.set_thumbnail(url=sprite)

        embed.set_footer(text="AI Prediction May Not Be Accurate")

        await ctx.reply(embed=embed)

def setup(bot):
    bot.add_cog(CommandsCOG(bot))
