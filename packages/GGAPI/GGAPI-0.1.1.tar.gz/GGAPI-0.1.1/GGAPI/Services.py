from GGAPI.Service import Service
import json


class CargoService(Service):

    def __init__(self, auth):
        super().__init__('individual', 'cargo', auth)

    def getCargoInformation(self, saleCode: str, lang: str = 'en') -> json:
        url = "{}&saleCode={}".format(self.requestURL('getCargoInformation', 'json', 'json', lang), saleCode)
        return self.session.get(url=url).json()

    def sendCargoInformation(self, saleCode: str, cargoCode: str, cargoCompany: str, cargoBranch: str, followUpUrl: str,
                             userType: str = 'S', lang: str = 'en') -> json:
        req = {
            "saleCode": saleCode,
            "cargoPostCode": cargoCode,
            "cargoCompany": cargoCompany,
            "cargoBranch": cargoBranch,
            "followUpUrl": followUpUrl,
            "userType": userType
        }

        url = self.requestURL('sendCargoInformation', 'json', 'json', lang)
        return self.session.post(url=url, json=req).json()


class ProductService(Service):

    def __init__(self, auth):
        super().__init__('individual', 'product', auth)

    def insertProduct(self, item_id: str, forceToSpecEntry: bool, nextDateOption: bool, request: dict,
                      lang: str = 'en') -> json:
        url = "{}&itemId={}&forceToSpecEntry={}&nextDateOption={}".format(
            self.requestURL('insertProduct', 'json', 'json', lang), item_id, forceToSpecEntry, nextDateOption)
        return self.session.post(url=url, json=request).json()

    def getProduct(self, lang: str, product_id: object) -> json:
        url = "{}&id=productId&value={}".format(self.requestURL('getProduct', 'json', 'json', lang), product_id)
        return self.session.get(url).json()

    def getProducts(self, startOffSet=0, rowCount=100, status='A', withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&status={}&withData={}".format(
            self.requestURL('getProducts', 'json', 'json', lang), startOffSet, rowCount, status, withData)
        return self.session.get(url=url).json()


class SaleService(Service):

    def __init__(self, auth):
        super().__init__('individual', 'activity', auth)

    def getSoldItems(self, startOffset=0, rowCount=100, withData=False, byStatus='S', lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}&byStatus={}".format(
            self.requestURL('getSoldItems', 'json', 'json', lang), startOffset, rowCount, withData, byStatus)
        return self.session.get(url=url).json()

    def getActiveSales(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getActiveSales', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()

    def getUnsoldItems(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getUnsoldItems', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()

    def getWonItems(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getWonItems', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()

    def getBidItems(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getBidItems', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()

    def getWatchItems(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getWatchItems', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()

    def getDidntWinItems(self, startOffset=0, rowCount=100, withData=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&withData={}".format(
            self.requestURL('getDidntWinItems', 'json', 'json', lang), startOffset, rowCount, withData)
        return self.session.get(url=url).json()


class StoreService(Service):

    def __init__(self, auth):
        super().__init__('individual', 'store', auth)

    def getStore(self, lang: str = 'en') -> json:
        url = self.requestURL('getStore', 'json', 'json', lang)
        return self.session.get(url=url).json()


class UserMessageService(Service):

    def __init__(self, auth):
        super().__init__('individual', 'message', auth)

    def getInboxMessages(self, startOffset=0, rowCount=100, unread=False, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}&unread={}".format(
            self.requestURL('getInboxMessages', 'json', 'json', lang), startOffset, rowCount, unread)
        return self.session.get(url=url).json()

    def sendNewMessage(self, to, title, content, sendCopy=False, lang: str = 'en'):
        req = {
            "to": to,
            "title": title,
            "messageContent": content,
            "sendCopy": sendCopy
        }
        url = self.requestURL('sendNewMessage', 'json', 'json', lang)
        return self.session.post(url=url, json=req).json()

    def getSendedMessages(self, startOffset=0, rowCount=100, lang: str = 'en') -> json:
        if rowCount > 100:
            rowCount = 100
        url = "{}&startOffSet={}&rowCount={}".format(self.requestURL('getSendedMessages', 'json', 'json', lang),
                                                     startOffset, rowCount)
        return self.session.get(url=url).json()
