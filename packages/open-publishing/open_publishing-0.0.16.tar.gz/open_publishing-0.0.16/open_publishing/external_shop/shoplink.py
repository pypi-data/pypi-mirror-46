"""Module for using the shoplink interface of the external shop service."""
from typing import Optional
from .external_shop import ExternalShop


class ShopLink(ExternalShop):
    """Class to send and get the shoplink to the external shop service."""

    def set_shoplink(self, shop: str, ean: str, publication_type: Optional[str], shoplink: str) -> None:
        """Set shop link of specified EAN and publication type of the shop."""
        if publication_type:
            urlpath = 'shoplink/{}/{}/{}'.format(shop, ean, publication_type)
        else:
            urlpath = 'shoplink/{}/{}'.format(shop, ean)
        self.put_request(urlpath=urlpath, data={'url': shoplink})

    def get_shoplink(self, shop: str, ean: str, publication_type: str) -> str:
        """Get the shoplink for the specified shop, EAN and publication type."""
        return self.get_request_field(urlpath='shoplink/{}/{}/{}'.format(shop, ean, publication_type),
                                      fieldname='url')
