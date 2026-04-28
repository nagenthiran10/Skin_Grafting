
from django.shortcuts import render, redirect

from .models import demo, main
from django.core.mail import send_mail

def home(request):
    return render(request, 'home_page/homepage.html')

# admin login & logout

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "admin@gmail.com" and password == "admin":
            messages.success(request,"Admin login successful")
            return redirect("/adminhome/")
        else:
            messages.error(request,"wrong credentials")
            return render(request, 'ad_min/admin_login.html')

    else:
        return render(request, 'ad_min/admin_login.html')


def logout(request):
    print("hello")
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            del request.session['user_id']
            messages.info(request, 'Admin Logout successful')
            return redirect('/')
        except demo.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('/')
    messages.info(request, 'Admin Logout successful')
    return redirect('/')

# admin home...............

def adminhome(request):
    return render(request, 'ad_min/admin_home.html')

# approve & reject..........

def exfoapprove(request):
    data = main.objects.filter(department='EXFOLIATION')
    return render(request, 'ad_min/exfo_approve.html',{'data': data})

def bioapprove(request):
    data = main.objects.filter(department='BIOADHESION')
    return render(request, 'ad_min/bio_approve.html',{'data': data})

def dermatoapprove(request):
    data = main.objects.filter(department='DERMATOPLASTY')
    return render(request, 'ad_min/dermato_approve.html',{'data': data})

def monitorapprove(request):
    data = main.objects.filter(department='MONITORING')
    return render(request, 'ad_min/monitor_approve.html',{'data': data})

def evalapprove(request):
    data = main.objects.filter(department='EVALUATION')
    return render(request, 'ad_min/eval_approve.html',{'data': data})


# requirements

