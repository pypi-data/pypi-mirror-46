from unittest import TestCase

import responses

from qbo import Qbo


class TestQbo(TestCase):
    def setUp(self):
        self.qbo = Qbo("https://test.test/")

    @responses.activate
    def test_recipes(self):
        response_json = {
            "index_0": {
                "uid": "00000000-0000-0000-0000-000000000000",
                "userId": "00000000-0000-0000-0000-000000000aaa",
                "creatorId": "00000000-0000-0000-0000-000000000aaa",
                "userName": "Testman",
                "name": "Milkcoffee",
                "coffeeAmount": 160,
                "foamAmount": 0,
                "milkAmount": 120,
                "cupSize": 280,
                "creationTimestamp": 1555994946,
                "defaultRecipe": 0,
                "usesHotMilk": 1,
                "sequence": {
                    "index_0": 1,
                    "index_1": 3,
                    "index_2": 0,
                    "index_3": 0,
                    "index_4": 0
                },
                "favouriteCapsuleId": -1
            },
            "index_1": {
                "uid": "00000000-0000-0000-0000-000000000001",
                "userId": "00000000-0000-0000-0000-000000000aaa",
                "creatorId": "00000000-0000-0000-0000-000000000aaa",
                "userName": "Testman",
                "name": "Coffee",
                "coffeeAmount": 75,
                "foamAmount": 80,
                "milkAmount": 120,
                "cupSize": 280,
                "creationTimestamp": 1499801868,
                "defaultRecipe": 0,
                "usesHotMilk": 0,
                "sequence": {
                    "index_0": 3,
                    "index_1": 4,
                    "index_2": 5,
                    "index_3": 2,
                    "index_4": 0
                },
                "favouriteCapsuleId": -1
            },
            "index_2": {
                "uid": "00000000-0000-0000-0000-000000000002",
                "userId": "00000000-0000-0000-0000-000000000aaa",
                "creatorId": "00000000-0000-0000-0000-000000000aaa",
                "userName": "Testman",
                "name": "Cappuccino",
                "coffeeAmount": 70,
                "foamAmount": 50,
                "milkAmount": 70,
                "cupSize": 200,
                "creationTimestamp": 1555479179,
                "defaultRecipe": 0,
                "usesHotMilk": 1,
                "sequence": {
                    "index_0": 3,
                    "index_1": 4,
                    "index_2": 2,
                    "index_3": 0,
                    "index_4": 0
                },
                "favouriteCapsuleId": -1
            }
        }

        responses.add(responses.GET, 'https://test.test/recipes', json=response_json, status=200)

        recipes = self.qbo.recipes()

        assert recipes is not None
        assert len(recipes) == 3

        from qbo.qbo import Recipe
        from uuid import UUID

        first_recipe = recipes[0]

        assert isinstance(first_recipe, Recipe)
        assert first_recipe.name == "Milkcoffee"

        assert isinstance(first_recipe.uid, UUID)
        assert first_recipe.uid == UUID("00000000-0000-0000-0000-000000000000")

        assert first_recipe.uses_hot_milk is True

        second_recipe = recipes[1]
        assert isinstance(second_recipe, Recipe)
        assert second_recipe.name == "Coffee"

        assert isinstance(second_recipe.uid, UUID)
        assert second_recipe.uid == UUID("00000000-0000-0000-0000-000000000001")

        assert second_recipe.uses_hot_milk is False

        third_recipe = recipes[2]
        assert isinstance(third_recipe, Recipe)
        assert third_recipe.name == "Cappuccino"

        assert isinstance(third_recipe.uid, UUID)
        assert third_recipe.uid == UUID("00000000-0000-0000-0000-000000000002")

        assert third_recipe.uses_hot_milk is True

    @responses.activate
    def test_name(self):
        response_json = {
            "name": "TEST123"
        }

        responses.add(responses.GET, 'https://test.test/settings/name', json=response_json, status=200)

        name = self.qbo.name()

        assert name == "TEST123"

    @responses.activate
    def test_maintenance_status(self):
        response_json = {
            "maximumDescaleValue": 40000,
            "currentDescaleValue": 10000,
            "machineDescaleStatus": 0,
            "maximumCleanValue": 80,
            "currentCleanValue": 40,
            "machineCleanStatus": 1,
            "rinsingStatus": 3
        }

        responses.add(responses.GET, 'https://test.test/status/maintenance', json=response_json, status=200)

        maintenance_status = self.qbo.maintenance_status()

        assert maintenance_status.maximum_descale_value == 40000
        assert maintenance_status.current_descale_value == 10000
        assert maintenance_status.descale_percent == 0.25
        assert maintenance_status.machine_descale_status == 0

        assert maintenance_status.maximum_clean_value == 80
        assert maintenance_status.current_clean_value == 40
        assert maintenance_status.clean_percent == 0.5
        assert maintenance_status.machine_clean_status == 1
        assert maintenance_status.rinsing_status == 3

    @responses.activate
    def test_machine_info(self):
        response_json = {
            "serialNumber": "111111",
            "macAddress": "AA:BB:CC:DD:EE:FF",
            "version": "V01.20.A123"
        }

        responses.add(responses.GET, 'https://test.test/machineInfo', json=response_json, status=200)

        machine_info = self.qbo.machine_info()

        assert machine_info.serial_number == "111111"
        assert machine_info.mac_address == "AA:BB:CC:DD:EE:FF"
        assert machine_info.version == "V01.20.A123"
