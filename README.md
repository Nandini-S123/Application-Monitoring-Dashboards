# Application Monitoring Dashboards

## Overview
Monitors application logs using Kafka,Zookeeper, MySQL, and Grafana.

## Setup
- Run: `docker-compose up --build`
- Run: 'node producer.js'(in other terminal)
- Grafana: `http://localhost:3000` 

## Dashboards
- Requests per Endpoint: Bar chart of request counts.
- Response Time Trends: Time-series of average response times.
- Error Distribution: Pie chart of error types.
- Recent Logs: Table of latest log entries.
- Error Rate by Endpoint: Bar chart of error percentages.

## Commands
- Start: `docker-compose up --build`
- Stop: `docker-compose down`
