# Quick reference

Maintained by: [Michael Oberdorf IT-Consulting](https://www.oberdorf-itc.de/)

Source code: [GitHub](https://github.com/cybcon/docker.dsb2pushover)

Container image: [DockerHub](https://hub.docker.com/r/oitc/dsb2pushover)

# Supported tags and respective `Dockerfile` links


* [`latest`, `1.0.12`](https://github.com/cybcon/docker.dsb2pushover/blob/v1.0.12/Dockerfile)
* [`1.0.9`](https://github.com/cybcon/docker.dsb2pushover/blob/v1.0.9/Dockerfile)
* [`1.0.8`](https://dev.azure.com/oberdorf-itc/Infrastructure/_git/docker.dsb2pushover?path=%2Fresources%2FDockerfile&version=GT1.0.8&_a=contents)
* [`1.0.7`](https://dev.azure.com/oberdorf-itc/Infrastructure/_git/docker.dsb2pushover?path=%2Fresources%2FDockerfile&version=GT1.0.7&_a=contents)


# What is the dsb2pushover container?

[DSBMobile](https://dsbmobile.de/) is a very common service in Germany for schools to manage substitution plans. There are several apps for the common mobile phone platforms.
After some problems with the DSBmobile app for Android I started looking for an API for DSBMobile to make the query more comfortable.
Here I came across the Python library [DSBApi](https://github.com/nerrixDE/DSBApi) and got inspired by it and built a Docker container from it, which filters out only the necessary entries for the coming day, prepares them and distributes them with the [Pushover](https://pushover.net/) service.

# Prerequisites to run the docker container
1. You need a DSBMobile login from the school (user and password)
2. You need a Pushover account and you need to create a new application for that (UserKey, ApiKey)

# Configuration
The docker container grab the configuration via environment variables.

| Environment variable name | Description | Required | Default value |
|--|--|--|--|
| `DSB_USERNAME` | The login username for DSBMobile | **MANDATORY** | |
| `DSB_PASSWORD` | The login password for DSBMobile | **MANDATORY** | |
| `PUSHOVER_USER_KEY` | The user key of your pushover account | **MANDATORY** | |
| `PUSHOVER_API_KEY` | The application key of your pushover application | **MANDATORY** | |
| `FILTER_SCHOOLCLASS` | The name of the school class in DSBMobile (regexp) | **OPTIONAL** | |
| `LOGLEVEL` | The loglevel of the application inside the container, can be one of: `debug`, `info`, `warning`, `error` | **OPTIONAL** | ` info` |
| `DSB_TABLE_FIELDS` | The table format of the DSBMobile tables, a comma separated list of attribute names | **OPTIONAL** | `type,class,lesson,subject,room,new_subject,new_teacher,teacher`

# Docker run

```
docker run --rm \
  -e DSB_USERNAME='dsb_username' \
  -e DSB_PASSWORD='mySecretPassword' \
  -e PUSHOVER_USER_KEY='PushoverUserKey' \
  -e PUSHOVER_API_KEY='PushoverApiKey' \
  -e FILTER_SCHOOLCLASS='6a?b?cd?' \
  -e DSB_TABLE_FIELDS='class,lesson,new_subject,room,subject,new_teacher,type,text' \
  oitc/dsb2pushover:latest
```

# Docker compose configuration

```yaml
  dsb2pushover:
    restart: "no"
    image: oitc/dsb2pushover:latest
    environment:
      DSB_USERNAME: 'dsb_username'
      DSB_PASSWORD: 'mySecretPassword'
      PUSHOVER_USER_KEY: 'PushoverUserKey'
      PUSHOVER_API_KEY: 'PushoverApiKey'
      FILTER_SCHOOLCLASS: '6a?b?cd?'
      DSB_TABLE_FIELDS: 'class,lesson,new_subject,room,subject,new_teacher,type,text'
```

# Example crontab entry
This is an example crontab entry to trigger the docker container every 5pm to send the updates for tomorrow using docker compose.
```
0 17 * * * /usr/bin/docker-compose -f docker-compose.yml run --rm dsb2pushover >/dev/null 2>&1
```

# Donate
I would appreciate a small donation to support the further development of my open source projects.

<a href="https://www.paypal.com/donate/?hosted_button_id=BHGJGGUS6RH44" target="_blank"><img src="https://raw.githubusercontent.com/stefan-niedermann/paypal-donate-button/master/paypal-donate-button.png" alt="Donate with PayPal" width="200px"></a>

# License

Copyright (c) 2023 Michael Oberdorf IT-Consulting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
