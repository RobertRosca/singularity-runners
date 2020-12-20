Bootstrap: library
From: debian:buster


%files
    ./scripts /opt/scripts

%environment
    export AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache

%post
    #  Install dependencies
    apt-get update
    apt-get install -y apt-transport-https build-essential ca-certificates \
        curl gettext iputils-ping jq libcurl4-openssl-dev liblttng-ust0 \
        openssh-client software-properties-common sudo supervisor unzip \
        zlib1g-dev

    apt-get clean

    #  Create symlinks to simplify setup of runners. Intention is that you bind
    #  a directory to /mnt/github-runner, that directory is then used to store
    #  all of the unique files for the runner you're starting
    ln -s /mnt/github-runner /home/github-runner
    ln -s /home/github-runner/hostedtoolcache /opt/hostedtoolcache

%apprun configure
    exec /opt/scripts/configure.py "$@"

%startscript
    exec /opt/scripts/start.py "$@"

%labels
    Author RobertRosca
    Version v0.1.0

%help
    Singularity container with dependencies required to run a self-hosted GitHub
    Runner. Contains some convenience scripts (`/opt/scripts`) to set up and
    start the runner.

    To set up the runner:

        singularity run -C \
            -B $LOCAL_STORAGE:/mnt/github-runner \
            --app configure \
            ./github-runner.sif \
            --url $GITHUB_REPO_URL \
            --token $GITHUB_RUNNER_TOKEN

    `LOCAL_STORAGE` should be the path to where you want to store the runner
    files locally; `url` and `token` values can be found on GitHub when setting
    up your own runner: Settings -> Actions -> Self-hosted runners -> Add runner

    To start the runner as a service:

        singularity instance start -C \
            -B $LOCAL_STORAGE:/mnt/github-runner \
            ./github-runner.sif $INSTANCE_NAME

    `INSTANCE_NAME` can be any name you want the instance to have, it's what
    you'll see when running `singularity instance list`
