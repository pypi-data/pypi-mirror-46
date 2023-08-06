from ftw.upgrade import UpgradeStep


class AddMissingPermissionForEditing(UpgradeStep):
    """Add missing permission for editing.
    """

    def __call__(self):
        self.install_upgrade_profile()
