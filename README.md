# gh-runner-singularity
A Singularity Container Image to Setup and Run GitHub Self-Hosted Runners

Singularity container with dependencies required to run a self-hosted GitHub
Runner. Contains some convenience scripts (`/opt/scripts`) to set up and
start the runner.

## Quick-Start

To get the container either:

1. Build it locally:  \
   `sudo singularity build github-runner.sif ./Singularity`
2. Pull it from Singularity Hub:  \
   `singularity pull shub://RobertRosca/gh-runner-singularity`

Then to configure your first runner:

```
singularity run -C \
    -B $LOCAL_STORAGE:/mnt/github-runner \
    ./github-runner.sif \
    configure --url $GITHUB_REPO_URL --token $GITHUB_RUNNER_TOKEN
```

`LOCAL_STORAGE` should be the path to where you want to store the runner
files locally; `url` and `token` values can be found on GitHub when setting
up your own runner: Settings -> Actions -> Self-hosted runners -> Add runner

To start the runner as a service:

```
singularity instance start -C \
    -B $LOCAL_STORAGE:/mnt/github-runner \
    ./github-runner.sif $INSTANCE_NAME
```

`INSTANCE_NAME` can be any name you want the instance to have, it's what
you'll see when running `singularity instance list`

## Examples

Here I want to have a directory `~/.github-runners/` which stores all the data
for the runners, first I build the container locally:

```
sudo singularity build github-runner.sif ./Singularity
```

I want this runner to be configured for this repository:
<https://github.com/robertrosca/vip-ipykernel>, so in this case the runner will
go in `~/.github-runners/vip-ipykernel/`.

So, I go to <https://github.com/RobertRosca/vip-ipykernel/settings/actions> and
click 'Add runner', this will show the (temporary) registration token, I can
just copy-paste it from the 'configure' line:

```
singularity run -C \
    -B ~/.github-runners/vip-ipykernel/:/mnt/github-runner \
    ./github-runner.sif configure --url https://github.com/RobertRosca/vip-ipykernel --token AAYPOCA2ZF9HQYEHPMUYHYS735IYW
```

This downloads and sets up the local runner under
`~/.github-runners/vip-ipykernel/`. Now I can start it in the background using
the `singularity instance` command:

```
singularity instance start -C \
    -B ~/.github-runners/vip-ipykernel/:/mnt/github-runner \
    ./github-runner.sif vip-ipykernel-runner
```

## Running Instances as Systemd Service

It's also possible to run the instance as a service, read more about this
[here](https://sylabs.io/guides/3.5/user-guide/running_services.html#system-integration-pid-files). In this case I would start the instance with
a pid-file argument:

```
singularity instance start -C \
    -B ~/.github-runners/vip-ipykernel/:/mnt/github-runner \
    --pid-file ~/.github-runners/vip-ipykernel/.pid \
    ./github-runner.sif vip-ipykernel-runner
```

And the systemd service file:

```
[Unit]
Description=ViP-IPykernel Self-Hosted GitHub Runner
After=network.target

[Service]
Type=forking
Restart=always
PIDFile=/home/roscar/.github-runners/vip-ipykernel/.pid
ExecStart=/usr/local/bin/singularity instance start -C -B ~/.github-runners/vip-ipykernel/:/mnt/github-runner --pid-file ~/.github-runners/vip-ipykernel/.pid ./github-runner.sif vip-ipykernel-runner
ExecStop=/usr/local/bin/singularity instance stop vip-ipykernel-runner

[Install]
WantedBy=multi-user.target
```
