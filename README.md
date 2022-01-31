# MQTT Client

This simple pub-sub client connects to an MQTT broker over AWS IoT and listens for messages posted by other clients over MQTT protocol and calculates the aerial distance between the clients.

## Demo

My personal live test involved two clients, one in a `zsh` terminal on a Macbook, and another on a Raspberry Pi 3.

### Setup & Usage

#### MQTT Broker (AWS IoT)

1. Register for AWS. As of 2022, AWS IoT has a free-tier for the first 12 months of an AWS account.
2. Set a security policy allowing publish and subscribe permissions for specific resources or from any authorized device.
3. Register a "Thing" (device) in AWS IoT. This should provide the following:
    - CA certificate (`.crt`)
    - Private RSA Key (`.pem`)
    - Certificate (`.private.key`)

#### MQTT Client

1. `git clone` this repository to the device.
2. In the project root, create a directory named `/credentials`
3. Place the files in Step 3 of the Broker section in `/credentials`. The files must be renamed as follows:
    - CA certificate: `root-CA.crt`
    - Certificate: `Thing.cert.pem`
    - Private Key: `Thing.private.key`
3. Create a `.env` file.
4. Enter the following information as environment variables. As locating the physical location of a device requires the use of a geolocation provider, this value is hard-coded for the scope of this project.
    - `AWS_ENDPOINT`: The endpoint of the cloud MQTT broker server.
    - `ID`: Some identifier for the device. Its value doesn't matter much but using duplicate IDs for clients will prevent it from calculating the distance with the other client.
    - `LAT`: Latitide value of the device's location.
    - `LNG`: Longitude value of the device's location.
5. `python3 client.py`

`.env` Example:
```
AWS_ENDPOINT=<'SECRET'>.iot.ca-central-1.amazonaws.com
ID=WPG
LAT=49.8153341
LNG=-97.0838079
```