import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.io">https://docs.battlesnake.io</a>.
    '''

@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')

@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()

@bottle.post('/start')
def start():
    data = bottle.request.json

    """
    TODO: If you intend to have a stateful snake AI,
            initialize your snake state here using the
            request's data if necessary.
    """
    #print(json.dumps(data))

    color = "#8935B9"

    return start_response(color)


@bottle.post('/move')
def move():
    data = bottle.request.json

    print(json.dumps(data))
  
    def check_border(width, height, head, directions):
        # dont is the list of other snakes and my own body
        # head is the head of my snake 
        # direction is the optimal direction that is to be validated
        # directions are the possible directions. Pop from this list if a move is invalid

         # 1. check if head is at a border and pop invalid directions (one of the coords is 0 or 14)
        if 0 in head:
            if head.index(0) == 0:
                print 'dont go left'
                directions.remove('left')
                print 'directions list', directions
            else: print 'can move left'
            if head.index(0) == 1:
                print 'dont go up'
                directions.remove('up')
                print 'directions list', directions
            else: 'can move up'

''' change 14 to width/height from data '''
        if width in head: 
            if head.index(width) == 0:
                print 'dont go right'
                directions.remove('right')
                print 'directions list', directions
            #else: print 'can move right'
            if head.index(width) == 1:
                print 'dont go down'
                directions.remove('down')
                print 'directions list', directions
            else: print 'can move down'

        return directions

        #check if direction is in directions list 
    
    def check_next_pos(direc, dont, head, directions):
        next_pos = [sum(x) for x in zip(head, direc)]
        print 'next position', next_pos
        if next_pos in dont:
            print 'dont go here'
            return False
        else: 
            print 'go here'
            return True

    def vec_to_word(direction):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]

        if direction == up:
            return 'up'
        if direction == down:
            return 'down'
        if direction == left:
            return 'left'
        if direction == right:
            return 'right'

    def word_to_vec(direction):
        up = [0, -1]
        down = [0, 1]
        left = [-1, 0]
        right = [1, 0]

        if direction == 'up':
            return up
        if direction == 'down':
            return down
        if direction == 'left':
            return left
        if direction == 'right':
            return right

    width = data['board']['width']
    height = data['board']['height']


    directions = ['up', 'down', 'left', 'right']
    direction = 'up'

    print 'turn ', data['turn']

    # add board boundaries to the list of places not to go
    # dont is a list of 2 element lists 
    # xaxis = []
    # yaxis = []
    dont = []

    # my snake head location
    head = [int(data["you"]["body"][0]["x"]), int(data["you"]["body"][0]["y"])]
    #print 'Head', head

    # grow the list of coordinates not to go
    # populate the list with snakes on the board including myself
    # differentiate between me and others??
    # save the head/tail location to see where they are moving??
    for i in data["board"]["snakes"]:
        for j in i['body']:
            pos = [j['x'],j['y']]
            dont.append(pos)
    print dont, 'DONT'
    
    # food location
    # change to make this the closest food!!
    food = [data["board"]["food"][0]["x"], data["board"]["food"][0]["y"]]

    #make a closest food function
    #order the directions based on priority

    # find food direction 
    negfood = [-x for x in food]
    dist = [sum(x) for x in zip(head, negfood)] # only picks first food in data
    #print 'distance x,y', dist 
    # return index of max(dist) to decide x or y move
    distabs = [abs(x) for x in dist]
    #print distabs
    ind = distabs.index(max(distabs))
    #print 'index', ind

    direc = [0, 0] # direction vector
    # set the direction vector 
    if dist[ind] < 0:
        direc[ind] = 1
    else: direc[ind] = -1
    #print 'direction vector', direc # pass direc to checkdir function

    # calling check border returns directions with invalid directions removed 
    directions = check_border(width, height, head, directions)
    print 'directions list after check_border()', directions

    while len(directions) != 0:
        isValid = check_next_pos(direc, dont, head, directions)
        
        if isValid == True:
            print 'position is valid'
            validDir = direc
            direction = vec_to_word(validDir)
            print 'direction ', direction
            return move_response(direction)
        
        invalidDir = vec_to_word(direc)
        print 'invalidDir', invalidDir
        print 'directions list', directions
        directions.remove(invalidDir)
        # change the direction vector to something else 
        direc = word_to_vec(directions[0])




@bottle.post('/end')
def end():
    data = bottle.request.json

    """
    TODO: If your snake AI was stateful,
        clean up any stateful objects here.
    """
    #print(json.dumps(data))

    return end_response()

# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )


