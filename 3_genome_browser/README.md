# Genome browser on a remote server

Deploy the genome browser on a remote server.

## 1. Create a new virtual machine in the Yandex/Mail/etc cloud (order at least 10GB of free disk space). Generate SSH key pair and use it to connect to your server.

Create a new virtual machine in the Yandex Cloud, chose these paramenets:

|OS|Type|Size|vCPU|RAM|
|---|---|---|---|---|
|Ubuntu 22.04|HDD|20 Gb|2|6 Gb

Create private and public keys with the command `ssh-keygen -t ed25519` as recommended [here](https://cloud.yandex.ru/docs/compute/operations/vm-connect/ssh). Press Enter three times to skip all.

Print the public key: `cat ~/.ssh/id_ed25519.pub`. That's how it looks:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIIyMEc6lQmNceItLElloyFPeXmGPvhxN9oeBO7x/P+QP snitkin@snitkin-NBR-WAX9
```

Copy and enter the key in the corresponding field to create a new virtual machine.

Connect to server by user name (`dvsnitkin`) and IP (`158.160.19.14`):

`ssh dvsnitkin@158.160.19.14`

## 2. Download the latest human genome assembly (GRCh38) from the Ensemble FTP server ([fasta](https://ftp.ensembl.org/pub/release-108/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz), [GFF3](https://ftp.ensembl.org/pub/release-108/gff3/homo_sapiens/Homo_sapiens.GRCh38.108.gff3.gz)). Index the fasta using samtools (`samtools faidx`) and GFF3 using tabix.

Download the human genome and unzip:

```
wget https://ftp.ensembl.org/pub/release-108/fasta/homo_sapiens/dna/Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz
wget https://ftp.ensembl.org/pub/release-108/gff3/homo_sapiens/Homo_sapiens.GRCh38.108.gff3.gz
gunzip *
```

Install samtools and tabix.

```
sudo apt-get install -y samtools
sudo apt-get install -y tabix
```

Index FASTA files:

```
samtools faidx Homo_sapiens.GRCh38.dna.primary_assembly.fa
```

Sort, zip the GFF3 file as prescribed [here](http://www.htslib.org/doc/tabix.html) and index with tabix:

```
in_gff=Homo_sapiens.GRCh38.108.gff3
(grep "^#" $in_gff; grep -v "^#" $in_gff | sort -t"`printf '\t'`" -k1,1 -k4,4n) | bgzip > sorted.$in_gff.gz;
tabix -p gff sorted.$in_gff.gz;
```

## 3. Select and download BED files for three ChIP-seq and one ATAC-seq experiment from the ENCODE (use one tissue/cell line). Sort, bgzip, and index them using tabix.

Cell line: **A549**

<u>ATAC-seq</u>: https://www.encodeproject.org/experiments/ENCSR288YMH/

<u>ChIP-seq</u>

**JUNB**

https://www.encodeproject.org/experiments/ENCSR656VWZ/

**CTCF**

https://www.encodeproject.org/experiments/ENCSR432AXE/

**EP300**

https://www.encodeproject.org/experiments/ENCSR044IFH/

Download three ChIP-seq and one ATAC-seq BED files.

```
wget https://www.encodeproject.org/files/ENCFF619XXH/@@download/ENCFF619XXH.bed.gz -O atac.bed.gz
wget https://www.encodeproject.org/files/ENCFF536CDN/@@download/ENCFF536CDN.bed.gz -O JUNB.bed.gz
wget https://www.encodeproject.org/files/ENCFF824SNC/@@download/ENCFF824SNC.bed.gz -O CTCF.bed.gz
wget https://www.encodeproject.org/files/ENCFF448IBS/@@download/ENCFF448IBS.bed.gz -O EP300.bed.gz
gunzip *.bed.gz
```

Sort, bgzip and index the BED files with tabix:

```
for c in atac JUNB CTCF EP300
do
    (grep "^#" $c.bed; grep -v "^#" $c.bed | sort -t"`printf '\t'`" -k1,1 -k4,4n) | bgzip > sorted.$c.bed.gz;
    tabix -p bed sorted.$c.bed.gz;
done
```


## 4. Download and install [JBrowse 2](https://jbrowse.org/jb2/). Create a new jbrowse [repository](https://jbrowse.org/jb2/docs/cli/#jbrowse-create-localpath) in `/mnt/JBrowse/` (or some other folder).

Install conda:

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

Install JBrowse 2 via conda:

```
miniconda3/bin/conda install -c bioconda jbrowse2
```

Create a jbrowse repository:

```
sudo /home/dvsnitkin/miniconda3/bin/jbrowse create /var/www/html/jbrowse/
```

## 5. Install nginx and amend its config(/etc/nginx/nginx.conf) to contain the following section:
```
http {
  # Don't touch other options!
  # ........
  # ........

  # Add this:
  server {
		listen 80;
		index index.html;

		location /jbrowse/ {
			alias /mnt/JBrowse/;
		}
	}

  # ........
}
```

Install [nginx](https://nginx.org/):

```
sudo apt-get install -y nginx
```

Change the config:

```
sudo nano /etc/nginx/nginx.conf
```

I add only this code because I don't need alias for JBrowse to be accessed:

```
server {
    listen 80;
    index index.html;
}
```


## 6. Restart the nginx (reload its config) and make sure that you can access the browser using a link like this: `http://64.129.58.13/jbrowse/`. Here `64.129.58.13` is your public IP address.

Reload nginx:

```
sudo nginx -s reload
```

The link `http://158.160.19.14/jbrowse/` is now working.

## 7. Add your files to the genome browser and verify that everything works as intended. Don't forget to [index](https://jbrowse.org/jb2/docs/cli/#jbrowse-text-index) the genome annotation, so you could later search by gene names.

Add the genome assembly:

```
sudo /home/dvsnitkin/miniconda3/bin/jbrowse add-assembly /home/dvsnitkin/Homo_sapiens.GRCh38.dna.primary_assembly.fa --load copy --out /var/www/html/jbrowse/
```

Index the genome annotation:

```
sudo /home/dvsnitkin/miniconda3/bin/jbrowse text-index --file=/home/dvsnitkin/sorted.Homo_sapiens.GRCh38.108.gff3.gz
```

Add tracks:

```
for c in atac JUNB CTCF EP300
do
    sudo /home/dvsnitkin/miniconda3/bin/jbrowse add-track sorted.$c.bed.gz --load copy --out /var/www/html/jbrowse
done
```

Genome browser is now working!
