import tflink
import os

from library.core import console
from library.core.helpmodule.randomtextcreator import GetRandomText

def ConvertFileIntoLink(input_file: str, remove: bool = False):
    try:
        if not os.path.isfile(input_file):
            return None
        
        file_extension = os.path.splitext(input_file)[1]
        client = tflink.TFLinkClient()
        link = tflink.TFLinkClient.upload(
            client,
            input_file,
            f"{GetRandomText(5)}{file_extension}"
        )

        if remove:
            os.remove(input_file)

        out_file = link.download_link
        
        return out_file

    except Exception as e:
        console.warn(f"Convert File To Link Was Error As: {e}")
        return None