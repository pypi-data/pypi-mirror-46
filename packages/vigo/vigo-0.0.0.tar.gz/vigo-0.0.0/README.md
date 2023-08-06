# vigo

[![Build Status](https://travis-ci.org/4383/vigo.svg?branch=master)](https://travis-ci.org/4383/vigo)
![PyPI](https://img.shields.io/pypi/v/vigo.svg)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/vigo.svg)
![PyPI - Status](https://img.shields.io/pypi/status/vigo.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Find code and files on openstack projects

vigo is a development tools that help you to get informations
about a given openstack group of projects.

vigo retrieve groups from [openstack governance](https://github.com/openstack/governance/blob/master/reference/projects.yaml).

## Features
- Search code on groups projects

## Install or Update vigo

```sh
$ pip install -U vigo
```

## Usage

Openstacker is automatically sync up with [the openstack governance repo](https://github.com/openstack/governance) to always provide results who corresponds to the latest openstack
updates and maintained projects.

Configuration of vigo is hosted in the `~/.vigo` repository in your
home.

```shell
$ # find occurence of string in groups of projects source code
$ # example: find which projects use bandit in specific versions on 
$ # the whole oslo and cloudkitty projects
$ stacker "bandit>=1.1.0,<1.6.0 # Apache-2.0" --groups oslo cloudkitty
Synchronize the vigo configuration...OK!
24 results found
~~~~~~~~~~~~~~~~
openstack/oslo.concurrency
test-requirements.txt (2ad43268fa8ec2aedc3176de8e30d9fa9ecfd056)
openstack/oslo.service
test-requirements.txt (1f12c102da8a402b4a8accc9029e03efae43f471)
openstack/oslo.utils
test-requirements.txt (ce63b708c2913b56f493d145e3204c507c70336f)
openstack/oslo.context
test-requirements.txt (123527191321361c2d67088a43424ae24febbd28)
openstack/oslo.versionedobjects
test-requirements.txt (e7a9a8b713bc9d212aae72dca594925dc3de9da1)
openstack/oslo.middleware
test-requirements.txt (6f0580b45fa1f2204a1f2d2af95fb4f7b8150a0b)
...
openstack/cloudkitty
test-requirements.txt (85fe57068270916a5a2e0c612ae2f87627056a97)
lower-constraints.txt (cf1beaddd4a315b0617cd33efdb528ace72b4ff0)
openstack/oslo.vmware
test-requirements.txt (044e6167a071d429689dcf19e94ee71fdcc344ce)
```

## Contribute

If you want to contribute to vigo [please first read the contribution guidelines](CONTRIBUTING.md)

## Licence

This project is under the MIT License.

[See the license file for more details](LICENSE)
