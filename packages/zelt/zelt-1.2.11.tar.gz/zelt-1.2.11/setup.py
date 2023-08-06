# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['zelt', 'zelt.kubernetes', 'zelt.kubernetes.storage']

package_data = \
{'': ['*']}

modules = \
['main']
install_requires = \
['boto3>=1.9,<2.0',
 'docopt>=0.6.2,<0.7.0',
 'greenlet>=0.4.15,<0.5.0',
 'har-transformer>=1.0,<2.0',
 'kubernetes>=8.0,<9.0',
 'locustio>=0.9.0,<0.10.0',
 'pyyaml>=5.1,<6.0',
 'tenacity>=5.0,<6.0']

extras_require = \
{'docs': ['sphinx>=1.8,<2.0',
          'sphinx-autodoc-typehints>=1.6,<2.0',
          'sphinx-issues>=1.2,<2.0']}

entry_points = \
{'console_scripts': ['zelt = main:cli']}

setup_kwargs = {
    'name': 'zelt',
    'version': '1.2.11',
    'description': 'Zalando end-to-end load tester',
    'long_description': ".. image:: docs/_static/zelt.png\n    :alt: Zelt logo\n\nZalando end-to-end load tester\n******************************\n\n.. image:: https://travis-ci.org/zalando-incubator/zelt.svg?branch=master\n   :alt: travis-ci status badge\n   :target: https://travis-ci.org/zalando-incubator/zelt\n\n.. image:: https://badgen.net/pypi/v/zelt\n   :alt: pypi version badge\n   :target: https://pypi.org/project/zelt\n\n.. image:: https://api.codacy.com/project/badge/Grade/a74dee2bbbd64da8951a3cec5059dda3\n   :alt: code quality badge\n   :target: https://www.codacy.com/app/bmaher/zelt\n\n.. image:: https://api.codacy.com/project/badge/Coverage/a74dee2bbbd64da8951a3cec5059dda3\n   :alt: test coverage badge\n   :target: https://www.codacy.com/app/bmaher/zelt\n\n.. image:: https://badgen.net/badge/code%20style/black/000\n   :alt: Code style: Black\n   :target: https://github.com/ambv/black\n\n|\n\nA **command-line tool** for orchestrating the deployment of\nLocust_ in Kubernetes_.\n\nUse it in conjunction with Transformer_ to run large-scale end-to-end\nload testing of your website.\n\nPrerequistes\n============\n\n-  `Python 3.6+`_\n\nInstallation\n============\n\nInstall using pip:\n\n.. code:: bash\n\n   pip install zelt\n\nUsage\n=====\n\nExample HAR files, locustfile, and manifests are included in the\n``examples/`` directory, try them out.\n\n**N.B** The cluster to deploy to is determined by your currently\nconfigured context. Ensure you are `using the correct cluster`_\nbefore using Zelt.\n\nLocustfile as input\n-------------------\n\nZelt can deploy Locust with a locustfile to a cluster:\n\n.. code:: bash\n\n   zelt from-locustfile PATH_TO_LOCUSTFILE --manifests PATH_TO_MANIFESTS\n\nHAR files(s) as input\n---------------------\n\nZelt can transform HAR file(s) into a locustfile and deploy it along\nwith Locust to a cluster:\n\n.. code:: bash\n\n   zelt from-har PATH_TO_HAR_FILES --manifests PATH_TO_MANIFESTS\n\n**N.B** This requires\nTransformer_ to be installed. For more information about Transformer,\nplease refer to `Transformer's documentation`_.\n\nRescale a deployment\n--------------------\n\nZelt can rescale the number of workers_ in a deployment it has made\nto a cluster:\n\n.. code:: bash\n\n   zelt rescale NUMBER_OF_WORKERS --manifests PATH_TO_MANIFESTS\n\nDelete a deployment\n-------------------\n\nZelt can delete deployments it has made from a cluster:\n\n.. code:: bash\n\n   zelt delete --manifests PATH_TO_MANIFESTS\n\nRun Locust locally\n------------------\n\nZelt can also run Locust locally by providing the ``--local/-l`` flag to\neither the ``from-har`` or ``from-locustfile`` command e.g.:\n\n.. code:: bash\n\n   zelt from-locustfile PATH_TO_LOCUSTFILE --local\n\nUse S3 for locustfile storage\n-----------------------------\n\nBy default, Zelt uses a ConfigMap for storing the locustfile. ConfigMaps\nhave a file-size limitation of ~2MB. If your locustfile is larger than\nthis then you can use an S3 bucket for locustfile storage.\n\nTo do so, add the following parameters to your Zelt command:\n\n-  ``--storage s3``: Switch to S3 storage\n-  ``--s3-bucket``: The name of your S3 bucket\n-  ``--s3-key``: The name of the file as stored in S3\n\n**N.B.** Zelt will *not* create the S3 bucket for you.\n\n**N.B.** Make sure to update your deployment manifest(s) to download the\nlocustfile file from S3 instead of loading from the ConfigMap volume\nmount.\n\nUse a configuration file for Zelt options\n-----------------------------------------\n\nAn alternative to specifying Zelt’s options on the command-line is to\nuse a configuration file, for example:\n\n.. code:: bash\n\n   zelt from-har --config examples/config/config.yaml\n\n**N.B.** The configuration file’s keys are the same as the command-line\noption names but without the double dash (``--``).\n\nDocumentation\n=============\n\nTake a look at our documentation_ for more details.\n\nContributing\n============\n\nPlease read `CONTRIBUTING.md <CONTRIBUTING.md>`__ for details on our\nprocess for submitting pull requests to us, and please ensure you follow\nthe `CODE_OF_CONDUCT.md <CODE_OF_CONDUCT.md>`__.\n\nVersioning\n==========\n\nWe use SemVer_ for versioning.\n\nAuthors\n=======\n\n-  **Brian Maher** - `@bmaher`_\n-  **Oliwia Zaremba** - `@tortila`_\n-  **Thibaut Le Page** - `@thilp`_\n\nSee also the list of `contributors <CONTRIBUTORS.md>`__ who participated\nin this project.\n\nLicense\n=======\n\nThis project is licensed under the MIT License - see the\n`LICENSE <LICENSE>`__ file for details\n\n.. _Locust: https://locust.io/\n.. _Kubernetes: https://kubernetes.io/\n.. _Transformer: https://github.com/zalando-incubator/transformer\n.. _`Python 3.6+`: https://www.python.org/downloads/\n.. _`using the correct cluster`: https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration\n.. _`Transformer's documentation`: https://transformer.readthedocs.io/\n.. _workers: https://docs.locust.io/en/stable/running-locust-distributed.html\n.. _documentation: https://zelt.readthedocs.io/\n.. _`@bmaher`: https://github.com/bmaher\n.. _`@tortila`: https://github.com/tortila\n.. _`@thilp`: https://github.com/thilp\n.. _SemVer: http://semver.org/\n",
    'author': 'Brian Maher',
    'author_email': 'brian.maher@zalando.de',
    'url': 'https://github.com/zalando-incubator/zelt',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