def requirements(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        type_of_wound = request.POST.get('type_of_wound')
        wound_placement = request.POST.get('wound_placement')
        depth_of_wound = request.POST.get('depth_of_wound')
        circumference_of_the_wound = request.POST.get('circumference_of_the_wound')

        p=random.randint(1000,9999)
        project_id=f"Project:{p}"

        demo(name_of_the_patient=name, age=age,

             gender=gender,type_of_wound=type_of_wound,
             wound_placement=wound_placement,depth_of_wound=depth_of_wound,project_id=project_id,circumference_of_the_wound=circumference_of_the_wound).save()
        messages.success(request, 'Requirements saved successfully.')
        return redirect('/adminhome/')  # Redirect to chief home after successful submission
    return render(request, 'ad_min/requirements.html')


# EXFOLIATION approve & reject..........

import random
def approve(request,id):
    data=main.objects.get(id=id)
    password=random.randint(1000,9999)
    print(password)
    data.password=password
    data.rh_id=f"SG:{password}"
    data.save()

    send_mail(
        '{0}:Username and Password'.format(data.department),
        'Hello {0},\n Your {1} profile has been Approved.\n Your Username is "{2}" and Password is "{3}".\n Make sure you use this Username and Password while your logging in to the portal of Exfoliation.\n Thank You '.format(
            data.name,data.department, data.email,data.password),
        'anvi.aadiv@gmail.com',
        [data.email],
        fail_silently=False,
    )

    data.approve=True
    data.reject=False
    data.save()
    messages.info(request,f"{data.rh_id} : {data.department} Approval Successful")
    return redirect("/adminhome/")



def reject(request,id):
    data = main.objects.get(id=id)
    data.approve=False
    data.reject=True
    data.save()

    subject = 'Client Rejection'
    plain_message = f"Hi {data.name},\nYour registration was rejected due to some reasons.try this later!"
    send_mail(subject, plain_message, 'kramesh.suryainfo@gmail.com', [data.email], fail_silently=False)

    # data.delete()
    messages.info(request, "Rejection Mail Sent to Client")
    return redirect("/adminhome/")


# manage reports..........

def exfomanage(request):
    data = demo.objects.all()
    return render(request, 'ad_min/exfo_manage.html',{'data': data})

def biomanage(request):
    data = demo.objects.all()
    return render(request, 'ad_min/bio_manage.html',{'data': data})

def dermatomanage(request):
    data = demo.objects.all()
    return render(request, 'ad_min/dermato_manage.html',{'data': data})

def monitormanage(request):
    data = demo.objects.all()
    return render(request, 'ad_min/monitor_manage.html',{'data': data})

def evalmanage(request):
    data = demo.objects.all()
    return render(request, 'ad_min/eval_manage.html',{'data': data})

# MANAGE STATUS

def managestatus(request):
    data = demo.objects.all()
    return render(request, "ad_min/manage_status.html", {'data': data})

# FINAL REPORT

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.contrib import messages
import matplotlib.pyplot as plt
import tempfile



import matplotlib.pyplot as plt
import tempfile

def create_chart_image(data_dict, title):
    # Define the physical size of the figure
    fig_width, fig_height = 8, 6  # in inches

    # Create a figure and axis for the plot
    fig, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Extract labels and values from the data dictionary
    labels = list(data_dict.keys())
    values = list(data_dict.values())

    # Set the number of bars
    num_bars = len(labels)

    # Set bar width (fraction of figure width)
    bar_width = 0.4  # Width of bars, adjust if needed

    # Adjust x-tick positions to reduce space between bars
    x_ticks = [i * (1 - bar_width) for i in range(num_bars)]

    # Create a bar plot with reduced space between bars
    bars = ax.bar(x_ticks, values, width=bar_width, color=['blue', 'orange'] * (num_bars // 2 + 1))

    # Set title and labels
    ax.set_title(title)
    ax.set_ylabel('Percentage')

    # Set x-tick labels
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(labels)

    # Add percentage values on top of the bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%',
            ha='center', va='bottom'
        )

    # Adjust layout to fit bars
    plt.tight_layout()

    # Save the plot to a temporary file
    temp_img = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
    fig.savefig(temp_img.name, bbox_inches='tight')
    plt.close(fig)

    return temp_img.name






def final_report(request, project_id):
    data = demo.objects.get(project_id=project_id)
    title = "DERMTECH NEXUS THE NEW FRONTIER IN SKIN GRAFTING REPORT"

    # Create a BytesIO buffer to store PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    def draw_title_and_project_id(c):
        c.setFont("Helvetica-Bold", 16)
        text_width = c.stringWidth(title)
        c.setFillColor(colors.blue)
        x_position = (c._pagesize[0] - text_width) / 2
        c.drawString(x_position, 800, title)

        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        project_id_label = "Project ID:"
        text_width = c.stringWidth(project_id_label)
        x_position = (c._pagesize[0] - text_width - 100) / 2
        c.drawString(x_position, 780, project_id_label)

        c.setFillColor(colors.black)
        c.drawString(x_position + text_width + 5, 780, f"{data.project_id}")

    def draw_section(c, title, section_data, start_y):
        c.setFont("Helvetica-Bold", 14)
        c.setFillColor(colors.blue)
        c.drawString(50, start_y, title)
        start_y -= 20

        table_data = [[f"{item[0]}", f"{item[1]}"] for item in section_data]
        table = Table(table_data, colWidths=[200, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        table.wrapOn(c, 400, 400)
        table.drawOn(c, 50, start_y - len(section_data) * 20)

        return start_y - len(section_data) * 20 - 60

    draw_title_and_project_id(c)

    sections = [
        ("EXFOLIATION", [
            ["Circumference Of Skin Needed", f"{data.circumference_of_skin_needed}"],
            ["Type of Material Used For Skin Peeling", f"{data.type_of_material}"],
            ["Place of Skin Peeled", f"{data.place_of_skin_peeling}"],
            ["Holes Made on Skin", f"{data.holes_made_ratio}"],
        ]),
        ("BIOADHESION", [
            ["Mussel Needed (g)", f"{data.mussel_glue_needed}"],
            ["Mussel Glue (mg)", f"{data.mussel_needed}"],
            ["Allantoin (mg)", f"{data.allantoin_needed}"],
            ["Egf (µg)", f"{data.egf_needed}"],
        ]),
        ("DERMATOPLASTY", [
            ["Grafting Time Taken (hours)", f"{data.grafting_operation_time_taken}"],
            ["Sterile Saline (ml)", f"{data.sterile_solution}"],
        ]),
        ("MONITORING", [
            ["Time Taken For Curing (months)", f"{data.time_taken_for_curing}"],
            ["Types of Food To Follow", f"{data.types_of_food_to_follow}"],
            ["Patient Progress", f"{data.patient_progress}"],
        ]),
        ("EVALUATION (FINAL REPORT)", [
            ["Existing Side Effects (%)", f"{data.predicted_existing_side_effects}"],
            ["Existing Percentage of Scar (%)", f"{data.predicted_existing_scar}"],
            ["Proposed Side Effects (%)", f"{data.predicted_proposed_side_effects}"],
            ["Proposed Percentage of Scar (%)", f"{data.predicted_proposed_scar}"],
        ])
    ]

    y_position = 750
    for section_title, section_data in sections:
        y_position = draw_section(c, section_title, section_data, y_position)

    if y_position < 150:
        c.showPage()
        y_position = 750

    def draw_image(c, img_path, start_y):
        c.drawImage(img_path, 50, start_y - 300, width=400, height=250)
        return start_y - 350

    existing_scar_data = {
        "Existing Scar (%)": float(data.predicted_existing_scar),
        "Proposed Scar (%)": float(data.predicted_proposed_scar)
    }
    proposed_side_effects_data = {
        "Existing Side Effects (%)": float(data.predicted_existing_side_effects),
        "Proposed Side Effects (%)": float(data.predicted_proposed_side_effects)
    }

    existing_scar_img = create_chart_image(existing_scar_data, "Scar Percentages")
    proposed_side_effects_img = create_chart_image(proposed_side_effects_data, "Side Effects Percentages")

    y_position = draw_image(c, existing_scar_img, y_position)
    draw_image(c, proposed_side_effects_img, y_position)

    c.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}_{data.project_id}.pdf"'
    response.write(pdf_data)

    data.f_report.save(f"{title}_{data.project_id}.pdf", ContentFile(pdf_data))
    data.rep = False
    data.report = True
    data.save()

    messages.success(request, f"{data.project_id}, Report Generated successfully")
    return redirect('/managestatus/')











