Bootstrap: library
From: debian:buster


%files
    ./ /opt/gh-runner-singularity
    ./README.md /.singularity.d/runscript.help

%environment
    export AGENT_TOOLSDIRECTORY=/opt/hostedtoolcache

%post
    #  Install dependencies
    apt-get update
    apt-get install -y apt-transport-https build-essential ca-certificates \
        curl gettext iputils-ping jq libcurl4-openssl-dev liblttng-ust0 \
        openssh-client software-properties-common sudo supervisor unzip \
        zlib1g-dev python3-pip

    apt-get clean

    #  Create symlinks to simplify setup of runners. Intention is that you bind
    #  a directory to /mnt/github-runner, that directory is then used to store
    #  all of the unique files for the runner you're starting
    ln -s /mnt/github-runner /home/github-runner
    ln -s /home/github-runner/hostedtoolcache /opt/hostedtoolcache

    python3 -m pip install --upgrade pip
    python3 -m pip install /opt/gh-runner-singularity

%runscript
    exec gh-runner-singularity "$@"

%startscript
    exec gh-runner-singularity start "$@"

%labels
    Author RobertRosca
    Version v0.1.0
