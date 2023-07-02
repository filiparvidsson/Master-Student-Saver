

# Master Student Saver

Filip Arvidsson - fa223hr@lnu

### Brief Overview


#### Time it might take you: 15min

### Objective 
Let me take you away on a journey, down to the south of Germany. The weather ranges from hot and humid, to cold and dry. You sit inside an old university building, concentrating away on your thesis. The words flow to the point you can't feel the sweat flowing down your forehead, your fingers sticking to the keyboard. Without your knowledge, it's time to put on a fan, open a window, or leave for another room. If only some kind of indicator could alarm you to the worsening indoor climate, and then see the inpact of the changes you make in real time.

My name is Filip, and this was written from the perspective of us master's students at the university of my thesis. I present to you, the Master Student Saver. Tag along and you can save some students too.

### Material
| Prop | Quantity   |
| :---:   | :---: |
| Rasperry Pi Pico W | 1  |
| DHT11 Sensor | 1   |
| RGB LED | 1   |
| 20pcs Jumper Cables M/F | 7   |

As outlined by the specifications of this project, I have worked with the Rasberry Pi Pico W. The great thing about the Pico W is the wireless LAN compatability, which opens up new possibilities to communicate with more data.

## Computer Setup

- ![Visual Studio Code](https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white)
My chosen IDE was Visual Studio Code. I got it working using the extension Pico-W-Go. That's all you need to start working. Visual Studio offers multiple ways to make the coding experience easier. Some tools I have chosen to use is the Github co-pilot extension and Intellisense for Python code.

### Putting everything together:
![circuit board](https://github.com/filiparvidsson/Master-Student-Saver/blob/main/images/circuits.jpg?raw=true)

Here you can see the
- Rasperry Pi Pico W to the left
- DHT11 Sensor connected with its data to Pin 16
- The RGB LED connected with its RGB channels to R(2), G(3), and B(4)

The Pico is using its wireless functionality to Setup a local web server which anyone on the network can connect to. The chosen platform was selected because the everything needs to be easy, free, and only available for people in the vicinity.

The platform works by sending a string to the webserver which the client then connects to. The webserver also sends some JavaScript in the string which puts more computation on the client.


### The code

#### My languages
- ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
As the aim of the course is to use Micropython, the backend functionality is coded using - you guessed it - Python. 

```
#Import the necessary libraries
import network
import socket
import machine
import time
from machine import Pin, PWM
from time import sleep
from dht import DHT11
```

```
# a function which takes wifi name and password as input and connects to the wifi
def connect_to_wifi(wifi_name, wifi_password)

def open_socket(ip, port)

def webpage(humidity, temperature, state, humState, tempState)

def serve(connection, pin)

# Method to read the temperature from the sensor
def read_temperature(sensor)

def read_humidity(sensor)

def evaluate_room(temperature, humidity)

def handle_rgb_light(Temptate, humState)

def light_rgb_light(color)

# Definition to light up the RGB light with a specific color
def light_rgb_light(color)

# Definition to put values into the arrays
def put_values_in_array(array, value, length)

# Initialize the pin and the sensor
pin = Pin("LED", Pin.OUT)
sensor = DHT11(Pin(16))
Led_R = PWM(Pin(2))
Led_G = PWM(Pin(3))
Led_B = PWM(Pin(4))
# Define the frequency
Led_R.freq(2000)   
Led_G.freq(2000)   
Led_B.freq(2000) 


try:
    ip = connect_to_wifi(ssid, password)
    connection = open_socket(ip, 80)
    serve(connection, pin)
except KeyboardInterrupt:
    machine.reset()
```


- ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
HTML5 was used to build the web interface using text and divs.

```
html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>ESP Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://d3js.org/d3.v6.min.js"></script>

            <style>
            body {{
            font-family: Arial, Helvetica, sans-serif;
            }}
            .chart {{
            width: 400px;
            height: 300px;
            }}
            .bar {{
            fill: steelblue;
            }}
        </style>
            </head>
            <body>
                <div">
                    <p>LED is <span id="led">{state}</span></p>
                </div>
                <div id="tempdiv">
                    <p>Temperature is <span id="temperature">{temperature}</span></p>
                    <p>Humidity is <span id="humidity">{humidity}</span></p>
                </div>
            
            <p>Inside is <span id="tempState">{tempState}</span> and <span id="humState">{humState}</span></p>

            <div class="chart"></div>
            </body>
            </html>
            """

```

- ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)
JavaScript handles the functionality of the interface.

