from ftw.upgrade import UpgradeStep


class AddEventsArchivePortlet(UpgradeStep):
    """Add events archive portlet.
    """

    def __call__(self):
        self.install_upgrade_profile()
