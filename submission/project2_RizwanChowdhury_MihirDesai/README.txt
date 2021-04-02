# CS352: Internet Technology - Project 2

0 - Rizwan Chowdhury (rzc2) and Mihir Desai (mvd67)

1. We implemented ls using non-blocking sockets and the "select" statement. The non-blocking sockets ensure request to one ts does not impede requests to another.
The "select" statement handles receiving the response from one of the servers and then timing out. We enabled the 5 second timeout by setting the timeout parameter
of the "select" method.

2. We have extensively tested our project. So far we did not find any errors and we hope it works fine when tested by the TAs.

3. We did not face any major significant problems. The only thing that challenged us was the load balancing part of the project it was tricky at first but we
looked into the hints provided in the instructions and settled on using the "select" method to resolve our issue. 

4. We learned how to connect to multiple sockets without blocking the connection to any one of them. Also while researching methods of resolving the multiple
connections issue we researched and learned a bit about python multi-threading.