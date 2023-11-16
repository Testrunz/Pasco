from pasco.code_node_device import CodeNodeDevice
import time

def main():
    code_node = CodeNodeDevice()
    code_node.connect_by_id('479-659')

    try:
        while True:
            button_value = code_node.read_data('Button1')
            temperature_value = code_node.read_data('Temperature')
            brightness_value = code_node.read_data('Brightness')
            
            print(f"Button1 Value: {button_value}")
            print(f"Temperature Value: {temperature_value}")
            print(f"Brightness Value: {brightness_value}")

            if button_value == 0:
                if brightness_value < 2:
                    code_node.set_rgb_led(100, 100, 100)
                else:
                    code_node.set_rgb_led(0, 0, 0)
                    
            time.sleep(0.25)
    except KeyboardInterrupt:
        pass  # Allow the user to exit the loop using Ctrl+C

    code_node.disconnect()

if __name__ == "__main__":
    main()
