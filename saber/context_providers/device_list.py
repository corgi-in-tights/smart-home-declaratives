from saber import SaberContextProvider
from saber.devices import get_device_manager


class DeviceListContextProvider(SaberContextProvider):
    """
    Context provider for device list management.
    This class is responsible for providing context related to device lists in the Saber logic layer.
    """

    def __init__(self):
        super().__init__("device_list")

    async def get_context(self, input_data: dict, intent_template: dict):
        """
        Get the context for device list management.
        This method should be overridden by subclasses to provide specific context.
        """
        devices = await get_device_manager().get_devices()
        device_list = [
            {
                "id": device["id"],
                "name": device["name"],
                "model": device.get("model", "Unknown"),
                "manufacturer": device.get("manufacturer", "Unknown"),
                "entities": await get_device_manager().get_device_entities(device["id"]),
            }
            for device in devices
        ]
        return {
            "device_list": device_list,
        }

    async def get_prompt(self, context: dict):
        return f"Here is the list of devices available in your system. {context['device_list']}"
