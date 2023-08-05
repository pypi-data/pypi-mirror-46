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

entry_points = \
{'console_scripts': ['zelt = main:cli']}

setup_kwargs = {
    'name': 'zelt',
    'version': '1.2.4',
    'description': 'Zalando end-to-end load tester',
    'long_description': '<p align="center"><img src="images/zelt.png"/></div>\n\n## Zalando end-to-end load tester\n\nA **command-line tool** for orchestrating the deployment of [Locust][] in [Kubernetes][].\n\nUse it in conjunction with [Transformer][] to run large-scale end-to-end load testing of your website.\n\n### Prerequistes\n\n- [Python 3.6+][]\n\n### Installation\n\nInstall using pip:\n\n```bash\npip install zelt\n```\n\n### Usage\n\nExample HAR files, locustfile, and manifests are included in the `examples/` directory, try them out.\n\n**N.B** The cluster to deploy to is determined by your currently configured context. Ensure you are [using the correct cluster][] before using Zelt.\n\n#### Locustfile as input\n\nZelt can deploy Locust with a locustfile to a cluster:\n\n```bash\nzelt from-locustfile PATH_TO_LOCUSTFILE --manifests PATH_TO_MANIFESTS\n```\n\n#### HAR files(s) as input\n\nZelt can transform HAR file(s) into a locustfile and deploy it along with Locust to a cluster:\n\n```bash\nzelt from-har PATH_TO_HAR_FILES --manifests PATH_TO_MANIFESTS\n```\n\n**N.B** This requires [Transformer][] to be installed. For more information about Transformer, please refer to its [documentation][].\n\n#### Rescale a deployment\n\nZelt can rescale the number of [workers][] in a deployment it has made to a cluster:\n\n```bash\nzelt rescale NUMBER_OF_WORKERS --manifests PATH_TO_MANIFESTS\n```\n\n#### Delete a deployment\n\nZelt can delete deployments it has made from a cluster:\n\n```bash\nzelt delete --manifests PATH_TO_MANIFESTS\n```\n\n#### Run Locust locally\n\nZelt can also run Locust locally by providing the `--local/-l` flag to either the `from-har` or `from-locustfile` command e.g.:\n\n```bash\nzelt from-locustfile PATH_TO_LOCUSTFILE --local\n```\n\n#### Use S3 for locustfile storage\n\nBy default, Zelt uses a ConfigMap for storing the locustfile. ConfigMaps have a file-size limitation of ~2MB. If your locustfile is larger than this then you can use an S3 bucket for locustfile storage.\n\nTo do so, add the following parameters to your Zelt command:\n\n- `--storage s3`: Switch to S3 storage\n- `--s3-bucket`: The name of your S3 bucket\n- `--s3-key`: The name of the file as stored in S3\n\n**N.B.** Zelt will _not_ create the S3 bucket for you.\n\n**N.B.** Make sure to update your deployment manifest(s) to download the locustfile file from S3 instead of loading from the ConfigMap volume mount.\n\n#### Use a configuration file for Zelt options\n\nAn alternative to specifying Zelt\'s options on the command-line is to use a configuration file, for example:\n\n```bash\nzelt from-har --config examples/config/config.yaml\n```\n\n**N.B.** The configuration file\'s keys are the same as the command-line option names but without the double dash (`--`).\n\n### Documentation\n\nComing soon...\n\n### Contributing\n\nPlease read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our process for submitting pull requests to us, and please ensure you follow the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).\n\n### Versioning\n\nWe use [SemVer][] for versioning.\n\n### Authors\n\n- **Brian Maher** - [@bmaher][]\n- **Oliwia Zaremba** - [@tortila][]\n- **Thibaut Le Page** - [@thilp][]\n\nSee also the list of [contributors](CONTRIBUTORS.md) who participated in this project.\n\n### License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n[Locust]: https://locust.io/\n[Kubernetes]: https://kubernetes.io/\n[Transformer]: https://github.com/zalando-incubator/transformer\n[Python 3.6+]: https://www.python.org/downloads/\n[using the correct cluster]: https://kubernetes.io/docs/reference/kubectl/cheatsheet/#kubectl-context-and-configuration\n[documentation]: https://transformer.readthedocs.io/\n[workers]: https://docs.locust.io/en/stable/running-locust-distributed.html\n[@bmaher]: https://github.com/bmaher\n[@tortila]: https://github.com/tortila\n[@thilp]: https://github.com/thilp\n[SemVer]: http://semver.org/\n',
    'author': 'Brian Maher',
    'author_email': 'brian.maher@zalando.de',
    'url': 'https://github.com/zalando-incubator/zelt',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
