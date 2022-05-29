[
  {
    "name": "the_internet",
    "image": "${docker_image_url_django}",
    "essential": true,
    "cpu": 10,
    "memory": 512,
    "links": [],
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 0,
        "protocol": "tcp"
      }
    ],
    "command": ["./run_server.sh", "8000"],
    "environment": [
      {
        "name": "DJANGO_SUPERUSER_USERNAME",
        "value": "${django_superuser_username}"
      },
      {
        "name": "DJANGO_SUPERUSER_PASSWORD",
        "value": "${django_superuser_password}"
      },
      {
        "name": "DJANGO_SUPERUSER_EMAIL",
        "value": "${django_superuser_email}"
      },    
      {
        "name": "RDS_DB_NAME",
        "value": "${rds_db_name}"
      },

      {
        "name": "DJANGO_SECRET_KEY",
        "value": "${django_secret_key}"
      },
      {
        "name": "RDS_USERNAME",
        "value": "${rds_username}"
      },
      {
        "name": "RDS_PASSWORD",
        "value": "${rds_password}"
      },
      {
        "name": "RDS_HOSTNAME",
        "value": "${rds_hostname}"
      },
      {
        "name": "STAGE",
        "value": "${django_stage}"
      },
      {
        "name": "RDS_PORT",
        "value": "5432"
      }
    ],
    "mountPoints": [
      {
        "containerPath": "/usr/src/app/staticfiles",
        "sourceVolume": "static_volume"
      }
    ],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/the_internet",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "the_internet-log-stream"
      }
    }
  },
  {
    "name": "nginx",
    "image": "${docker_image_url_nginx}",
    "essential": true,
    "cpu": 10,
    "memory": 128,
    "links": ["the_internet"],
    "portMappings": [
      {
        "containerPort": 80,
        "hostPort": 0,
        "protocol": "tcp"
      }
    ]
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/nginx",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "nginx-log-stream"
      }
    }
  }
]
