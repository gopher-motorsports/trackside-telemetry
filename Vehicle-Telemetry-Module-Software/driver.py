import TracksideLogger as tl

logr = tl.TracksideLogger()

def print_formatted(string):
    white = '\33[107m'
    black = '\33[30m'
    bold = '\33[1m'
    str1 = white + black + bold + string +'\33[0m'
    print(str1)

while True:
    try:
        frame = logr.read() # bytes object - raw
        frame = str(frame)
        
        print("Recieved Data!")
        print(frame)
        print("\n")
        
    except:
        print("\n")
        print_formatted("SHUTTING DOWN INTERNALS...")
        
        del logr
        break
    
