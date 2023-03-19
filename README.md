# DETR Object Detection Web App

This is a web application that uses Facebook's DETR (DEtection TRansformer) model to perform object detection on images.

## Installation

### Prerequisites

- Docker Compose

To install Docker Compose on Ubuntu, you can follow the instructions on the [official Docker website](https://docs.docker.com/compose/install/).

Note that this program is designed to work on any operating system that supports Docker, but it has only been tested on Ubuntu 20.04.5 LTS x86_64. For the best experience, it is recommended to use Ubuntu 20.04.5 LTS x86_64.

### Clone the Repository

Clone the repository by running the following command in a terminal:

`git clone https://github.com/0x00000024/detr-object-detection-web-app.git`

### Start the Docker Containers

Start the Docker containers by running the following command:

`bash detr-object-detection-web-app/docker/start_docker_compose.sh`

To connect to the Docker container, you can use SSH:

`ssh root@localhost -p 2222`

The default password is "1". You can change the password and port in the `.env` file in the `docker` directory.

## Usage

To run the program, use the following command:

`python detr_object_detection.py`

After running the above command, you can test the application by opening localhost in your Ubuntu web browser.

## Demo

![DETR Object Detection Web App Demo](./static/demo.gif)

## License

This program is licensed under the MIT license. See the `LICENSE` file for more information.
