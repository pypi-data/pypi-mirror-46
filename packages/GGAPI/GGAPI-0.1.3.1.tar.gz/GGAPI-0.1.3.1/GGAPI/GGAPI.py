from GGAPI import Auth
from GGAPI.Services import UserMessageService, StoreService, ProductService, CargoService, SaleService


class GGAPI(object):

    def __init__(self, username, password, api_key, secret_key):
        self._auth = Auth.Auth(username, password, api_key, secret_key)
        self._cargoService = CargoService(self._auth)
        self._productService = ProductService(self._auth)
        self._saleService = SaleService(self._auth)
        self._storeService = StoreService(self._auth)
        self._userMessageService = UserMessageService(self._auth)

    def getCargoService(self) -> CargoService:
        return self._cargoService

    def getProductService(self) -> ProductService:
        return self._productService

    def getSaleService(self) -> SaleService:
        return self._saleService

    def getStoreService(self) -> StoreService:
        return self._storeService

    def getUserMessageService(self) -> UserMessageService:
        return self._userMessageService
