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
msg = None
current_player = '🟡'
board = []
player_list = []
recentPos = []
spaces_left = 42
reactions = {"1️⃣": 0, "2️⃣": 1, "3️⃣": 2, "4️⃣": 3, "5️⃣": 4, "6️⃣": 5, "7️⃣": 6}

# Need to add a method to allow ONLY two players to join:
def roster(author):
    global player_list
    if len(player_list) < 2:
        player_list.append(author)
    return

def initialize_board():
    b = [['⚪' for _ in range(7)] for _ in range(6)]
    b.append(['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣'])
    return b

def display_board():
    board_str = ''
    for row in board:
        board_str += '|'.join(row) + '\n'
    return board_str

# Check Endgame Logic:
def dfs(start):
    # Helper function/heuristic for check_win() method:
    #if length >= 4:
        #return True
    return False

def check_win(origin):
    # Longest segment of any color is >=4:
    # Only need to check from the most recently placed circle.
    if dfs(origin):
        return True
    return False

def check_draw():
    # All spaces filled but no instance of 4 long segment:
    global spaces_left
    if spaces_left <= 0:
        return True
    return False


# Gameplay Logic:
def make_move(column):
    global board, recentPos, spaces_left
    for row in range(len(board)-1, -1, -1):  # when we find empty space, place
        if board[row][column] == '⚪':
            if current_player == '🟡':
                board[row][column] = '🟡'
            else:
                board[row][column] = '🔴'
            recentPos = [row, column]
            spaces_left -= 1
            return True
    # Overflow detected:
    return False

def switch_player():
    global current_player
    current_player = '🔴' if current_player == '🟡' else '🟡'


@bot.command(name='start_connect4')
async def start_connect4(ctx):
    global game_active, current_player, board, msg
    game_active = True
    current_player = '🟡'
    board = initialize_board()
    description = f"{display_board()}\nNew Connect 4 game started! Player 1's turn (🟡)."
    msg = await send_embed(ctx=ctx, title='Connect4', description=description)

@bot.event
async def on_reaction_add(reaction, user):
    '''This function serves to make moves as specified by the player.'''
    if reaction.message.author == bot.user and user != bot.user:
        # Make move based on which emoji was reacted to:
        global game_active, player_list, msg, reactions, recentPos
        column = reactions[str(reaction)]
        ctx = reaction.message.channel
        if not game_active:
            await ctx.send("No active game. Start a new game with !start_connect4.")
            return
        if column < 0 or column > 6:
            description = "Invalid column. Choose a column between 0 and 6."
            await update_embed(msg, title='Connect4', description=description)
            return

        # Add logic to make move and update board.
        # Make call to make_move and check if column is full:
        if not make_move(column):
            description = f"{display_board()}\nPlayer {current_player} please choose a valid column."
            await update_embed(msg, title='Connect4', description=description)
            return
        else:
            switch_player()
            description = f"{display_board()}\nPlayer {current_player}'s turn."
            await update_embed(msg, title='Connect4', description=description)

        if check_win(recentPos):
            description = f"{display_board()}\nPlayer {current_player} wins!"
            await update_embed(msg, title='Connect4', description=description)
            game_active = False
            player_list = []
        elif check_draw():
            description = f"{display_board()}\nIt's a draw!"
            await update_embed(msg, title='Connect4', description=description)
            game_active = False
            player_list = []


# Functions to create, send, or edit embed:
def create_embed(title, description, url=None, image_url=None):
    embed = discord.Embed(title=title, description=description, color=color)
    if url:
        embed.set_url(url)
    if image_url:
        embed.set_image(url=image_url)
    return embed

async def send_embed(ctx, title, description, url=None, image_url=None):
    # Sends the initial embedded message (game board):
    embed = create_embed(title, description, url, image_url)
    message = await ctx.send(embed=embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")
    await message.add_reaction("6️⃣")
    await message.add_reaction("7️⃣")
    return message

async def update_embed(message, title, description, url=None, image_url=None):
    # Updates the game board to prevent message spamming:
    new_embed = discord.Embed(title=title, description=description, color=color)
    await message.edit(embed=new_embed)
    await message.add_reaction("1️⃣")
    await message.add_reaction("2️⃣")
    await message.add_reaction("3️⃣")
    await message.add_reaction("4️⃣")
    await message.add_reaction("5️⃣")
    await message.add_reaction("6️⃣")
    await message.add_reaction("7️⃣")

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