import socket
import sys
from threading import Thread
from SocketServer import ThreadingMixIn
import psycopg2
import pickle

#Multithreaded Python server : TCP Server Socket Thread Pool

class ClientThread(Thread):
        def __init__(self, ip, port):
                Thread.__init__(self)
                self.ip = ip
                self.port = port
                print("New server socket thread started for ", ip, ":", str(port))
        def run(self):
                while True:
                        data = conn.recv(2048)
                        print("Server receives data", data)
                        if data == 'menu':
                                MESSAGE = "1.Sign up\n2.Log in\n"
                        elif data == '1':
                                MESSAGE = "Enter username and password separated by a space."
                                conn.send(MESSAGE)
                                userpass = conn.recv(2048)
                                username, password = userpass.split(" ")
                                #print "Username is" + username
                                #print "Password is" + password
                                dbconn = psycopg2.connect(database="cn", user = "postgres", password = "compnet", host = "127.0.0.1", port = "5432")
                                cur = dbconn.cursor()
                                #cur.execute("select waiting from train where train_name = 'Shatabdi Express'")
                                cur.execute("insert into customer (username, passwd) values('"+username+"','"+password+"');")
                                cur.execute("select * from customer")
                                rows = cur.fetchall()
                                print rows
                                dbconn.commit()
                                dbconn.close()
                                MESSAGE = "Signed you up"
                                
                        elif data == '2':
                                MESSAGE = "\nEnter username and password separated by a space.\n"
                                print"\nserver sending\n"
                                conn.send(MESSAGE)
                                
                                userpass = conn.recv(2048)
                                username, password = userpass.split(" ");
                                dbconn = psycopg2.connect(database="cn", user = "postgres", password = "compnet", host = "127.0.0.1", port = "5432")
                                cur = dbconn.cursor()
                                cur.execute("select username from customer where username = '"+username+"'and passwd = '"+password+"';")
                                usercheck = cur.fetchone()
                                print usercheck
                                #if usercheck is not None, sign in. Show new menu for functions, option to log out
                                if usercheck == None:
                                        MESSAGE = "Login failed."
                                else:
                            		MESSAGE = "Login successful\nWELCOME Mr "+usercheck[0]+"!\n\n1.Reserve a seat\n2.Seats available\n3.Cancel reservation\n4.Waiting list\n5.Train from A to B\n6.My details\n7.Generate ticket\n8.Cost of journey\n9.Log out\n"
                            		#print"\nserver sending\n"
                            		conn.send(MESSAGE)                       		
                            		#print"\nserver sent\n"
                            		logout_flag = 0;
                                        while logout_flag == 0:
                            		        data2 = conn.recv(2048)
                            		        print("Server receives data", data2)
                            		        if data2 == '1':
                            		                MESSAGE = "\nEnter the train you want a seat on.\n"
                            		                conn.send(MESSAGE)
                            		                tname = conn.recv(2048)
                            		                cur = dbconn.cursor()
                            		                cur.execute("select seats_avail from train where train_name = '"+tname+"';")
                            		                num_free = cur.fetchone()
                            		                num_free = num_free[0]
                            		                print("num_free is", num_free)
                            		                if num_free == 0:
                            		                        print("No free seats")
                            		                        MESSAGE = "You have been waitlisted.\n"
                            		                        cur.execute("update train set waiting = waiting + 1 where train_name = '"+tname+"';")
                            		                        cur.execute("update customer set train_id_waiting = (select train_id from train where train_name = '"+tname+"') where username = '"+usercheck[0]+"';")
                            		                        
                            		                        
                    		                        elif num_free > 0:
                    		                                MESSAGE = "You have been allocated a seat!\n"
                    		                                cur.execute("update train set seats_avail = seats_avail - 1 where train_name = '"+tname+"';")
                    		                                cur.execute("update customer set train_id_got = (select train_id from train where train_name = '"+tname+"') where username = '"+usercheck[0]+"';")

                            		        #display list of trains along with their number of seats available.train_name seats_avail
                            		        elif data2 == '2':
                            		                MESSAGE = "\nEnter the name of the train you want the available seats for.\n"
                            		                conn.send(MESSAGE)
                            		                tname = conn.recv(2048)
                            		                print("The train name is ", tname)
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select seats_avail from train where train_name = '"+tname+"';")
                            		        	t_list = cur.fetchone()
                            		        	print("The number of available seats is ",t_list[0])
                            		        	MESSAGE = "The number of available seats is " + str(t_list[0])
                            		        	
                            		        elif data2 == '3':
                            		                MESSAGE = "\nEnter the train you want to cancel your waiting/reservation for.\n"
                            		                conn.send(MESSAGE)
                            		                tname = conn.recv(2048)
                            		                cur = dbconn.cursor()
                            		                cur.execute("select train_id_waiting from customer where username = '"+usercheck[0]+"';")
                            		                waiting = cur.fetchone()
                            		                cur.execute("select train_id_got from customer where username = '"+usercheck[0]+"';")
                            		                got = cur.fetchone()
                            		                cur.execute("select train_id from train where train_name = '"+tname+"';")
                            		                tid = cur.fetchone()
                    		                        if(tid[0] == waiting[0]):
                    		                                MESSAGE = "You have been removed from the wait list.\n"
                    		                                cur.execute("update train set waiting = waiting - 1 where train_name = '"+tname+"';")
                    		                                cur.execute("update customer set train_id_waiting = NULL where username = '"+usercheck[0]+"';")
                    		                                
                    		                                
            		                                elif(tid[0] == got[0]):                                                   
                    		                                MESSAGE = "Your reservation has been removed.\n"
                    		                                cur.execute("update train set seats_avail = seats_avail + 1 where train_name = '"+tname+"';")
                    		                                cur.execute("update customer set train_id_got = NULL where username = '"+usercheck[0]+"';")
                            		        	
                            		        	
                            		        elif data2 == '4':
                            		                MESSAGE = "\nEnter the name of the train you want the waiting list for.\n"
                            		                conn.send(MESSAGE)
                            		                tname = conn.recv(2048)
                            		                print("The train name is ", tname)
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select waiting from train where train_name = '"+tname+"';")
                            		        	t_list = cur.fetchone()
                            		        	print("The number of people waiting is ",t_list[0])
                            		        	MESSAGE = "The number of people waiting is " + str(t_list[0])         
                            		        	
                            		        elif data2 == '5':
                            		                MESSAGE = "\nEnter the starting point and destination separated by a space.\n"
                            		                conn.send(MESSAGE)
                            		                tnames = conn.recv(2048)
                            		                start, dest = tnames.split(" ")
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select train_name, arr_time, dep_time from train where from_place = '"+start+"'and to_place = '"+dest+"';")
                            		        	t_list = cur.fetchone()
                            		        	print(t_list)
                            		        	MESSAGE = "\nThe train is "+t_list[0]+", arriving at " + str(t_list[1]) + " and leaving at " + str(t_list[2]) + "\n"                           		        	
                            		        	 
                            		        	 
                            		        elif data2 == '6':
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select username, train_id_got, train_id_waiting from customer where username = '"+usercheck[0]+"';")
                            		        	t_list = cur.fetchone()
                            		        	MESSAGE = "\nYour username is "+t_list[0]+", the train you have reserved a seat on is " + str(t_list[1]) + " and the one you are waiting for is " + str(t_list[2]) + "\n"        
                                                 		        	  
                                                 		        	  
                            		        elif data2 == '7':
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select username, train_id_got from customer where username = '"+usercheck[0]+"';")
                            		        	cust_stuff = cur.fetchone()
                            		        	#cust_stuff[1] is train_id_got
                            		        	cur.execute("select train_name, from_place, to_place, arr_time, dep_time, cost from train where train_id = '"+str(cust_stuff[1])+"';")
                            		        	
                            		        	train_stuff = cur.fetchone()
                            		        	MESSAGE = "\nTICKET\nName: " + cust_stuff[0] + "\nTrain ID: " + str(cust_stuff[1]) + "\nTrain Name: " + train_stuff[0] + "\nFrom: " + train_stuff[1] + "\nTo: " + train_stuff[2] + "\nArrival Time: " + str(train_stuff[3]) + "\nDeparture Time: " + str(train_stuff[4]) + "\nCost: " + str(train_stuff[5]) + "\n";                                                  		        	  
                                                 		        	  
                                                 		        	  
                            		        	
                            		        elif data2 == '8':
                            		                MESSAGE = "\nEnter the name of the train you want the cost for.\n"
                            		                conn.send(MESSAGE)
                            		                tname = conn.recv(2048)
                            		                print("The train name is ", tname)
                            		        	cur = dbconn.cursor()
                            		        	cur.execute("select cost from train where train_name = '"+tname+"';")
                            		        	t_list = cur.fetchone()
                            		        	print("The cost is ",t_list[0])
                            		        	MESSAGE = "The cost is " + str(t_list[0])                            		        	                 		        
                            		        	
                    		                elif data2 == '9': #log out
                    		                        print("Logout option selected.")
                    		                        logout_flag = 1
                    		                        
                            		        else:#maybe elif data2 == 'menu'
                            		                MESSAGE = "\n1.Reserve a seat\n2.Seats available\n3.Cancel reservation\n4.Waiting list\n5.Train from A to B\n6.My details\n7.Generate ticket\n8.Cost of journey\n9.Log out\n"
                            		                
                            		                
                                                print("The logout flag is currently", logout_flag)
            		                        if logout_flag == 0:
            		                                conn.send(MESSAGE)
    		                                else:
    		                                        MESSAGE = "1. Sign up\n2. Log in\n"
    		                                        
    		                                        break
                                dbconn.commit()
                                dbconn.close()                    
                                                                
                        else:
                                MESSAGE = raw_input("Multithreaded Python server : Enter response from server/Enter exit:")
                        
                        if MESSAGE == 'exit':#not entering block
                                tcpServer.close()
                                sys.exit()
                        #print"\nserver sending again\n"
                        conn.send(MESSAGE)
                        #print"\nserver sent again\n"

#Multithreaded Python server : TCP server socket program stub
TCP_IP = '0.0.0.0'
TCP_PORT = 2008
BUFFER_SIZE = 20 #usually 1024, but we need quick response

tcpServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpServer.bind((TCP_IP, TCP_PORT))
threads = []

while True:
        tcpServer.listen(4)
        print("Multithreaded Python server : Waiting for connections from TCP clients...")
        (conn, (ip,port)) = tcpServer.accept()
        newthread = ClientThread(ip,port)
        newthread.start()
        threads.append(newthread)
        
for t in threads:
        t.join() #end


