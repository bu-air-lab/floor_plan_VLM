at(lab1, 0).
:- not at(water_fountain, n-1).    
                    
#minimize { L,X,Y,I: path(X,Y,I), cost(X,Y,L)}. 
                    
#show approach/2.
                    
#show gothrough/2.
                    
#show opendoor/2.
                    
#show goto/2.
                