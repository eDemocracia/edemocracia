# e-Democracia

## Environment Setup

First of all, you need to install some dependencies on yout system:

```
# Fedora
sudo dnf install libxml2-devel libxslt-devel

# CentOS
sudo yum install libxml2-devel libxslt-devel

# Debian/Ubuntu
sudo yum install libxml2-dev libxslt-dev
```

We're using `pipenv` to manage our python dependencies, so you have to install it:

```
sudo pip install pipenv
```

And then install all project's dependencies:

```
pipenv install
```