import threading

# Function used to process threads
import time

# Number of threads that has to be processed
processCount = 0

# Number of threads that has been processed per batch
count = 0

def processthread(color, numberofthreads, initprocessid):

    global processCount
    global count
    processCount = numberofthreads

    # Process threads
    if color == "Blue":
        for ctr1 in range(numberofthreads):
            blueThreads[ctr1+initprocessid].start()
            blueThreads[ctr1 + initprocessid].join()

    else:
        for ctr1 in range(numberofthreads):
            greenThreads[ctr1+initprocessid].start()
            greenThreads[ctr1 + initprocessid].join()

    count = 0

def dothread(color, processid):
    global count
    global processCount

    # When thread first enters room, print only allowed color
    if count == 0:
        print(color + " only")

    rooms.acquire()

    count = count + 1
    print(color + " #" + str(processid))

    rooms.release()

    # When final thread leaves fitting room, print empty fitting room
    if count == processCount:
        print("Empty fitting room\n")


# Main function
if __name__ == '__main__':

    # Input

    n = int(input("Number of slots inside fitting room: "))
    b = int(input("Number of blue threads "))
    g = int(input("Number of green threads "))


    # Initialize threads
    blueThreads = []
    greenThreads = []

    # Limits the amount of threads that can enter the fitting room
    rooms = threading.Semaphore(n)

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
    else:
        turn = False


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
                turn = False

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
                turn = True

