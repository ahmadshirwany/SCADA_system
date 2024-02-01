# Flask App for Data Visualization

## Overview

This Flask app is a small course project designed to provide a user-friendly interface for visualizing and analyzing data coming from robots in the field. Hosted on Azure, it utilizes various routes to fetch and display data, providing insights into robot performance, alarms, and statistics.

## Features

- **Dashboard**: View overall robot data with the ability to filter by robot ID.
- **Measurement History**: Explore historical measurement data for better analysis.
- **Event History**: Access a log of events recorded by the robots.

## Project Background

This project is part of a course and serves as an educational exercise to visualize data collected from robots deployed in the field. The web service is hosted on Azure, showcasing practical experience in deploying applications on cloud platforms.

## Azure Hosting

The web service is hosted on Azure, leveraging its cloud infrastructure to ensure scalability and availability.

## Setup

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS
- SQLite

- 

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/your_repo.git
   
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   
3. Configure the database URI:
   ```bash
   app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///your_database.db"

4. Run the application:
    ```bash
    python app.py

### Dashboard

- **Route**: `/`
- **Description**: Displays overall robot data with filtering options.

### Measurement History

- **Route**: `/measurement-history`
- **Description**: Displays historical measurement data for analysis.

### Event History

- **Route**: `/event-history`
- **Description**: Displays a log of events recorded by the robots.

### Data

- **Route**: `/data`
- **Description**: Fetches robot data based on parameters like robot ID, start date, and end date.

### Alarms

- **Route**: `/alarms`
- **Description**: Fetches alarm data based on parameters like robot ID, start date, and end date.

### Robot Data Stats

- **Route**: `/rob_data_stats`
- **Description**: Fetches statistics for a specific robot.

### Robots Latest Status

- **Route**: `/robots_latest_status`
- **Description**: Fetches the latest status of a specific robot.

### Usage

- Access the application through the defined routes and interact with the data visualization dashboards.


