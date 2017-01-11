def generate_games_resp(request_user, games):
    client_games = []
    client_users = []
    for game in games:
        client_games.append(server_game_to_client(request_user, game))
        for player in game.players:
            if player.id != request_user.id:
                client_users.append(server_user_to_client(request_user, player))
    return {
        "games": client_games,
        "users": client_users,
    }

def server_user_to_client(request_user, user):
    ret = {
        "id": user.id,
        "name": user.name,
        "firstName": user.first_name,
        "lastName": user.last_name,
    }
    if user.id == request_user.id:
        ret["fbToken"] = user.fb_token
    return ret

def server_game_to_client(request_user, game):
    for player in game.players:
        if player.id != request_user.id:
            return {
                "id": game.id,
                "partnerId": player.id,
                "isCreator": game.creator_id == request_user.id,
                "rounds": [server_round_to_client(request_user, round)
                    for round in game.rounds]
            }

def server_round_to_client(request_user, round):
    return {
        "id": round.id,
        "word": round.word,
        "isCluer": round.cluer_id == request_user.id,
        "clues": round.clues,
        "guesses": round.guesses,
        "replayed": round.replayed,
        "updated": round.updated,
    }
