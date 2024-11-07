from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
import pandas as pd
from .forms import RegistrationForm
from .models import Registration  


def landing(request):
    return render(request, 'UserEntry/landing.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)


        if form.is_valid():
            registration = form.save()  

            try:
                send_mail(
                    subject='Registration Successful',
                    message=f"Hello {registration.name},\n\nYour data has been uploaded successfully.\n\nThank you for registering!",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[registration.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
                return render(request, 'UserEntry/register.html', {
                    'form': form,
                    'error_message': "There was an issue sending the confirmation email. Please try again later."
                })

            return redirect('thank_you')

        else:
            print(form.errors)
            return render(request, 'UserEntry/register.html', {
                'form': form,
                'error_message': "Please correct the errors below."
            })

    else:
        form = RegistrationForm()

    return render(request, 'UserEntry/register.html', {'form': form})




def thank_you(request):
    return render(request, 'UserEntry/thank_you.html', {
        'message': "Thank you for registering! A confirmation email has been sent to your inbox."
    })


# Export data to Excel
def export_to_excel(request):
    # Fetch data from your Django model
    data = Registration.objects.all().values()
    # Convert to DataFrame
    df = pd.DataFrame(list(data))

    # Create a response with the appropriate Excel headers
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'

    # Write DataFrame to an Excel file in the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    return response
