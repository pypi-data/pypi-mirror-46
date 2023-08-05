import pkgutil

def version():
    a = pkgutil.get_data(__package__, 'version/A-major').strip()
    b = pkgutil.get_data(__package__, 'version/B-minor').strip()
    c = pkgutil.get_data(__package__, 'version/C-patch').strip()
    return '{}.{}.{}'.format(
        a.decode('utf-8'), b.decode('utf-8'), c.decode('utf-8'))