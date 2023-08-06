`RedLock <https://redlock.io/>`_ API Client
===========================================

``rlock`` is a python package which integrates with parts of the API of the
RedLock Public Cloud Security service.

.. code-block:: bash

    >>>from rlock.api import Client
    >>>c = Client("scott@oracle.com", "tiger", "https://api.redlock.io/")
    >>>for policy in c.policies.take(5):
    ...    print(f"{policy.policyId}: {policy.name}")
    43c42760-5283-4bc4-ac43-a80e58c4139f: AWS S3 bucket has global view ACL permissions enabled
    472e08a2-c741-43eb-a3ca-e2f5cd275cf7: Azure Network Security Group allows FTP (TCP Port 21)
    91c941aa-d110-4b33-9934-aadd86b1a4d9: AWS Redshift database does not have audit logging enabled
    f5b4b962-e053-4e73-94d2-c21bd2520a0d: AWS ElastiCache cluster not associated with VPC
    fe81b03a-c602-4b16-8ae9-973724c1adae: GCP Kubernetes Engine Clusters web UI/Dashboard is set to Enabled

Installation
------------
``pip install rlock``

Documentation
-------------
https://rlock.readthedocs.org/
