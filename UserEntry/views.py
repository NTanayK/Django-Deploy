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
                    subject='Your Registration for Data Science Workshop is Confirmed!',
                    message=None,  # We will use HTML content instead
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[registration.email],
                    fail_silently=False,
                    html_message=f"""
                            <html>
                                <body style="font-family: Arial, sans-serif; line-height: 1.6;">
                                    <div style="border: 1px solid #d9d9d9; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
                                        <h2 style="color: #333;">Hello {registration.name},</h2>
                                        <p>We are excited to inform you that your registration for the upcoming workshop <strong>Data Science with R</strong> has been successfully confirmed!</p>

                                        <h3 style="color: #555;">Your Slot:</h3>
                                        <p style="color: #4caf50; font-weight: bold;">Confirmed!</p>

                                        <h3 style="color: #555;">Workshop Details:</h3>
                                        <p><strong><em>Data Science With R by Dr. Md Hasnat Ali</em></strong></p>
                                        <p><strong>Location:</strong> Class Room-1, Level-1, KAR Campus</p>

                                        <h4 style="color: #333; margin-bottom: 5px;">Timings:</h4>
                                        <p>
                                            <strong><u>Module - I:</u></strong> Friday, 17 January 2025, 3:00 pm - 5:00 pm<br>
                                            <strong><u>Module - II:</u></strong> Friday, 24 January 2025, 3:00 pm - 5:00 pm
                                        </p>

                                        <h3 style="color: #555;">Workshop Overview:</h3>
                                        <p>This workshop is designed to provide participants with foundational skills in R programming, data manipulation, and statistical analysis,
                                        equipping them for various data science applications. </p>



                                        <h4 style="color: #333;">Important Notes:</h4>
                                        <ul>
                                            <li>Please arrive 10 minutes before the session starts to complete the check-in process.</li>
                                            <li>Bring a notebook and a laptop with R Studio pre-installed (if possible).</li>
                                            <li>Refreshments will be provided during the break.</li>
                                        </ul>

                                        <p>If you have any questions or require assistance, please don’t hesitate to contact us at <strong>7794814703</strong>. We’re here to help!</p>


                                        <p style="margin-top: 20px;">We look forward to seeing you at the workshop!</p>

                                        <p>Best Regards,<br>
                                        <strong>The Workshop Team</strong></p>
                                    </div>
                                </body>
                            </html>
                        """
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
