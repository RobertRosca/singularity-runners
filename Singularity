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

    python3 -m pip install --upgrade pip
    python3 -m pip install /opt/gh-runner-singularity

%runscript
    exec gh-runner-singularity "$@"

%startscript
    exec gh-runner-singularity start "$@"

%labels
    Author RobertRosca
    Version v0.1.0
