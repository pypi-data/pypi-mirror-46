def home_directory(cxn):
    """
    Get the absolute path to the user's home directory
    Example::
        from bigga.contrib.fabtools import home_directory
        home = home_directory(cxn, 'alice')
    """
    result = cxn.run('echo ~')
    return result.stdout.strip()
