from .pin_resolver import PinResolver


class ManualPinResolver(PinResolver):
    def get_pin(self, email: str) -> int:
        while True:
            try:
                pin_str = input(f"Pin for {email}: ")
                return int(pin_str)
            except ValueError:
                print("Pin must be a 6-digit number")
