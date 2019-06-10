class Power:
    """
    Power

    Singleton pattern
    """
    colName = ['name', 'manufacturer', 'standard', 'w', 'fan_size', 'fan_num', 'pfc', 'rail',
               'a', '4pin_ide', 'sata', '6+2pin_pci-e', 'as', 'img', 'etc', 'price']
    colIdentifier = ['', '', '파워', 'W', 'mm 팬', '개(팬)', 'PFC', '+12V',
                     'A', '4핀 IDE', 'SATA', '6+2핀 PCI-E', '무상', 'http']
    _instance = None

    @classmethod
    def _get_instance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._get_instance
        return cls._instance

    def __init__(self):
        self._dict = {col: "0" for col in self.colName}