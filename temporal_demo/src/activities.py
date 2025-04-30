import asyncio
from temporalio import activity
from pdf2image import convert_from_path
import os

class Aadhar_Verification:
    @activity.defn
    async def unpackPdf(self, data):
        """Unpack the PDF file and extract the data."""
        # Simulate unpacking the PDF
        images = convert_from_path(data['file_location'])
        output_dir = os.path.join(os.getcwd(), "aadhar_images")
        os.makedirs(output_dir, exist_ok=True)
        
        for i in range(len(images)):
            images[i].save(os.path.join(output_dir, f'image_{i}.png'), 'PNG')
        print(f"Unpacked PDF and saved images to {output_dir}")
        return output_dir
    