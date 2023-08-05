from bigga.contrib.patchwork.info import distro_family


def update_index(cxn):
    """
    Update APT package definitions.
    """
    if distro_family(cxn) == "debian":
        cxn.run('DEBIAN_FRONTEND=noninteractive sudo apt-get update')
    else:
        cxn.run('sudo yum update')


def is_installed(cxn, pkg_name):
    """
    Check if a package is installed.
    """
    # TODO: support yum
    res = cxn.run("dpkg -s %(pkg_name)s" % locals())
    res = res.result.strip()
    for line in res.splitlines():
        if line.startswith("Status: "):
            status = line[8:]
            if "installed" in status.split(' '):
                return True
    return False


def package(c, *packages):
    """
    Installs one or more ``packages`` using the system package manager.
    Specifically, this function calls a package manager like ``apt-get`` or
    ``yum`` once per package given.
    """
    # Try to suppress interactive prompts, assume 'yes' to all questions
    apt = "DEBIAN_FRONTEND=noninteractive apt-get install -y {}"
    # Run from cache vs updating package lists every time; assume 'yes'.
    yum = "yum install -y %s"
    manager = apt if distro_family(c) == "debian" else yum
    for package in packages:
        c.sudo(manager.format(package))


def packages(cxn, package_list):
    for _package in package_list:
        package(cxn, _package)
