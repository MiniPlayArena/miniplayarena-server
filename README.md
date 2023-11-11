
### Game Interface :D

In order to have a player take a turn, get the data from the client and call game.take_turn
```
# some logic to get the data from the client..
game_state = current_game.take_turn(player_id, turn_data)
```
Where player_id is the index of the player in the game (I can change this to be client id etc)

take_turn returns JSON data containing the gamestate of the current game, which must then be sent back to the clients. Currently in the format
```
{
    "game-state": [
        ..game dependent information for player 0,
        ..game dependent information for player 1,
        etc
    ]
}
```

You can also get all the data a specific client should see using the function
```
current_game.get_client_data(client_id) # for one specific player
current_game.get_all_client_data() # for all players
```