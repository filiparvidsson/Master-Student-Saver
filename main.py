import network
import socket
import machine
import time
from machine import Pin, PWM
from time import sleep
from dht import DHT11


# a function which takes wifi name and password as input and connects to the wifi
def connect_to_wifi(wifi_name, wifi_password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_name, wifi_password)
    while not wlan.isconnected():
        print("Connecting to wifi...")
        sleep(1)
    ip = wlan.ifconfig()[0]
    print("Connected to wifi with ip: {}".format(ip))
    return ip

def open_socket(ip, port):
    # Open a socket
    address = (ip, port)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage(humidity, temperature, state, humState, tempState):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>ESP Web Server</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://d3js.org/d3.v7.min.js"></script>

            <style>
            body {{
            font-family: Arial, Helvetica, sans-serif;
            }}
            .chart {{
            width: 500px;
            height: 400px;
            }}
            .bar {{
            fill: steelblue;
            }}
        </style>
            </head>
            <body>
                <div>
                    <p>LED is <span id="led">{state}</span></p>
                </div>
                <div id="tempdiv">
                    <p>Temperature is <span id="temperature">{temperature}</span></p>
                    <p>Humidity is <span id="humidity">{humidity}</span></p>
                </div>
            
            <p>Inside is <span id="tempState">{tempState}</span> and <span id="humState">{humState}</span></p>
            <p> The bar chart below shows the temperature and humidity values</p>
            <div class="chart"></div>
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
            
            </body>
            </html>
            """
    return str(html)

def serve(connection, pin):
    #Start a web server
    state = 'BLACK'
    pin.off()
    temperature = 0
    humidity = 0
    tempState = 'OK'
    humState = 'OK'
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton':
            pin.on()
            state = 'ON'
            # Redirect back to the main page
            client.send("HTTP/1.1 303 See Other\nLocation: /\n\n")
        elif request =='/lightoff':
            pin.off()
            state = 'OFF'
            # Redirect back to the main page
            client.send("HTTP/1.1 303 See Other\nLocation: /\n\n")
        elif request == '/get_temperature':
            # Code for handling get_temperature request
            response = ""
            # Read the temperature from the sensor
            sensor.measure()
            temperature = read_temperature(sensor)
            humidity = read_humidity(sensor)
            tempState, humState, state = evaluate_room(temperature, humidity)

            # Prepare the temperature data as a string response
            response = f"Temperature: {temperature}@@@"
            response += f"Humidity: {humidity}@@@"
            # make them into strings for the html
            response += f"Temp State: {tempState}@@@"
            response += f"Hum State: {humState}@@@"
            response += f"State: {state}@@@"



            # call the put_values:in_array method the first time and then ever minute
            global tempArray, humArray, start_time
            if (time.time() - start_time) > 10:
                tempArray = put_values_in_array(tempArray, temperature, length)
                humArray = put_values_in_array(humArray, humidity, length)
                start_time = time.time()

            # Add the array to the response as a string
            response += f"Temp Array: {tempArray}@@@"
            response += f"Hum Array: {humArray}@@@"


            # Combine the response and HTML code
            html = webpage(humidity, temperature, state, humState, tempState)
            response += html

            # Send the combined response
            client.send(response)
        else:
            html = webpage(humidity, temperature, state, humState, tempState)
            client.send(html)

        client.close()


# Method to read the temperature from the sensor
def read_temperature(sensor):
    temperature = sensor.temperature()
    return temperature

# Method to read the humidity from the sensor
def read_humidity(sensor):
    humidity = sensor.humidity()
    return humidity

# Definition to evaluate room temperature and humidity
def evaluate_room(temperature, humidity):
    if temperature < 18:
        tempState = 'COLD'
    elif temperature > 21:
        tempState = 'HOT'
    else:
        tempState = 'OK'
    
    if humidity < 30:
        humState = 'DRY'
    elif humidity > 50:
        humState = 'HUMID'
    else:
        humState = 'OK'

    color = handle_rgb_light(tempState, humState)

    return tempState, humState, color

# Definition for handling the RGB light, which takes in a string and a color
def handle_rgb_light(Temptate, humState):
# light different colors depending on the temperature and humidity
    color = 'WHITE'
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
    elif Temptate == 'HOT' and humState == 'OK':
        color = 'YELLOW'
    elif Temptate == 'OK' and humState == 'OK':
        color = 'GREEN'
    elif Temptate == 'OK' and humState == 'DRY':
        color = 'WHITE'
    elif Temptate == 'OK' and humState == 'HUMID':
        color = 'WHITE'
    else:
        color = 'BLACK'
    light_rgb_light(color)
    return color


# Definition to light up the RGB light with a specific color
def light_rgb_light(color):
    if color == 'RED':
        Led_R.duty_u16(65535)
        Led_G.duty_u16(0)
        Led_B.duty_u16(0)
    elif color == 'GREEN':
        Led_R.duty_u16(0)
        Led_G.duty_u16(65535)
        Led_B.duty_u16(0)
    elif color == 'BLUE':
        Led_R.duty_u16(0)
        Led_G.duty_u16(0)
        Led_B.duty_u16(65535)
    elif color == 'YELLOW':
        Led_R.duty_u16(65535)
        Led_G.duty_u16(65535)
        Led_B.duty_u16(0)
    elif color == 'PURPLE':
        Led_R.duty_u16(65535)
        Led_G.duty_u16(0)
        Led_B.duty_u16(65535)
    elif color == 'CYAN':
        Led_R.duty_u16(0)
        Led_G.duty_u16(65535)
        Led_B.duty_u16(65535)
    elif color == 'WHITE':
        Led_R.duty_u16(65535)
        Led_G.duty_u16(65535)
        Led_B.duty_u16(65535)
    elif color == 'BLACK':
        Led_R.duty_u16(0)
        Led_G.duty_u16(0)
        Led_B.duty_u16(0)
    else:
        Led_R.duty_u16(0)
        Led_G.duty_u16(0)
        Led_B.duty_u16(0)
        print('Invalid color')

# Definition to put values into the arrays
def put_values_in_array(array, value, length):
    # If the array have 24 values, remove the first element
    if len(array) == length:
        array.pop(0)
    # Append the new value to the array
    array.append(value)
    return array


    
# If not at home, use the following wifi
atHome = False

if not atHome:
    ssid = 'XXXX'
    password = 'XXXX'
else:
    ssid = 'XXXX'
    password = 'XXXX'

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

# Two empty arrays to store 24 hours of temperature and humidity
tempArray = [0]
humArray = [0]
length = 1000
start_time = time.time()



try:
    ip = connect_to_wifi(ssid, password)
    connection = open_socket(ip, 80)
    serve(connection, pin)
except KeyboardInterrupt:
    machine.reset()


# Unit tests for the functions, use later for a test.py file
def test_read_temperature():
    # check that the temperature is a float
    assert type(read_temperature(sensor)) == float

def test_read_humidity():
    # check that the humidity is a float
    assert type(read_humidity(sensor)) == float

def test_evaluate_room():
    # check that the temperature-, humidity-state and color is a string
    assert type(evaluate_room(20, 40)[0]) == str
    assert type(evaluate_room(20, 40)[1]) == str
    assert type(evaluate_room(20, 40)[2]) == str

def test_handle_rgb_light():
    # check that the color is a string
    assert type(handle_rgb_light('OK', 'OK')) == str

def test_light_rgb_light():
    # Test to see that if invalid color is given, led is turned off
    light_rgb_light('INVALID')
    assert Led_R.duty_u16() == 0

def test_put_values_in_array():
    # Test to see that the array is updated with the new value
    assert put_values_in_array([1,2,3], 4, 3) == [2,3,4]
    # Test to see that the array is updated with the new value and the first element is removed
    assert put_values_in_array([1,2,3], 4, 2) == [2,3,4]
    # Test to see that the array is updated with the new value and the first element is removed
    assert put_values_in_array([1,2,3], 4, 1) == [3,4]
    # Test to see that the array is updated with the new value and the first element is removed
    assert put_values_in_array([1,2,3], 4, 0) == [4]

# Run the unit tests once when the program starts
test_read_temperature()
test_read_humidity()
test_evaluate_room()
test_handle_rgb_light()
test_light_rgb_light()
test_put_values_in_array()

