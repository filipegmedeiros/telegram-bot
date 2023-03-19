from dependency_injector import containers, providers

from repository.purchase_repository import PurchaseRepository
from service.bot_service import BotService
from service.purchase_service import PurchaseService


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(modules=['app'])

    purchase_repository = providers.Factory(PurchaseRepository)
    purchase_service = providers.Factory(PurchaseService, purchase_repository=purchase_repository)
    bot_service = providers.Factory(BotService, purchase_service=purchase_service)

