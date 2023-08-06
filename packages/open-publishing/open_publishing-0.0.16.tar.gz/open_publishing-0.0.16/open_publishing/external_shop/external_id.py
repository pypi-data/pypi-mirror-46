"""Module for using the external_id interface of the external shop service."""

from .external_shop import ExternalShop


class ExternalID(ExternalShop):
    """Class to send and get the external_d to the external shop service."""

    def set_external_id(self, shop: str, ean: str, external_id: str) -> None:
        """Set external_id of specified EAN of the shop."""
        self.put_request(urlpath='external_id/{}/{}'.format(shop, ean),
                         data={'external_id': external_id})

    def get_external_id(self, shop: str, ean: str) -> str:
        """Get the external_id for the specified shop, EAN."""
        return self.get_request_field(urlpath='external_id/{}/{}'.format(shop, ean),
                                      fieldname='external_id')
