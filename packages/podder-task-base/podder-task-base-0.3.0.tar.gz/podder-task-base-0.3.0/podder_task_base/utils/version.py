def get_version(version=None):
    """Return version X.Y[.Z] from VERSION."""
    version = get_complete_version(version)
    parts = 2 if version[2] == 0 else 3
    return '.'.join(str(x) for x in version[:parts])


def get_complete_version(version=None):
    if version is None:
        from podder_task_base import VERSION as version
    else:
        assert len(version) == 3
    return version
