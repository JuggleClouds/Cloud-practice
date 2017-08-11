## Example of deploying an micro-services "application and database" using Helm in a cluster Kubernetes.

      This application is intended for the practical mastering of Kubernetes and Helm.
  ---
### The application consists of two micro-services:

What would you understand that there is no need for additional magic, for the implementation of applications in ***Kubernetes***  using ***Helm***. I took side projects for the implementation of micro services and realized with the help of their data an example.

1. Service application  just a microblogging web application written in ***Python*** and ***Flask***, implemented to demonstrate the work with the database, works through ***uwsgi***. This application you find on [github](https://github.com/miguelgrinberg/microblog) and in my opinion the best tutorial you will find  [The Flask Mega-Tutorial, Part I: Hello, World!](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world). I took the application from this excellent guy in an unchanged state, the second step i just added a simple authentication mechanism by name and password, because by default in the tutorial uses type authentication openid, which is not very convenient for the example.

2. Database postgresql for data storage, this application uses the scheme of working with nfs disk - on deployed on your local machine or remotely. I took the implementation of creating an docker image for the database here [docker-alpine-postgres](https://github.com/kiasaki/docker-alpine-postgres).
In this project, everything is simple and intuitive, one script ***docker-entrypoint.sh*** that initializes the database at startup

**Micro services interconnection **:


<img src="https://github.com/JuggleClouds/Cloud-practice/raw/master/k8s-helm-exampleapp/shema micro service.png">
When a request comes from the client, it gets into the application service, applications can be located on any of the physical nodes, if suddenly the server or application to fall down, the application automatically self-settles on the other server through the cluster. The same thing happens with the database, plus the database has its own permanent store remain in the same state.

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
> `The application will be deployed to the kubernetes using a helm so that i make a small intro to helm.`

### What is  Helm ?

[Docks Helm](https://docs.helm.sh/using_helm/#quickstart-guide)

There are package managers apt, yum, dnf, homebrew etc, for a convenient turn of the application on operating systems. Helm this is also the same for Kubernetes, Helm is a tool that simplifies the installation and management of applications Kubernetes.

* Helm consists of two parts of client and server:
  - To install the client part of the helm on its workstation, just download the bin file for your system from [GitRepoHelm](https://github.com/kubernetes/helm), give this file the right to write a ``chmod u+x helm`` and put the helm (bin file) in you ``PATH:`` to the application folder ex.. ``/usr/local/bin``. You can get acquainted with the full instruction on installation here [install helm](https://docs.helm.sh/using_helm/#installing-helm).
  - The server part (tiller) consists of deployed in the kubernetes, the server part is installed simply by command ``helm init``, one thing you need to perform this command only when you have a cluster installed.
---
### Deploy micro blog
</br>

#### Preparation of the necessary environment for their work stations
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

8. Go to directory ``./k8s-helm-exampleapp``, in file ``values.yaml`` In the section ``app`` change parameter ''externalIPs'' on ip address which displays the command ``minikube ip``. Now if it is necessary that the database had a real and nfs disk and the data was stored on it, you first need to raise the nfs drive example instruction how to do it on OS centos here [nfsdisk-gaid](https://www.digitalocean.com/community/tutorials/how-to-set-up-an-nfs-mount-on-centos-6), in file ``values.yaml``  in section  ``db`` -> ``Persistence`` set up parameter ``Enabled`` on ``true`` and change parameters ``nfspath`` and ``nfsserver`` on their. If database does not need a persistent disk then in the section ``db`` -> ``Persistence`` set up parameter ``Enabled`` on ``fasle``.
</br>
</br>

#### Install the application using make and helm
</br>

1. Install the application - go to directory ``./k8s-helm-exampleapp`` , run the command ``make run``. All variables and commands for assembling and operating the project are described in **Makefile**, a description of the commands can be viewed by running the command ``make help`` .

4. Check ``make status`` or ``kubectl get all -n exampleapp``.

5. Now when the application needs to migrate data to the database run command ``kubectl get pod -n exampleapp``. From the list we need pod with app title example  **blog-exampleapp-***.

6. Let's get into the self under by using kubectl and perform data migration. Run comand ``kubectl -n exampleapp exec blog-exampleapp-***   -i -t -- bash -il``, now when we log into the container, we perform data migration to the database ``python ./db_create.py && python ./db_migrate.py``

7. By ip from the result of the command ``minikube ip`` Go through the browser, see the application. Now you need to register in the system register, then enter. You can also log into the system through the location ``/loginopenid`` in this case, the authentication using the openid login can register an account with yahoo, aol or flickr.

8. When you want to remove applications, simply run the command ``make purge``.
