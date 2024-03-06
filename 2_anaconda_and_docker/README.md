# Anaconda and Docker

## 1. Install Anaconda/Miniconda.

I use Linux Ubuntu and I already have Miniconda installed, but to install it one can use the following commands:

`wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh`

`bash Miniconda3-latest-Linux-x86_64.sh`

## 2. Create `conda` environment, install the following programs with specified versions:

* [fastqc](https://www.bioinformatics.babraham.ac.uk/projects/fastqc/), v0.11.9
* [STAR](https://github.com/alexdobin/STAR), v2.7.10b
* [samtools](https://github.com/samtools/samtools), v1.16.1
* [picard](https://github.com/broadinstitute/picard), v2.27.5
* [salmon](https://github.com/COMBINE-lab/salmon), commit tag 1.9.0
* [bedtools](https://github.com/arq5x/bedtools2), v2.30.0
* [multiqc](https://github.com/ewels/MultiQC), v1.13

Create new totaly empty environment called `dependencies` by the command:

`conda create --name dependencies --no-default-packages`

Activate a new environment:

`conda activate dependencies`

Add channels through which I will install new packages:

`conda config --add channels bioconda`

`conda config --add channels conda-forge`

Install the particular versions of the tools:

`conda install fastqc=0.11.9`

`conda install star=2.7.10b`

`conda install bedtools=2.30.0`

`conda install samtools=1.16.1`

`conda install salmon=1.9.0`

`conda install multiqc=1.13`

I failed to install picard of the 2.27.5 version, because the latest version of it in Conda is 2.27.

## 3. Export `conda` environment to the **environment.yml** file. Recover the invironment on the basis of this file.

Export the environment to the **environment.yml** file:

`conda env export --from-history > environment.yml`

The content of the [**environment.yml**](environment.yml) file:

---

```
name: dependencies
channels:
  - conda-forge
  - bioconda
  - defaults
dependencies:
  - samtools=1.16.1
  - salmon=1.9.0
  - multiqc=1.13
  - fastqc=0.11.9
  - star=2.7.10b
  - bedtools=2.30.0
prefix: /home/snitkin/anaconda3/envs/dependencies
```

---

Delete the dependencies environment:

`conda env remove -n dependencies`

Recover the invironment on the basis of the [**environment.yml**](environment.yml) file:

`conda env create -n dependencies --file environment.yml`

After download, check that all the packages of particular versions are there with `conda list`. Yes, this is it!

## 4. [Install Docker](https://docs.docker.com/engine/install/ubuntu/)

```
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release


sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
 
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
  
sudo apt-get update
  
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

## 5. Create **Dockerfile** with the same list of programs.

Create a Dockerfile (see the content of the Dockerfile below):

`nano Dockerfile`

Create an image from the Dockerfile:

`sudo docker build -t dependencies .`

Launch the container from image:

`sudo docker run -it dependencies bash`

*Warning! Execute `. /.bashrc` command right after the container is run for correct work of all aliases.*

**[Dockerfile](Dockerfile_before) before linter**

---

```docker
FROM ubuntu:latest
MAINTAINER "snitkin.d@list.ru"
# apt-transport-https & wget
RUN apt update && \
    apt -y install apt-transport-https wget
# Unzip
RUN apt install unzip
# Java
RUN apt -y install openjdk-11-jdk xvfb
# Perl
RUN apt -y install perl
# Create /.bashrc for aliases
# Execute ". /.bashrc" command right after the container is run
RUN touch /.bashrc
# FastQC v0.11.9
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && \
    unzip fastqc_v0.11.9.zip && \
    rm fastqc_v0.11.9.zip && \
    chmod a+x /FastQC/fastqc && \
    echo 'alias fastqc="/FastQC/fastqc"' >> /.bashrc # && \
# STAR v2.7.10b
RUN wget https://github.com/alexdobin/STAR/releases/download/2.7.10b/STAR_2.7.10b.zip && \
    unzip ./STAR_2.7.10b.zip && \
    rm ./STAR_2.7.10b.zip && \
    chmod a+x ./STAR_2.7.10b/Linux_x86_64_static/STAR ?? \
    mv ./STAR_2.7.10b/Linux_x86_64_static/STAR /bin/STAR && \
    rm -r ./STAR_2.7.10b
# samtools v1.16.1
RUN wget https://github.com/samtools/samtools/archive/refs/tags/1.16.1.zip -O ./samtools-1.16.1.zip && \
    unzip ./samtools-1.16.1.zip && \
    rm ./samtools-1.16.1.zip && \
    mv ./samtools-1.16.1/misc /samtools && \
    rm -r ./samtools-1.16.1 && \
    echo 'alias samtools="/samtools/samtools.pl"' >> /.bashrc
# picard v2.27.5
RUN wget https://github.com/broadinstitute/picard/releases/download/2.27.5/picard.jar -O /bin/picard.jar && \
    chmod a+x /bin/picard.jar && \
    echo 'alias picard="java -jar /bin/picard.jar"' >> /.bashrc
# bedrools v2.30.0
RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.30.0/bedtools.static.binary -O /bin/bedtools.static.binary && \
    chmod a+x /bin/bedtools.static.binary && \
    echo 'alias bedtools="/bin/bedtools.static.binary"' >> /.bashrc
# Python 3 with pip
RUN apt -y install python3-pip
# MultiQC v1.13
RUN pip install multiqc==1.13
# salmon v1.9.0 with libgomp1 and libtbb12 needed for its functioning
RUN wget https://github.com/COMBINE-lab/salmon/releases/download/v1.9.0/salmon-1.9.0_linux_x86_64.tar.gz && \
    tar -zxvf ./salmon-1.9.0_linux_x86_64.tar.gz && \
    rm salmon-1.9.0_linux_x86_64.tar.gz && \
    chmod a+x ./salmon-1.9.0_linux_x86_64/bin/salmon && \
    mv ./salmon-1.9.0_linux_x86_64/bin/salmon /bin/salmon && \
    rm -r ./salmon-1.9.0_linux_x86_64 && \
    apt install libgomp1 libtbb12
```
---


## 6. Use [hadolint](https://hadolint.github.io/hadolint/) litner to remove as many reported warnings as possible.

The list of changes:

1. Specified the version of Ubuntu.
2. MAINTAINER is deprecated. Replaced with the `LABEL author`.
3. Replaced `apt` with `apt-get` because `apt` is meant to be an end-user tool.
4. Added versions to all the installed packages.
5. Added `--no-install-recommends` to exclude all the unnecessary packages.

* [0.5] Add relevant [labels](https://docs.docker.com/engine/reference/builder/#label), e.g. maintainer, version, etc. ([hint](https://medium.com/@chamilad/lets-make-your-docker-image-better-than-90-of-existing-ones-8b1e5de950d))

Added version and description labels.

**[Dockerfile](Dockerfile_after) after linter**

*Warning! Execute `. /.bashrc` command right after the container is run for correct work of all aliases.*

---

```docker
FROM ubuntu:22.04
LABEL author="snitkin.d@list.ru"
LABEL version="1.0"
LABEL description="Container for the homework 1 in Computing Infrastructure in Bioinformatics Problems, HSE, 2022"
# Apt packages installation
RUN apt-get update && \
    # apt-utils
    apt-get -y --no-install-recommends install apt-utils=2.4.8 && \
    # apt-transport-https
    apt-get -y --no-install-recommends install apt-transport-https=2.4.8 && \
    # Wget
    apt-get -y --no-install-recommends install wget=1.21.2-2ubuntu1 && \
    # Unzip
    apt-get -y --no-install-recommends install unzip=6.0-26ubuntu3.1 && \
    # Python 3 with pip
    apt-get -y --no-install-recommends install python3-pip=22.0.2+dfsg-1 && \
    # Java
    apt-get -y --no-install-recommends install openjdk-11-jdk=11.0.17+8-1ubuntu2~22.04 && \
    apt-get -y --no-install-recommends install xvfb=2:21.1.3-2ubuntu2.3 && \
    # Perl
    apt-get -y --no-install-recommends install perl=5.34.0-3ubuntu1.1 && \
    # libgomp1 & libtbb12 (needed for salmon)
    apt-get -y --no-install-recommends install libgomp1=12.1.0-2ubuntu1~22.04 && \
    apt-get -y --no-install-recommends install libtbb12=2021.5.0-7ubuntu2 && \
    # Delete the apt-get lists
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Create /.bashrc for aliases
# Execute ". /.bashrc" command right after the container is run
RUN touch /.bashrc
# FastQC v0.11.9
RUN wget https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.11.9.zip && \
    unzip fastqc_v0.11.9.zip && \
    rm fastqc_v0.11.9.zip && \
    chmod a+x /FastQC/fastqc && \
    echo 'alias fastqc="/FastQC/fastqc"' >> /.bashrc # && \
# STAR v2.7.10b
RUN wget https://github.com/alexdobin/STAR/releases/download/2.7.10b/STAR_2.7.10b.zip && \
    unzip ./STAR_2.7.10b.zip && \
    rm ./STAR_2.7.10b.zip && \
    chmod a+x ./STAR_2.7.10b/Linux_x86_64_static/STAR ?? \
    mv ./STAR_2.7.10b/Linux_x86_64_static/STAR /bin/STAR && \
    rm -r ./STAR_2.7.10b
# samtools v1.16.1
RUN wget https://github.com/samtools/samtools/archive/refs/tags/1.16.1.zip -O ./samtools-1.16.1.zip && \
    unzip ./samtools-1.16.1.zip && \
    rm ./samtools-1.16.1.zip && \
    mv ./samtools-1.16.1/misc /samtools && \
    rm -r ./samtools-1.16.1 && \
    echo 'alias samtools="/samtools/samtools.pl"' >> /.bashrc
# picard v2.27.5
RUN wget https://github.com/broadinstitute/picard/releases/download/2.27.5/picard.jar -O /bin/picard.jar && \
    chmod a+x /bin/picard.jar && \
    echo 'alias picard="java -jar /bin/picard.jar"' >> /.bashrc
# bedrools v2.30.0
RUN wget https://github.com/arq5x/bedtools2/releases/download/v2.30.0/bedtools.static.binary -O /bin/bedtools.static.binary && \
    chmod a+x /bin/bedtools.static.binary && \
    echo 'alias bedtools="/bin/bedtools.static.binary"' >> /.bashrc
# MultiQC v1.13
RUN pip install multiqc==1.13
# salmon v1.9.0
RUN wget https://github.com/COMBINE-lab/salmon/releases/download/v1.9.0/salmon-1.9.0_linux_x86_64.tar.gz && \
    tar -zxvf ./salmon-1.9.0_linux_x86_64.tar.gz && \
    rm salmon-1.9.0_linux_x86_64.tar.gz && \
    chmod a+x ./salmon-1.9.0_linux_x86_64/bin/salmon && \
    mv ./salmon-1.9.0_linux_x86_64/bin/salmon /bin/salmon && \
    rm -r ./salmon-1.9.0_linux_x86_64
```
---