```
<script>
                function updateContent() {{
                    var xhttp = new XMLHttpRequest();
                    
                    // Define the callback function when the request is complete
                    xhttp.onreadystatechange = function() {{
                        if (this.readyState == 4 && this.status == 200) {{
                            // Parse the response as separate values
                            var values = this.responseText.split('@@@');
                            var temperature = values[0];
                            var humidity = values[1];
                            var tempState = values[2];
                            var humState = values[3];
                            var state = values[4];    
                            document.getElementById("temperature").innerHTML = temperature;
                            document.getElementById("humidity").innerHTML = humidity;
                            document.getElementById("humState").innerHTML = humState;
                            document.getElementById("tempState").innerHTML = tempState;  
                            document.getElementById("led").innerHTML = state;

                            var tempArray = values[5];
                            var humArray = values[6];
                        
                            if (humState.includes("OK")) {{
                                document.getElementById("humidity").style.color = "green";
                            }} else {{
                                document.getElementById("humidity").style.color = "red";
                            }}

                            if (tempState.includes("OK")) {{
                                document.getElementById("temperature").style.color = "green";
                            }} else {{
                                document.getElementById("temperature").style.color = "red";
                            }}

                            updateChart(tempArray, humArray);
                                                    
                        }}
                    }};
                    
                    xhttp.open("GET", "/get_temperature", true);
                    xhttp.send();
                }}
                function updateChart(tempArray, humArray) {{
                var chartContainer = d3.select(".chart");

                chartContainer.selectAll("*").remove();
                var width = 400;
                var height = 300;
                var svg = chartContainer.append("svg")
                    .attr("width", width)
                    .attr("height", height);

                tempData = tempArray.split("[")[1].split("]")[0].split(", ");
                humData = humArray.split("[")[1].split("]")[0].split(", ");

                // Plot the temperature and humidity values as lines on the chart
                var xScale = d3.scaleLinear()
                    .domain([0, tempData.length - 1])
                    .range([0, width - 50]);

                var yScale = d3.scaleLinear()
                    .domain([0, 100])
                    .range([height - 50, 0]);

                var line = d3.line()
                    .x(function(d, i) {{ return xScale(i); }})
                    .y(function(d) {{ return yScale(d); }})
                    .curve(d3.curveMonotoneX);

                svg.append("path")
                    .datum(tempData)
                    .attr("fill", "none")
                    .attr("stroke", "green")
                    .attr("stroke-width", 2)
                    .attr("d", line)
                    .attr("transform", "translate(50, 0)");

                
                svg.append("rect")
                    .attr("x", 50)
                    .attr("y", yScale(21))
                    .attr("width", width - 50)
                    .attr("height", yScale(18) - yScale(21))
                    .attr("fill", "green")
                    .attr("opacity", 0.2);

                svg.append("path")
                    .datum(humData)
                    .attr("fill", "none")
                    .attr("stroke", "blue")
                    .attr("stroke-width", 2)
                    .attr("d", line)
                    .attr("transform", "translate(50, 0)");

                svg.append("rect")
                    .attr("x", 50)
                    .attr("y", yScale(50))
                    .attr("width", width - 50)
                    .attr("height", yScale(30) - yScale(50))
                    .attr("fill", "blue")
                    .attr("opacity", 0.2);

                var xAxis = d3.axisBottom(xScale);
                var yAxis = d3.axisLeft(yScale);

                svg.append("g")
                    .attr("transform", "translate(50," + (height - 50) + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("transform", "translate(50, 0)")
                    .call(yAxis);

                }}
                
                function startUpdating() {{
                    updateContent();

                    setInterval(updateContent, 1000);
                }}
                
                window.onload = startUpdating;
            </script>
```

### Data transmission
As previously mentioned, we use the Wifi protocal for data transfer. The STA_IF arguments means that we use an existing network.
```
wlan = network.WLAN(network.STA_IF)
```
After the wifi has been connected, it will return an IP adress of where a client can access the server.
```
ip = wlan.ifconfig()[0]
```
Then we wait for a connecting client, and see which request they want.
```
# Wait for a connection
        client = connection.accept()[0]
        # Read the request message as a string
        request = client.recv(1024)
        request = str(request)
```
One type of request is to get the measurement information.
```
if request == '/get_temperature':
...
```
This request is made every second, which refreshes our live values displayed on the page.
```
// Client side
setInterval(updateContent, 1000);
```
If 10 seconds has passed, we also update the array of logged values to update how it's previously been.
```
if (time.time() - start_time) > 10:
                tempArray = put_values_in_array(tempArray, temperature, length)
                humArray = put_values_in_array(humArray, humidity, length)
                start_time = time.time()
```
We then send the HTML-page with the updated information to the client.
```
html = webpage(humidity, temperature, state, humState, tempState)
            client.send(html)

client.close()
```

### Displaying the data

