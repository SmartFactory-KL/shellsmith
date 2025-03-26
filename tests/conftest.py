from dataclasses import dataclass

import pytest

from shellsmith import services
from shellsmith.config import config


def pytest_sessionstart(session):
    if services.health() != "UP":
        host = config.host
        reason = f"❌ BaSyx AAS Environment is not running at {host}"
        pytest.exit(reason, returncode=1)


@dataclass
class BaseModel:
    id_short: str
    id: str


@dataclass
class Shell(BaseModel):
    pass


@dataclass
class Submodel(BaseModel):
    pass


@dataclass
class Product(Shell):
    product_identification: Submodel
    production_plan: Submodel


@dataclass
class Resource(Shell):
    good_information: Submodel
    asset_location: Submodel


semitrailer_product = Product(
    id_short="Semitrailer",
    id="https://smartfactory.de/shells/3a4f1723-fc7d-4903-a621-d79ce9e4241c",
    product_identification=Submodel(
        id_short="ProductIdentification",
        id="https://smartfactory.de/submodels/c9afa701-4218-4628-b62c-40204a0f9f06",
    ),
    production_plan=Submodel(
        id_short="ProductionPlan",
        id="https://smartfactory.de/submodels/f1f73b85-73b8-429f-b706-df9cbbd503c0",
    ),
)

wst_a_1_resource = Resource(
    id_short="WorkpieceCarrier_A_1",
    id="https://smartfactory.de/shells/20e23e70-2248-4484-9b96-aa142d1cc12d",
    good_information=Submodel(
        id_short="GoodInformation",
        id="https://smartfactory.de/submodels/eaedbc25-c8b3-435f-bd52-3a336e9d5ef5",
    ),
    asset_location=Submodel(
        id_short="AssetLocation",
        id="https://smartfactory.de/submodels/34e987dd-f5fd-4639-b1cc-eed8ff09b6a9",
    ),
)


@pytest.fixture
def semitrailer() -> Product:
    return semitrailer_product


@pytest.fixture
def workpiece_carrier_a1() -> Resource:
    return wst_a_1_resource
