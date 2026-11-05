import os
import discord

class BotClient(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Comandos de barra sincronizados.")

client = BotClient()

@client.event
async def on_ready():
    print(f'Conectado como {client.user}')

@client.tree.command(name="enviar", description="Envia uma mensagem formatada com imagem para um canal")
@app_commands.describe(
    canal="O canal onde a mensagem será enviada",
    mensagem="O texto que deseja enviar",
    imagem="A URL da imagem (opcional)"
)
async def enviar(
    interaction: discord.Interaction,
    canal: discord.TextChannel,
    mensagem: str,
    imagem: str = None
):
    await interaction.response.defer(thinking=True)
    
    embed = discord.Embed(description=mensagem, color=discord.Color.blue())
    if imagem:
        embed.set_image(url=imagem)
        
    try:
        await canal.send(embed=embed)
        await interaction.followup.send(f"Mensagem enviada com sucesso para {canal.mention}!", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Erro ao enviar mensagem: {e}", ephemeral=True)

client.run(os.getenv('DISCORD_TOKEN'))
