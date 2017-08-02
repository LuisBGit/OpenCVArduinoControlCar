
import nxt.bluesock # Make sure you remember this!

b = nxt.bluesock.BlueSock('001353033F50').connect()


motorLeft = nxt.Motor(b, nxt.PORT_C)

while 1:
    motorLeft.run(50) #nunber from -100 to 100
    time.sleep(.1)