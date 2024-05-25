import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize bot:
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)

# Game State Variables:
game_active = False
current_player = '🟡'
board = []
longest = 0

def initialize_board():
    return [[' ' for _  in range(7)] for _ in range(6)]

def display_board():
    board_str = ''
    for row in board:
        board_str += '|'.join(row) + '\n'
    return board_str

# Check Endgame Logic:
def check_win():
    # Longest segment of any color is >=4:
    # Only need to check from the most recently placed circle.
    pass

def check_draw():
    # All spaces filled but not instance of 4 long segment:
    pass


# Gameplay Logic:
def make_move(column):
    #
    pass

def switch_player():
    global current_player
    current_player = '🔴' if current_player == '🟡' else '🟡'


@bot.command(name='startconnect4')
async def start_connect4(ctx):
    global game_active, current_player, board
    game_active = True
    current_player = '🟡'
    board = initialize_board()
    await ctx.send("New Connect 4 game started! Player 1's turn (🟡).")
    await ctx.send(display_board())

@bot.command(name='move')
async def move(ctx, column: int):
    global game_active
    if not game_active:
        await ctx.send("No active game. Start a new game with ?startconnect4.")
        return
    if column < 0 or column > 6:
        await ctx.send("Invalid column. Choose a column between 0 and 6.")
        return

    # Add logic to make move and update board.

    if check_win():
        await ctx.send(f"Player {current_player} wins!")
        game_active = False
    elif check_draw():
        await ctx.send("It's a draw!")
        game_active = False
    else:
        switch_player()
        await ctx.send(f"Player {current_player}'s turn.")
        await ctx.send(display_board())


# Function to create embed:
def create_embed(title, description, url=None, image_url=None):
    embed = discord.Embed(title=title, description=description)
    if url:
        embed.set_url(url)
    if image_url:
        embed.set_image(url=image_url)
    return embed

async def send_embed(ctx, title, description, url=None, image_url=None):
    embed = create_embed(title, description, url, image_url)
    channel = bot.get_channel(1243655198874796072) #TEMPORARY
    if channel:
        await channel.send(embed=embed)
    else:
        await ctx.send("Couldn't find the specified channel.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

# Run the bot:
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)