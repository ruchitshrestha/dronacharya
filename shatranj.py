#!/usr/bin/python3.6
import berserk
import chess
import chess.pgn
import chess.engine
import io
import os
from concurrent.futures import ThreadPoolExecutor

API_TOKEN = open('personal_token','r').readline().strip()

def analysis_helper(games):
    engine = chess.engine.SimpleEngine.popen_uci('/usr/games/stockfish')

    for game in games:
        game = chess.pgn.read_game(open('games/'+game,'r'))
        variant = game.headers['Variant']
        if variant!='Standard':
            continue
        identifier = game.headers['Site']
        identifier_tag = identifier.split('/')[-1]
        f_name = "analysis/game_{}".format(identifier_tag)
        me = "white" if game.headers['White']=='chittyct' else "black"

        with open(f_name, 'w') as f:
            f.write("**URL: {} | Tag: {} | Side: {}**\n".format(identifier,identifier_tag, me))
            f.write("HEADERS: {}\n\n".format(str(game.headers)))
            move_id = 2
            while not game.is_end():
                game = game.variations[0]
                move = game.san()
                analysis = engine.analyse(game.board(), chess.engine.Limit(time=2))
                move_num = move_id//2
                move_str = "{}.".format(move_num) if move_id%2==0 else "{}...".format(move_num)
                move_id += 1
                try:
                    f.write("{} {} | Analysis: {} | Depth: {} | EngineMove : {}\n".format(move_str, move, analysis['score'],analysis['depth'],analysis['pv'][0]))
                except:
                    break

    engine.quit()


def produce_analysis():
    #WARNING: This takes a long time (predicted 12 hours)
    games = os.listdir('games')
    print('TOTAL GAMES' , len(games))
    if not os.path.exists('analysis'):
        os.makedirs('analysis')
    chunks = [games[x:x+500] for x in range(0, len(games), 500)]

    executer = ThreadPoolExecutor(max_workers=10)
    for games_sublist in chunks:
        executer.submit(analysis_helper,games_sublist)




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
#read_all_games()
# def main():
#     # read_all_games()
#     pass
#
# if __name__=='__main__':
#     main()
