from ftw.upgrade import UpgradeStep


class AddMapPreferences(UpgradeStep):
    """Add map preferences.
    """

    def __call__(self):
        self.install_upgrade_profile()
