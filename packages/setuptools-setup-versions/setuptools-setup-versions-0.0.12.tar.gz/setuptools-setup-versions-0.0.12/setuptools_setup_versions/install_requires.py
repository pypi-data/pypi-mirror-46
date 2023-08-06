import os

import re, pkg_resources
from warnings import warn

from . import find, parse

try:
    from collections import Sequence, Optional
except ImportError:
    Sequence = Optional = None


def update_versions(package_directory_or_setup_script=None, default_operator=None):
    # type: (Optional[str], Optional[str]) -> bool
    """
    Update setup.py installation requirements to (at minimum) require the version of each referenced package which is
    currently installed.

    Parameters:

        package_directory_or_setup_script (str):

            The directory containing the package. This directory must include a file named "setup.py".

    Returns:

         `True` if changes were made to setup.py, otherwise `False`
    """

    setup_script_path = find.setup_script_path(package_directory_or_setup_script)

    with open(setup_script_path) as setup_file:  # Read the current `setup.py` configuration

        setup_file_contents = setup_file.read()  # Retains the original setup file content for later comparison
        new_setup_file_contents = setup_file_contents  # This is the content which will be manipulated

        for setup_call in parse.setup_calls(
            setup_file_contents,
            name_space=dict(
                __file__=os.path.abspath(setup_script_path)
            )
        ):
            if 'install_requires' in setup_call:

                original_source = str(setup_call)
                install_requires = []
                missing_packages = []

                for requirement in setup_call['install_requires']:

                    # Parse the requirement string
                    parts = re.split(r'([<>=]+)', requirement)

                    if len(parts) == 3:  # The requirement includes a version
                        referenced_package, operator, version = parts
                    else:  # The requirement does not yet include a version
                        referenced_package = parts[0]
                        if '@' in referenced_package:
                            operator = version = None
                        else:
                            operator = default_operator
                            version = '0' if default_operator else None

                    referenced_package_name = referenced_package.split('@')[0]

                    # Determine the package version currently installed for this resource
                    try:
                        version = pkg_resources.get_distribution(referenced_package_name).version
                    except pkg_resources.DistributionNotFound:
                        missing_packages.append(referenced_package_name)

                    if operator:
                        install_requires.append(referenced_package + operator + version)
                    else:
                        install_requires.append(referenced_package)

                setup_call['install_requires'] = install_requires

                new_source = str(setup_call)

                if original_source != new_source:

                    new_setup_file_contents = new_setup_file_contents.replace(
                        original_source,
                        new_source
                    )

                if missing_packages:
                    warn(
                        'The following packages were not present in the source environment, and therefore a version ' +
                        'could not be inferred: ' + ', '.join(missing_packages)
                    )

    updated = False  # type: bool

    if new_setup_file_contents != setup_file_contents:
        with open('./setup.py', 'w') as setup_file:
            setup_file.write(new_setup_file_contents)
            updated = True

    return updated
