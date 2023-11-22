<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frontend Example</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            background-image: url('1.avif');
            /* Set the background image */
            background-size: cover;
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            color: white;
        }

        /* Style for the buttons */
        button {
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px;
            cursor: pointer;
            background-color: #4CAF50;
            /* Green background color */
            color: white;
            border: none;
            border-radius: 5px;
        }

        /* Hide the emergencyStopButton initially */
        #emergencyStopButton {
            display: none;
        }
    </style>
</head>

<body>

    <h1>Unmanned Automatic Inspection System for Patrol of Suspicious Objects</h1>

    <button id="sendRequestButton">Start Patrol</button>
    <button id="emergencyStopButton">Emergency Stop</button>

    <script>
        document.getElementById("sendRequestButton").addEventListener("click", function () {
            var serverAddress = 'http://192.168.50.183:8888';
            var message_wak = 'wake up';

            fetchRequest(serverAddress, message_wak);

            document.getElementById("sendRequestButton").style.display = "none";
            document.getElementById("emergencyStopButton").style.display = "inline-block";
        });

        document.getElementById("emergencyStopButton").addEventListener("click", function () {
            var serverAddress = 'http://192.168.50.183:8888';
            var message_stp = 'stop';

            fetchRequest(serverAddress, message_stp);
        });

        function fetchRequest(serverAddress, message) {
            alert('send successfully');

            fetch(serverAddress, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: 'message=' + message,
            })
                .then(response => response.text())
                .then(data => {
                    console.log('Server Response:', data);
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }
    </script>

</body>

</html>