This project features different types of data:
Measured every second:
- Live temperature
- Live humidity
- The state of temperature - Processed on the server
- The state of humidity - Processed on the server
- The color as a result of the states
Measured and saved every 10 seconds
- An array with a defined length - If the array is filled it will delete the first element to fit the last.

The temperature, humidity, states, and color is displayed as text on the page. If the temperature or humidity is outside acceptable range it will have a red color, otherwise green. 
```
if (humState.includes("OK")) {{
                                document.getElementById("humidity").style.color = "green";
                            }} else {{
                                document.getElementById("humidity").style.color = "red";
                            }}

                            if (tempState.includes("OK")) {{
                                document.getElementById("temperature").style.color = "green";
                            }} else {{
                                document.getElementById("temperature").style.color = "red";
                            }}

```

The arrays containing previous measurements will be displayed using the D3.js library.
```
<script src="https://d3js.org/d3.v7.min.js"></script>
...
function updateChart(tempArray, humArray) {{
                var chartContainer = d3.select(".chart");

                chartContainer.selectAll("*").remove();
                var width = 400;
                var height = 300;
                var svg = chartContainer.append("svg")
                    .attr("width", width)
                    .attr("height", height);

                tempData = tempArray.split("[")[1].split("]")[0].split(", ");
                humData = humArray.split("[")[1].split("]")[0].split(", ");

                // Plot the temperature and humidity values as lines on the chart
                var xScale = d3.scaleLinear()
                    .domain([0, tempData.length - 1])
                    .range([0, width - 50]);

                var yScale = d3.scaleLinear()
                    .domain([0, 100])
                    .range([height - 50, 0]);

                var line = d3.line()
                    .x(function(d, i) {{ return xScale(i); }})
                    .y(function(d) {{ return yScale(d); }})
                    .curve(d3.curveMonotoneX);

                svg.append("path")
                    .datum(tempData)
                    .attr("fill", "none")
                    .attr("stroke", "green")
                    .attr("stroke-width", 2)
                    .attr("d", line)
                    .attr("transform", "translate(50, 0)");

                
                svg.append("rect")
                    .attr("x", 50)
                    .attr("y", yScale(21))
                    .attr("width", width - 50)
                    .attr("height", yScale(18) - yScale(21))
                    .attr("fill", "green")
                    .attr("opacity", 0.2);

                svg.append("path")
                    .datum(humData)
                    .attr("fill", "none")
                    .attr("stroke", "blue")
                    .attr("stroke-width", 2)
                    .attr("d", line)
                    .attr("transform", "translate(50, 0)");

                svg.append("rect")
                    .attr("x", 50)
                    .attr("y", yScale(50))
                    .attr("width", width - 50)
                    .attr("height", yScale(30) - yScale(50))
                    .attr("fill", "blue")
                    .attr("opacity", 0.2);

                var xAxis = d3.axisBottom(xScale);
                var yAxis = d3.axisLeft(yScale);

                svg.append("g")
                    .attr("transform", "translate(50," + (height - 50) + ")")
                    .call(xAxis);

                svg.append("g")
                    .attr("transform", "translate(50, 0)")
                    .call(yAxis);

                }}

```
The color is displayed on the web interface as well as the LED. The color is dependant upon different combinations of temperature and humidity.

```
if Temptate == 'COLD' and humState == 'DRY':
        color = 'BLUE'
    elif Temptate == 'COLD' and humState == 'HUMID':
        color = 'CYAN'
    elif Temptate == 'COLD' and humState == 'OK':
        color = 'WHITE'
    elif Temptate == 'HOT' and humState == 'DRY':
        color = 'RED'
    elif Temptate == 'HOT' and humState == 'HUMID':
        color = 'PURPLE'
...
```
If everything is acceptable, the color will be green.
## Final results
The final result is a connected system between the sensor measuring, and a live web interface, and a LED showing different states.

### The hardware
As shown by the image, the LED indicates the current state, which is HOT and HUMID.
![circuit board](https://github.com/filiparvidsson/Master-Student-Saver/blob/main/images/LEDon.jpg?raw=true)



### The web interface
Here you can observe the temperature and humidity being measured at different times.

After 14 measurements:
![interface 1](https://github.com/filiparvidsson/Master-Student-Saver/blob/main/images/interface.PNG?raw=true)

After 23 measurements: 
![interface 2](https://github.com/filiparvidsson/Master-Student-Saver/blob/main/images/interface2.PNG?raw=true)

### Final thoughts
I am fairly happy that the script finally worked. It was unknown issues with the website when more was added, but it turned out I was maxing out the size of the string in regards to memory. A final touch would have been to have the outside measurements for comparison. 


## Authors

- [@filiparvidsson](https://github.com/filiparvidsson)

