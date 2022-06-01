import threading

# Function used to process threads
import time


def processthread(color, numberofthreads, initprocessid):
    # Process threads
    if color == "Blue":
        for ctr1 in range(numberofthreads):
            blueThreads[ctr1+initprocessid].start()
            blueThreads[ctr1 + initprocessid].join()
            #lock.release()
            #print(color + " #" + str(initprocessid+ctr1))

    else:
        for ctr1 in range(numberofthreads):
            greenThreads[ctr1+initprocessid].start()
            greenThreads[ctr1 + initprocessid].join()
            #lock.release()
            #print(color + " #" + str(initprocessid+ctr1))


def dothread(color, processid):
    lock.acquire()
    print(color + " #" + str(processid))
    lock.release()


# Main function
if __name__ == '__main__':

    # Input

    n = int(input("Number of slots inside fitting room: "))
    b = int(input("Number of blue threads "))
    g = int(input("Number of green threads "))


    # Initialize threads
    blueThreads = []
    greenThreads = []
    lock = threading.Lock()

    for ctr in range(b):
        blueThreads.append(threading.Thread(target=dothread, args=["Blue", ctr]))

    for ctr in range(g):
        greenThreads.append(threading.Thread(target=dothread, args=["Green", ctr]))


    print("\n")
    processedBlue = 0
    processedGreen = 0

    # Prioritize color with more amount of threads
    if b >= g:
        turn = True
        print("Blue only")
    else:
        turn = False
        print("Green only")


    # While there are still threads remaining to be processed
    while(b + g > 0):

        # This if and else statement ensures that threads being processed does not exceed the capacity of the fitting room
        if(turn):

            # Process b number of threads if they all fit in the fitting room
            if(b <= n):
                processthread("Blue", b, processedBlue)
                processedBlue += b
                b -= b

            # Process n number of blue threads only so that the threads being processed does not exceed the capacity of the fitting room
            else:
                processthread("Blue", n, processedBlue)
                processedBlue += n
                b -= n

            # Pass the lock to green threads if there are still green threads remaining
            # This is to avoid starvation
            if(g > 0):

                # Print empty fitting room. Will only switch once fitting room is empty.
                print("Empty fitting room\n")
                turn = False
                # Print only allowed thread color
                print("Green only")

        # This if and else statement ensures that threads being processed does not exceed the capacity of the fitting room
        else:

            # Process g number of threads if they all fit in the fitting room
            if (g <= n):
                processthread("Green", g, processedGreen)
                processedGreen += g
                g -= g

            # Process n number of green threads only so that the threads being processed does not exceed the capacity of the fitting room
            else:
                processthread("Green", n, processedGreen)
                processedGreen += n
                g -= n

            # Pass the lock to blue threads if there are still blue threads remaining
            # This is to avoid starvation
            if (b > 0):
                # Print empty fitting room. Will only switch once fitting room is empty.
                print("Empty fitting room\n")
                turn = True
                # Print only allowed thread color
                print("Blue only")

    # Print final empty fitting room when done processing all threads
    print("Empty fitting room")
    #processthread("Blue", 3, 5)
