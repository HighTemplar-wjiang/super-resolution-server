import os
import cv2

from server_path import *


class SuperResolution:

    def __init__(self, model_name, scale_factor):
        """Init and load model."""
        self.sr_model = cv2.dnn_superres.DnnSuperResImpl_create()
        self.sr_model.readModel(os.path.join(model_path, f"{model_name.upper()}_x{scale_factor}.pb"))
        self.sr_model.setModel(model_name.lower(), scale_factor)

    async def super_sample(self, filename):
        """Load and super-sample the image."""

        # Read file.
        filename_full_path = os.path.join(cache_path, filename)
        img_raw = cv2.imread(filename_full_path)

        # Super scaling.
        print(f"[INFO] Upscaling {filename}, resolution: {img_raw.shape}")
        if (img_raw.shape[0] > 500) or (img_raw.shape[1] > 500):
            print(f"[ERROR] Cannot process image with high resolution.")
            return None

        img_sr = self.sr_model.upsample(img_raw)
        print(f"[INFO] Upscaled {filename}, resolution: {img_sr.shape}")

        # Export to file.
        filename_root, filename_ext = os.path.splitext(filename)
        export_filename = filename_root + "_sr" + filename_ext
        export_filename_full_path = os.path.join(cache_path, export_filename)
        cv2.imwrite(export_filename_full_path, img_sr)

        return export_filename
