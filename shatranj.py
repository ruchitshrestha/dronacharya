#!/usr/bin/python3
import berserk
import chess
import chess.pgn
import chess.engine
import io
import os

API_TOKEN = open('personal_token','r').readline().strip()
# engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

# move_id = 2
# for game in games:
#     game = chess.pgn.read_game(io.StringIO(game))
#     print(move_id-1, game.headers["Site"])
#     move_id+=1
#     while not game.is_end():
#         break #LOL
#         #for each move record
#         game = game.variations[0]
#         move = game.san() #Last move
#         analysis = engine.analyse(game.board(), chess.engine.Limit(time=2))
#         move_num = move_id//2
#         move_str = "{}.".format(move_num) if move_id%2==0 else "{}...".format(move_num)
#         move_id+=1
#         print("{} {} | Analysis: {} | Depth: {} | EngineMove : {}".format(move_str, move, analysis['score'],analysis['depth'],analysis['pv'][0]))

    # engine.quit()

def produce_analysis():
    #WARNING: This takes a long time (predicted 12 hours)
    games = os.listdir('games')
    print(len(games))
    engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')
    if not os.path.exists('analysis'):
        os.makedirs('analysis')
    for game in games:
        game = chess.pgn.read_game(open('games/'+game,'r'))
        variant = game.headers['Variant']
        if variant!='Standard':
            continue
        identifier = game.headers['Site']
        identifier_tag = identifier.split('/')[-1]
        f_name = "analysis/game_{}".format(identifier_tag)

        with open(f_name, 'w') as f:
            f.write(identifier)
        engine.quit()
        break



def read_all_games(): #could take username + other parameters for export_by_player

    session = berserk.TokenSession(API_TOKEN)
    client = berserk.Client(session=session)
    games = client.games.export_by_player('chittyct', as_pgn=True)

    id = 1
    for game in games:
        with open('games/game_{}.json'.format(id), 'w') as f:
            f.write(str(game)+'\n')
            print('games/game_{}.json written'.format(id))
        id +=1

produce_analysis()

# def main():
#     # read_all_games()
#     pass
#
# if __name__=='__main__':
#     main()
