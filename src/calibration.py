class PixelCalibration:
    """
    Convert image coordinates between pixels and physical distance.
    """

    def __init__(self, mm_per_pixel):
        if mm_per_pixel <= 0:
            raise ValueError("mm_per_pixel must be positive")

        self.mm_per_pixel = mm_per_pixel

    def pixels_to_mm(self, pixels):
        return pixels * self.mm_per_pixel

    def mm_to_pixels(self, mm):
        return mm / self.mm_per_pixel

    def __repr__(self):
        return (
            f"PixelCalibration("
            f"mm_per_pixel={self.mm_per_pixel}"
            f")"
        )