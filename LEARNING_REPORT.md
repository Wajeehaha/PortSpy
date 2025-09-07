

I developed PortSpy, a TCP port scanner using Python, which taught me valuable lessons about network programming and security concepts. This project helped me understand how network communications work in practice.

Building the port scanner gave me hands-on experience with TCP/IP protocols. I learned that ports are like doorways on computers - web servers use port 80 for HTTP and port 443 for HTTPS, while SSH uses port 22. 

The most challenging part was learning Python's socket library. Creating a socket is like making a phone call - you specify the IP address and port number to connect to a specific service. I also learned about connection timeouts, which prevent the scanner from waiting too long for unresponsive ports.

Initially, my scanner checked ports one by one, which was very slow. Using Python's ThreadPoolExecutor to check multiple ports simultaneously reduced scan times from minutes to seconds. However, I learned that too many threads can overwhelm systems, so finding the right balance (around 50 threads) was important.

Through testing, I learned that ports have different states:
- **Open**: Service is running and accepts connections
- **Closed**: Port is accessible but no service running
- **Filtered**: Firewall blocks access

Testing different websites showed me that most organizations only expose necessary services (like web ports 80 and 443) while filtering others for security.

This project taught me about responsible use. Port scanning can be seen as suspicious activity, so it should only be used on your own systems, with explicit permission, or on educational targets like scanme.nmap.org.

When my scanner gave unexpected results, I learned to troubleshoot network issues. For example, when port 443 on scanme.nmap.org appeared filtered instead of open, I initially thought my code was wrong. Testing multiple targets showed my scanner was working correctly - the target configuration had changed.

I organized my code into separate modules for host resolution, port parsing, scanning logic, and result formatting. This modular approach made the code easier to understand and maintain.

The biggest challenges were handling network errors gracefully and creating user-friendly output. I learned to use try-catch blocks for error handling and added colors and progress bars to make the scanner easy to use for this i used some of the libraries i.e colorama to make my output in a formatted manner 

Building PortSpy was more educational than expected and it was fun too felt like a new thing I explored through which i can dive into new interesting things. It combined networking theory with practical programming skills and taught me about security, performance, and user experience.