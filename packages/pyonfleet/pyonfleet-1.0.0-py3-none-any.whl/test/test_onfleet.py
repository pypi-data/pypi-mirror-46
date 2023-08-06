# import settings
# from pytest import fixture
# from .onfleet import Onfleet
# import base64
# import sys

# @fixture
# def api_info():
#     pass

# def test_onfleet_info():
#     """Tests an API call to Onfleet"""
#     encoded = base64.encodestring(b"e17b7186a973e8c90361ef63c7c31ae4")
#     onfleet_instance = Onfleet(encoded)
#     response = onfleet_instance.info()
#     assert onfleet_instance.api_key == encoded
#     assert response == 1922, "The response"

from onfleet import Onfleet

api = Onfleet()
driver = {
  "name": "A Swartz Test",
  "phone": "617-342-8853",
  "teams": ["W*8bF5jY11Rk05E0bXBHiGg2"],
  "vehicle": {
    "type": "CAR",
    "description": "Tesla Model S",
    "licensePlate": "FKNS9A",
    "color": "purple",
  }
}
api.workers.create(body=driver)