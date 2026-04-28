import math

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,redirect
from admins.models import demo
from admins.models import main
from django.contrib import messages

# HOME

def bio_home(request):
    return render(request,"bioadhesion/bio_homepage.html")

#bioadhesion register and login

def bio_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        main(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'Bioadhesion Registration Successful, Kindly check your email: {email} for Login Credentials.')
        return redirect('/')
    return render(request,'bioadhesion/reg_log.html')

def bio_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            data = main.objects.get(email=email, password=password)
            if main:
                messages.info(request, "Bioadesion  Login Successful")
                return redirect("/bio_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'bioadhesion/reg_log.html')
        except:
            messages.info(request, "Wrong Credentials")
            return render(request, 'bioadhesion/reg_log.html')
    return render(request, 'bioadhesion/reg_log.html')


# exfo-reports


import json
from Crypto.Cipher import AES
import datetime
import hashlib
from Crypto.Random import get_random_bytes
from django.shortcuts import render
import base64


# Algorithm: AES Encryption, SHA-256 Hashing

# Blockchain class definition
class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_block(previous_hash='1')  # Genesis block

    def create_block(self, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }
        self.chain.append(block)
        return block

    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def get_last_block(self):
        return self.chain[-1]


# Key and initialization vector (IV) generation
def generate_key_iv():
    key = get_random_bytes(32)  # AES-256
    iv = get_random_bytes(16)  # AES block size
    return key, iv


# Encrypt data
def encrypt_data(plain_text, key, iv):
    cipher = AES.new(key, AES.MODE_CFB, iv)
    encrypted_data = cipher.encrypt(plain_text.encode('utf-8'))
    return base64.b64encode(iv + encrypted_data).decode('utf-8')


# Encrypt data using blockchain principles
def bio_req_result(request):
    data = demo.objects.all()
    blockchain = Blockchain()

    # Generate key and IV (should be stored securely and retrieved when needed)
    key, iv = generate_key_iv()

    for item in data:
        # Encrypt each field separately, handling None values
        e_circumference_of_skin_needed = encrypt_data(
            str(item.circumference_of_skin_needed) if item.circumference_of_skin_needed is not None else '0', key, iv)
        e_type_of_material = encrypt_data(
            str(item.type_of_material) if item.type_of_material is not None else '0', key, iv)
        e_place_of_skin_peeling = encrypt_data(
            str(item.place_of_skin_peeling) if item.place_of_skin_peeling is not None else '0', key, iv)
        e_holes_made_ratio= encrypt_data(
            str(item.holes_made_ratio) if item.holes_made_ratio is not None else '0', key, iv)

        # Create a block of encrypted data
        block_data = {
            'encrypted_circumference_of_skin_needed': e_circumference_of_skin_needed,
            'encrypted_type_of_material':e_type_of_material,
            'encrypted_place_of_skin_peeling':e_place_of_skin_peeling,
            'encrypted_holes_made_ratio':e_holes_made_ratio,

        }

        # Add block to the blockchain
        blockchain.data = block_data
        block = blockchain.create_block(previous_hash=blockchain.get_last_block()['previous_hash'])

        # Update the existing record with encrypted data and blockchain information
        item.encrypted_circumference_of_skin_needed = e_circumference_of_skin_needed
        item.encrypted_type_of_material = e_type_of_material
        item.encrypted_place_of_skin_peeling= e_place_of_skin_peeling
        item.encrypted_holes_made_ratio = e_holes_made_ratio
        item.save()
    return render(request, 'bioadhesion/exfo_reports.html', {'data': data})



def getkey_bio(request, project_id):
    data = demo.objects.get(project_id=project_id)
    key = get_random_bytes(32)  # AES-256 requires a 32-byte key

    # Encode the key for storage (base64 is a common choice)
    encoded_key = base64.b64encode(key).decode('utf-8')
    data.bio_decryption_key = encoded_key
    data.save()

    send_mail(
        'Bioadhesion: Decryption key',
        f'Hi Bioadhesion,\nYour Decryption key for Decrypting "{data.project_id}" Record is "{data.bio_decryption_key}".\n'
        'Please use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['kramesh.suryainfo@gmail.com'],
        fail_silently=False,
    )
    data.bio_get_key = True
    data.save()
    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/exforeports/')





def decrypt_data_bio(request, project_id):
    d = demo.objects.get(project_id=project_id)
    if request.method == "POST":
        decryption_key = request.POST['decryption_key']


        if d.bio_decryption_key == decryption_key:
            d.bio_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Key Verified Successfully')
            return redirect('/exforeports/')
        else:
            messages.info(request, f'{d.project_id}: Wrong Key, Kindly enter the correct key to continue.')
    return redirect('/exforeports/')



# bio-scan

def bio_scan(request):
    data =demo.objects.filter(bio_decrypt=True)
    context = {'data': data}
    return render(request,"bioadhesion/bio_scan.html",context)


# bio - calculation.....................


def bio_calculation(request, project_id):
    # Retrieve the demo object using the project_id
    demo_object = demo.objects.get(project_id=project_id)

    # Extract and convert data from the demo object
    depth_of_wound_cm = float(demo_object.depth_of_wound)
    circumference_of_wound = float(demo_object.circumference_of_the_wound)

    # Calculate the area of the wound
    wound_area = circumference_of_wound * depth_of_wound_cm

    # Constant k for mussel glue calculation (from example)
    k = 160  # This constant is derived from the provided example

    # Calculate mussel glue needed
    mussel_glue_needed = k * wound_area

    # Calculate mussel needed (1 gram mussel = 1 mg glue)
    mussel_needed = mussel_glue_needed

    # Calculate allantoin needed (1% of mussel glue needed)
    allantoin_needed = mussel_glue_needed * 0.01

    # Calculate EGF needed (0.01% of mussel glue needed)
    egf_needed = mussel_glue_needed * 0.0001

    # Ensure EGF is not too small (optional)
    egf_needed = mussel_glue_needed * 0.0001  # Set a minimum threshold

    # Save calculated values back to the demo object
    demo_object.mussel_glue_needed = mussel_glue_needed
    demo_object.mussel_needed = mussel_needed
    demo_object.allantoin_needed = allantoin_needed
    demo_object.egf_needed = egf_needed

    # Update the status
    demo_object.bio_scanned = True
    demo_object.status = "Bioadhesion Done"
    demo_object.save()

    # Provide feedback and render the results
    messages.info(request, "Bioadhesion Processed Successfully")
    data = demo.objects.all()
    return redirect("/bio_file/")


# Bio file

def bio_file(request):
    data=demo.objects.filter(bio_scanned=True)
    return render(request,"bioadhesion/bio_file.html",{'data':data})


# Logout

def bio_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            del request.session['user_id']
            messages.info(request, 'Bioadhesion Logout successful')
            return redirect('/')
        except demo.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('/')
    messages.info(request, 'Bioadhesion Logout successful')
    return redirect('/')
