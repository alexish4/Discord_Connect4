import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize bot:
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Color Object for embeddings:
color = discord.Color.from_rgb(114, 137, 218)

# Game State Variables:
game_active = False
current_player = '🟡'
board = []
player_list = []

# Need to add a method to allow ONLY two players to join:
def roster(author):
    global player_list
    if len(player_list) < 2:
        player_list.append(author)
    return

def initialize_board():
    return [[' ' for _ in range(7)] for _ in range(6)]

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
    global board
    for row_index in range(len(board)): #when we find empty space, place
        if board[row_index][column] == ' ':
            if current_player == '🟡':
                board[row_index][column] = '🟡'
            else:
                board[row_index][column] = '🔴'
            break
    pass

def switch_player():
    global current_player
    current_player = '🔴' if current_player == '🟡' else '🟡'


@bot.command(name='start_connect4')
async def start_connect4(ctx):
    global game_active, current_player, board
    game_active = True
    current_player = '🟡'
    board = initialize_board()
    await ctx.send("New Connect 4 game started! Player 1's turn (🟡).")
    await send_embed(ctx=ctx, title='Connect4', description=display_board())

@bot.command(name='move')
async def move(ctx, column: int):
    global game_active, player_list
    if not game_active:
        await ctx.send("No active game. Start a new game with !start_connect4.")
        return
    if column < 0 or column > 6:
        await ctx.send("Invalid column. Choose a column between 0 and 6.")
        return

    # Add logic to make move and update board.
    # Make call to make_move
    make_move(column)

    if check_win():
        await ctx.send(f"Player {current_player} wins!")
        game_active = False
        player_list = []
    elif check_draw():
        await ctx.send("It's a draw!")
        game_active = False
        player_list = []
    else:
        switch_player()
        await ctx.send(f"Player {current_player}'s turn.")
        await send_embed(ctx=ctx, title='Connect4', description=display_board())


# Function to create embed:
def create_embed(title, description, url=None, image_url=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if url:
        embed.set_url(url)
    if image_url:
        embed.set_image(url=image_url)
    return embed

async def send_embed(ctx, title, description, url=None, image_url=None):
    embed = create_embed(title, description, url, image_url)
    channel = ctx.channel
    if channel:
        await channel.send(embed=embed)
    else:
        await ctx.send("Couldn't find the specified channel.")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself:
    if message.author == bot.user:
        return

    # Get author's ID:
    author_id = message.author.id

    # Add author to roster if message is "Dibs":
    if message.content == "Dibs":
        roster(author_id)

    # Ensure that the bot processes incoming messages:
    await bot.process_commands(message)

# Run the bot:
TOKEN = os.getenv("TOKEN")
bot.run(TOKEN)