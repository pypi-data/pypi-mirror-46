
============
Introduction
============

LED is a utility to generate TLS certificates from Let's Encrypt and install
them in Docker containers.


Objectives
----------

    1. Provide an elegant command-line interface for provisioning TLS certificates to Docker containers.
    2. Enable automatic renewal of Let's Encrypt certificates via Systemd Timer or Cron.
    3. Bootstrap web servers with self-signed certificates.
    4. Support both NGINX and Apache httpd

       👉 *Initial support will only be for NGINX* 👈

Installing
----------

Install and update using `pip`:

.. code-block:: bash

   pip install -U led


A Simple Example
----------------

.. code-block:: bash

   led create certs


Links
-----

* Website:
* Documentation:
* License: https://www.gnu.org/licenses/agpl.html
* Releases: https://pypi.org/project/led/
* Code: _To be released soon..._
* Issue tracker:
* Test status:
* Test coverage:
