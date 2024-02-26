
# EventMusic Producer

EventMusic Producer is a Dockerized application designed to read data and output them to a Kafka topic, using Avro schemas for data serialization. It integrates seamlessly with Kafka and the Schema Registry to manage the flow of event data linked to music event information.

#### Event types
Page view events (page_view_events) are generated when users browse the site. They are structured as follows:
```
{
  "ts": "Timestamp of the event",
  "sessionId": "Session identifier",
  "page": "URL of the page visited",
  "auth": "Authentication status (Logged In/Logged Out)",
  "method": "HTTP method used for the request",
  "status": "HTTP status code of the response",
  "level": "Subscription type (free/paid)",
  "itemInSession": "Number of items in the session",
  "city": "User's city",
  "zip": "User's zip code",
  "state": "User's state/region",
  "userAgent": "Browser user agent",
  "lon": "Longitude",
  "lat": "Latitude",
  "userId": "User identifier",
  "lastName": "User's last name",
  "firstName": "User's first name",
  "gender": "User's gender",
  "registration": "User registration timestamp",
  "artist": "Listened artist",
  "song": "Song listened to",
  "duration": "Song duration in seconds".
}
```

Listen events (listen_events) are generated when users listen to songs. Their structure is as follows:
```
{
  "artist": "Artist name",
  "song": "Song title",
  "duration": "Song duration in seconds",
  "ts": "Event timestamp",
  "sessionId": "Session identifier",
  "auth": "Authentication status",
  "level": "Subscription type",
  "itemInSession": "Number of items in session",
  "city": "Ville",
  "zip": "Zip code",
  "state": "State/Region",
  "country": "Pays",
  "userAgent": "Browser user agent",
  "lon": "Longitude",
  "lat": "Latitude",
  "userId": "User identifier",
  "lastName": "Last name",
  "firstName": "First name",
  "gender": "Sexe",
  "registration": "Registration timestamp".
}
```
Authentication events (auth_events) are generated when users attempt to log in. Structure :
```
{
  "ts": "Timestamp de l'événement",
  "sessionId": "Identifiant de la session",
  "level": "Type d'abonnement",
  "itemInSession": "Nombre d'éléments dans la session",
  "city": "Ville",
  "zip": "Code postal",
  "state": "État/région",
  "userAgent": "Agent utilisateur du navigateur",
  "lon": "Longitude",
  "lat": "Latitude",
  "userId": "Identifiant de l'utilisateur",
  "lastName": "Nom de famille",
  "firstName": "Prénom",
  "gender": "Sexe",
  "registration": "Timestamp de l'inscription",
  "success": "Succès de l'authentification (True/False)"
}
```

## Features

- **Kafka Integration**: Seamlessly produces music event data to Kafka topics.
- **Avro Serialization**: Utilizes Avro schemas for efficient data serialization and validation.
- **Docker Support**: Fully Dockerized for easy deployment and scaling.
- **Batch Processing**: Sends data in batches to optimize network use and processing time.
- **Flexible Configuration**: Easy to configure with environment variables for Kafka, Schema Registry, and more.

## Getting Started with Docker

Follow these steps to get the application running with Docker:

### Pull the Docker Image

```
docker pull stefen2020/eventmusic:v1
```

### Run the Container

Make sure Kafka and Schema Registry are running and accessible. Replace `localhost` with your Kafka and Schema Registry hosts if necessary.

```
docker run --network="host" --name eventmusic-container stefen2020/eventmusic:v1
```

## Getting Started manually

Make sure Kafka and Schema Registry are running and accessible. Replace `localhost` with your Kafka and Schema Registry hosts if necessary.

```
python listen_events.py

python page_view_events.py

python auth_events.py

python main.py
```

## Contributing

Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See `LICENSE` for more information.

## Contact

- **Name**: Stefen Taime
- **Email**: [stefentaime@gmail.com](mailto:stefen@example.com)
- **Project URL**: [https://github.com/Stefen-Taime/eventmusic](https://github.com/Stefen-Taime/eventmusic)
- **Project HUB DOCKER URL**: [https://hub.docker.com/r/stefen2020/eventmusic](https://hub.docker.com/r/stefen2020/eventmusic)
