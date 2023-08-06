# ECS Service Monitor (ecs-mon)

## Installation
```shell
pip install ecs-mon
```

## Usage
```shell
ecs-mon --svc my-service --cluster linux --alb --profile myAWSprofile
```

## Using esc-mon with watch
```shell
watch -n 10 ecs-mon --svc my-service --cluster linux --alb --profile myAWSprofile
```

The above command will rerun ecs-mon command every 10 seconds.

#### Installing Watch Command on MacOS
```shell
brew install watch
```

More information about Watch command: http://manpages.ubuntu.com/manpages/bionic/man1/watch.1.html

## Publishing Updates to PyPi

For the maintainer - to publish an updated version of ssm-search, increment the version number in version.py and run the following:

```shell
docker build -f ./Dockerfile.buildenv -t ecs-mon:build .
docker run --rm -it --entrypoint make ecs-mon:build publish
```

At the prompts, enter the username and password to the pypi.org repo.

## How to build
```shell
make build
```

## License

MIT License

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
