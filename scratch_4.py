import usb.core
import usb.util
import time

def thermal_print():
    """These values are the vendor and product id converted to integers"""
    vendor_id = 0x04b8
    product_id = 0x0202

    # Find the device
    printer = usb.core.find(idVendor=vendor_id, idProduct=product_id)
    if printer is None:
        raise ValueError("Printer not found")

    # Set the active configuration. With no arguments, the first configuration will be the active one
    printer.set_configuration()

    # Get an endpoint instance
    cfg = printer.get_active_configuration()
    intf = cfg[(0, 0)]

    ep_out = usb.util.find_descriptor(
        intf,
        # Match the first OUT endpoint
        custom_match=lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
    )

    if ep_out is None:
        raise ValueError("Endpoint not found")

    # Prepare the text to print
    current_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", current_time)
    text = formatted_time + "\n"

    # Print the text
    ep_out.write(text.encode('utf-8'))

    # Add linefeed
    ep_out.write(b'\n')

thermal_print()
