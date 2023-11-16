# Index HTML page for Nginx

The following code contains the html for the index page of the Airsight nginx server:

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Airsight Server</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #000;
            color: #fff;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            justify-content: center;
            min-height: 100vh;
            overflow-x: hidden;
        }

        header {
            text-align: left;
            margin-bottom: 20px;
            padding: 20px;
            width: 100%;
            box-sizing: border-box;
        }

        h1 {
            font-size: 2em;
            margin: 0;
            color: #ededed; /* Updated title color */
        }

        h2 {
            font-size: 1.5em;
            margin: 0;
            color: #ededed; /* Updated title color */
        }

        .services {
            display: flex;
            flex-wrap: wrap;
            justify-content: flex-start;
            gap: 20px;
            padding: 20px;
            box-sizing: border-box;
        }

        .service {
            background-color: #000000;
            padding: 20px;
            border: solid 1px #252525;
            border-radius: 10px;
            width: 300px;
            text-align: center;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
            transition: background-color 0.3s;
            margin: 10px;
        }

        .service:hover {
            background-color: #1a1a1a;
        }

        .service a {
            color: #ededed;
            text-decoration: none;
            font-weight: bold;
            display: block;
            margin-bottom: 10px;
        }

        .service-description {
            font-size: 0.9em;
            color: #8f8f8f;
        }

        footer {
            margin-top: 20px;
            text-align: left;
            padding: 20px;
            width: 100%;
            box-sizing: border-box;
            color: #8f8f8f;
        }
    </style>
</head>
<body>
    <header>
        <img src="https://airsight-woad.vercel.app/_next/image?url=%2Flogo-480px.png&w=96&q=75" alt="Airsight Logo" width="48" height="48">
        <h1>Airsight Server</h1>
        <h2>Welcome to Airsight Cloud Server</h2>
    </header>

    <div class="services">
        <div class="service">
            <a href="https://airsight-woad.vercel.app/" target="_blank">Airsight Frontend</a>
            <p class="service-description">Explore the Airsight web application. User-friendly interface for data visualization.</p>
        </div>

        <div class="service">
            <a href="https://airsight.cloudsin.space/api/" target="_blank">Backend API</a>
            <p class="service-description">Access the backend API for data retrieval. Provides data to the Airsight Frontend.</p>
        </div>

        <div class="service">
            <a href="https://airsight.cloudsin.space/grafana/" target="_blank">Grafana Dashboard</a>
            <p class="service-description">Monitor and visualize data using Grafana. Create and customize dashboards for insights.</p>
        </div>

        <div class="service">
            <a href="https://airsight.cloudsin.space/influxdb/" target="_blank">InfluxDB</a>
            <p class="service-description">Manage time-series data with InfluxDB. Stores and retrieves data efficiently over time.</p>
        </div>

        <div class="service">
            <a href="https://airsight.cloudsin.space/portainer/" target="_blank">Portainer</a>
            <p class="service-description">Manage Docker containers with Portainer. User-friendly interface for Docker container management.</p>
        </div>

        <div class="service">
            <a href="https://github.com/Sten-AP/AIrsight/" target="_blank">Github</a>
            <p class="service-description">The official GitHub repository for Airsight.</p>
        </div>
    </div>

    <footer>
        <p>For more information, visit <a href="https://github.com/Sten-AP/AIrsight/" target="_blank">Airsight GitHub Repository</a>.</p>
    </footer>
</body>
</html>
```