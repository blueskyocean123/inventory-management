# from django.db.models.signals import pre_save
# from .models import QRCode
# from django.utils.crypto import get_random_string
# from django.conf import settings as appsettings
# from .models import Product
# import qrcode

# ##Receiver function

# def QRcode_receiver(sender, instance, *args, **kwargs):
#     product = Product.objects.all()
#     qr_text = product.get_unique_number

#     # if not instance.string: # We need to check if we want to create
#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,)
#     # instance.string = qr_text
#     qr.add_data(qr_text)
#     img = qr.make_image()
#     codepwd = appsettings.MEDIA_ROOT+"qr/"+instance.string+".png"
#     img.save(codepwd)
#     instance.qr_code = "qr/"+instance.string+".png"

# pre_save.connect(QRcode_receiver, sender=QRcode)