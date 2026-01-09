import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=";", intents=intents)

# ===== DADOS =====
dinheiro = {}
chance_cassino = 60
valor_receba = 999999999999999  # valor padrão do receba

@bot.event
async def on_ready():
    print(f"Bot ligado como {bot.user}")

# ===== CARTEIRA =====
@bot.command()
async def carteira(ctx):
    dinheiro.setdefault(ctx.author.id, 0)

    embed = discord.Embed(color=0x2ecc71)
    embed.description = (
        f"👤 **Usuário:** {ctx.author.mention}\n\n"
        f"💵 **Dinheiro:** R$ {dinheiro[ctx.author.id]}\n"
        f"🏦 **Banco:** R$ 0"
    )
    await ctx.send(embed=embed)

# ===== CASSINO =====
@bot.command()
async def cassino(ctx, aposta: int = 1):
    dinheiro.setdefault(ctx.author.id, 0)

    ganhou = random.randint(1, 100) <= chance_cassino

    if ganhou:
        dinheiro[ctx.author.id] += aposta
        resultado = "💰 **VOCÊ GANHOU!**"
    else:
        dinheiro[ctx.author.id] -= aposta
        resultado = "💸 **VOCÊ PERDEU!**"

    embed = discord.Embed(color=0xe74c3c)
    embed.description = (
        f"{resultado}\n\n"
        f"━━━━━━━━━━━━━━\n"
        f"💵 **Aposta:** `{aposta}`\n"
        f"😈 **O cassino venceu**\n"
        f"📊 **Chance:** `{chance_cassino}%`"
    )
    await ctx.send(embed=embed)

# ===== RECEBA (ADMIN) =====
@bot.command()
@commands.has_permissions(administrator=True)
async def receba(ctx, membro: discord.Member):
    dinheiro.setdefault(membro.id, 0)
    dinheiro[membro.id] += valor_receba

    embed = discord.Embed(color=0xf1c40f)
    embed.description = (
        f"💸 **DINHEIRO CONCEDIDO!**\n\n"
        f"👤 **Usuário:** {membro.mention}\n"
        f"💵 **Valor:** R$ {valor_receba}\n"
        f"🛡️ **Concedido por:** {ctx.author.mention}"
    )
    await ctx.send(embed=embed)

# ===== CONFIGURAR VALOR DO RECEBA =====
@bot.command()
@commands.has_permissions(administrator=True)
async def setreceba(ctx, valor: int):
    global valor_receba
    valor_receba = valor
    await ctx.send(f"⚙️ Valor do **;receba** definido para **R$ {valor}**")

# ===== TOKEN (PELO RENDER) =====
bot.run(os.getenv("TOKEN"))
