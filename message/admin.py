from django.contrib import admin
from .models import Contact, RepliedContact
from django.core.mail import send_mail
from django.conf import settings


# Register your models here.

class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at', 'reply_status')
    list_editable = ('reply_status',)

    def save_model(self, request, obj, form, change):
        if obj.reply_status:
            reply_message = obj.reply_message
            # Create a new RepliedContact instance
            RepliedContact.objects.create(

                user=obj.user,  # Assuming you want to copy the user from Contact
                name=obj.name,
                email=obj.email,
                message=obj.message,
                reply_message=reply_message
            )

            # Send the reply email
            subject = 'Reply to Your Message'
            message = f"Hello {obj.name},\n\n{reply_message}"
            recipient_list = [obj.email]
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,  # From email address
                recipient_list,
                fail_silently=False,
            )

            # Optionally, delete the original Contact if desired
            obj.delete()
        else:
            super().save_model(request, obj, form, change)


admin.site.register(Contact, ContactAdmin)


class RepliedContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'reply_message', 'replied_at', )


admin.site.register(RepliedContact, RepliedContactAdmin)