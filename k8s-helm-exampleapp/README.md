## Example of deploying an micro-services "application and database" using Helm in a cluster Kubernetes.

      This application is intended for the practical mastering of Kubernetes and Helm.
  ---

## Cluster Requirements

Kubernetes runs in a variety of environments and is inherently
modular. Not all clusters are the same. These are the requirements for
this example.

* Minikube or Kubernetes version 1.2 is required due to using newer features, such
  at PV Claims and Deployments. Run `kubectl version` to see your
  cluster version.
* [Cluster DNS](https://github.com/kubernetes/dns) will be used for service discovery.
* Helm
* Make
* If you want to collect images something you need `docker`

## Table of Contents

<!-- BEGIN MUNGE: GENERATED_TOC -->

- [Cluster Requirements](#cluster-requirements)
  - [Table of Contents](#table-of-contents)
  - [The application consists of two micro-services](#the-application-consists-of-two-micro-services)
  - [What is  Helm ?](#what-is-helm-?)
  - [Preparation of the necessary environment for their work station](#preparation-of-the-necessary-environment-for-their-work-stations)
  - [Deploy micro blog using make and helm](#deploy-micro-blog-using-make-and-helm)

<!-- END MUNGE: GENERATED_TOC -->

## The application consists of two micro-services:

What would you understand that there is no need for additional magic, for the implementation of applications in ***Kubernetes***  using ***Helm***. I took side projects for the implementation of micro services and realized with the help of their data an example.

1. Service application  just a microblogging web application written in ***Python*** and ***Flask***, implemented to demonstrate the work with the database, works through ***uwsgi***. This application you find on [github](https://github.com/miguelgrinberg/microblog) and in my opinion the best tutorial you will find  [The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). I took the application from this excellent guy in an unchanged state, the second step i just added a simple authentication mechanism by name and password, because by default in the tutorial uses type authentication openid, which is not very convenient for the example.

2. Database postgresql for data storage, this application uses the scheme of working with type of storage **hostPath** for minikube and **nfs** for a full cluster kubernetes - on deployed on your local machine or remotely. I took the implementation of creating an docker image for the database here [docker-alpine-postgres](https://github.com/kiasaki/docker-alpine-postgres).
In this project, everything is simple and intuitive, one script ***docker-entrypoint.sh*** that initializes the database at startup

**Micro services interconnection**

<img src="https://github.com/JuggleClouds/Cloud-practice/raw/master/k8s-helm-exampleapp/shema micro service.png">
When a request comes from the client, it gets into the application service, applications can be located on any of the physical nodes, if suddenly the server or application to fall down, the application automatically self-settles on the other server through the cluster. The same thing happens with the database, plus the database has its own permanent store remain in the same state.
<br>

**Basic objects of Kubernetes which are used in this application**:

* [Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/) to
  define persistent disks (disk lifecycle not tied to the Pods).
* [Services](https://kubernetes.io/docs/concepts/services-networking/service/) to enable Pods to
  locate one another.
* [External IP](https://kubernetes.io/docs/concepts/services-networking/service/#type-externalIps)
  to expose Services externally.
* [Deployments](http://kubernetes.io/docs/user-guide/deployments/) to ensure Pods
  stay up and running.
* [Secrets](http://kubernetes.io/docs/user-guide/secrets/) to store sensitive
  passwords.
---
<br>

> `The application will be deployed to the kubernetes using a helm so that i make a small intro to helm.`

### What is  Helm ?

[Docks Helm](https://docs.helm.sh/using_helm/#quickstart-guide)

There are package managers apt, yum, dnf, homebrew etc, for a convenient turn of the application on operating systems. Helm this is also the same for Kubernetes, Helm is a tool that simplifies the installation and management of applications Kubernetes.

* Helm consists of two parts of client and server:
  - To install the client part of the helm on its workstation, just download the bin file for your system from [GitRepoHelm](https://github.com/kubernetes/helm), give this file the right to write a ``chmod u+x helm`` and put the helm (bin file) in you ``PATH:`` to the application folder ex.. ``/usr/local/bin``. You can get acquainted with the full instruction on installation here [install helm](https://docs.helm.sh/using_helm/#installing-helm).
  - The server part (tiller) consists of deployed in the kubernetes, the server part is installed simply by command ``helm init``, one thing you need to perform this command only when you have a cluster installed.
---

### Preparation of the necessary environment for their work stations

</br>

1. First you need to download and install minikube on your machine, just click on the link  [minikube ](https://github.com/kubernetes/minikube/releases), there are versions for all operating systems and commands for installation. Install a virtual environment in your OS, minikube requires:

  * OS X
    - xhyve driver, VirtualBox or VMware Fusion installation
  * Linux
    - VirtualBox or KVM installation,
  * Windows
    - Hyper-V
  * VT-x/AMD-v virtualization must be enabled in BIOS

   > If there are problems with installing the virtual environment in the OS, you need to disable the secure boot in the BIOS (UEFI) or generate the keys for the secure boot.

2. Run the minikube command from the console ``minikube start``, minikube create a virtual machine and run it kubernetes, it will add everything you need credentials to access the cluster kubernetes to a file ``~/.kube/config``.

3. Then you can add auto-completion for **minikube** by the following instructions [minikube_completion](https://github.com/kubernetes/minikube/blob/master/docs/minikube_completion.md), this item can be made at will, the functionality simply installs auto-completions for **minikube**.

3. Already today you can manage the cluster, using ``kubectl``, to test the health of the cluster, you can run command ``kubectl get nodes``, as a result of the command, the node should give out a node, for example ``minikube   Ready     9d`` or execute the command ``kubectl get po -n kube-system``, in the output will be all the system pods for the cluster, well and at last ``kubectl --help``, plus do not forget to use the autocompletion of commands on the button ``tab``.

5. Next, you need to install Helm on your machine, just download bin files to your ``/usr/local/bin`` from here [helm](https://github.com/kubernetes/helm),For the user and ***OSX***, you can simply run command ``brew install kubernetes-helm``.

6. Install **Helm** server "**tiller**" in our new cluster, just run  command ``helm init``. After executing this command, you can see in the cluster what appeared under the pod **tiller** - execute the command ``kubectl get all -n kube-system`` we can see that the new "tiller" has appeared here is an example of the conclusion ``rs/tiller-deploy-3299276078``

7. Copy the application itself [microblog](https://github.com/JuggleClouds/Cloud-practice/tree/master/k8s-helm-exampleapp).

8. Go to directory ``./k8s-helm-exampleapp``, in file ``values.yaml`` In the section ``app`` change parameter ''externalIPs'' on ip address which displays the command ``minikube ip``.

 > :warning: The type of persistent volume on the minikube is only available **hostPath**. This step is optional, it is intended only for clusters kubernetes that are not deployed with the help of minikube, to connect the nfs disk with data storage for the database. Here we will configure nfs for centos, but it will not be difficult for other operating systems to find instructions on the Internet

 * Now if it is necessary that the database had a real and nfs disk and the data was stored on it, you first need to raise the nfs drive:
    1. The system should be set up as root. You can access the root user by typing ```sudo su```<p>
    2. Step One—Download the Required Software ``` yum install nfs-utils nfs-utils-lib ```<p>
    3. Subsequently, run several startup scripts for the NFS server:<p> ```chkconfig nfs on``` or ```systemctl enable nfs```   
    ```service rpcbind start``` or ```systemctl status  rpcbind```  
    ```service nfs start``` or ```systemctl start nfs```
    4. The next step is to decide which directory we want to share with the client server. The chosen directory should then be added to the /etc/exports file, which specifies both the directory to be shared and the details of how it is shared.<p>
    Suppose we wanted to share the directory, **/opt/exampleapp**  
    Creating this directory ```sudo mkdir -p  /opt/exampleapp```
    5. We need to export the directory:  
    ```vi /etc/exports```  
    Add the following lines to the bottom of the file, sharing the directory with the client:  
    ```/mnt/exampleapp  *(rw,sync)``` or ```/mnt/exampleapp  "ip you nfs server"(rw,sync)```  
    These settings accomplish several tasks:
      * To get the client node address, you need to run the command, In the result we get the following addresses ```192.168.99.100```
      * ``rw``: This option allows the client server to both read and write within the shared directory
      * ``sync``: Sync confirms requests to the shared directory only once the changes have been committed.
      * ``no_subtree_check``: This option prevents the subtree checking. When a shared directory is the subdirectory of a larger filesystem, nfs performs scans of every directory above it, in order to verify its permissions and details. Disabling the subtree check may increase the reliability of NFS, but reduce security.
      * ``no_root_squash``: This phrase allows root to connect to the designated directory   
      > All the parameters for the NFS can be seen here [nfs options](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/5/html/Deployment_Guide/s1-nfs-server-config-exports.html)
      * Once you have entered in the settings for each directory, run the following command to export them: ```exportfs -a```<p>  
 * In file ``values.yaml``  in section  ``db`` -> ``Persistence`` set up parameter ``Enabled`` on ``true``. You need to comment out the parameters ```type: hostpath```, ```path: "/tmp/data/pv-1"``` Uncomment settings ```type: nfs``` and change parameters **nfspath: /opt/exampleapp** and **nfsserver: "ip you nfs server"**  on their. If database does not need a persistent disk then in the section ``db`` -> ``Persistence`` set up parameter ``Enabled`` on ``false``.
</br>

### Deploy micro blog using make and helm
</br>

In this project, to simplify the assembly of the docker images and the reversal using the helm, all commands and variables are combined in one Makefile. This is for us a mini pipeline **cd - continuous deployment**, the make is used here to avoid becoming attached to the more cumbersome **cd** systems. To see all the commands of our mini pipeline you can simply by running the command ``make help``.

1. Install the application - go to directory ``./k8s-helm-exampleapp`` , run the command ``make run``.

4. Check ``make status`` or ``kubectl get all -n exampleapp``.

5. Now when the application needs to migrate data to the database run command ``kubectl get pod -n exampleapp``. From the list we need pod with app title example  **blog-exampleapp-***.

6. Let's get into the self under by using kubectl and perform data migration. Run comand ``kubectl -n exampleapp exec blog-exampleapp-***   -i -t -- bash -il``, now when we log into the container, we perform data migration to the database ``python ./db_create.py && python ./db_migrate.py``

7. By ip from the result of the command ``minikube ip`` Go through the browser, see the application. Now you need to register in the system register, then enter. You can also log into the system through the location ``/loginopenid`` in this case, the authentication using the openid login can register an account with yahoo, aol or flickr.

8. When you want to remove applications, simply run the command ``make purge``.
