

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from admins.models import demo
from admins.models import main
from django.contrib import messages



# HOME

def exfo_home(request):
    return render(request,"exfoliation/exfo_homepage.html")

# exfoliation register and login:


def exfo_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        main(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'Exfoliation Registration Successful, Kindly check your email: {email} for Login Credentials.')
        return redirect('/')
    return render(request,'exfoliation/reg_log.html')



def exfo_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            # Try to retrieve the user with the given email and password
            user = main.objects.get(email=email, password=password)

            if user:
                # Set the login field to True (1) upon successful login
                user.login = True
                user.save()

                # Set the user ID in the session to track the logged-in user
                request.session['user_id'] = user.id

                messages.info(request, "Exfoliation Login Successful")
                return redirect("/exfo_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'exfoliation/reg_log.html')
        except main.DoesNotExist:
            # Handle case where the user with the provided credentials does not exist
            messages.info(request, "Wrong Credentials")
            return render(request, 'exfoliation/reg_log.html')

    return render(request, 'exfoliation/reg_log.html')



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
def exfo_req_result(request):
    data = demo.objects.all()
    blockchain = Blockchain()

    # Generate key and IV (should be stored securely and retrieved when needed)
    key, iv = generate_key_iv()

    for item in data:
        # Encrypt each field separately, handling None values
        e_name_of_the_patient = encrypt_data(
            str(item.name_of_the_patient) if item.name_of_the_patient is not None else '0', key, iv)
        e_age = encrypt_data(
            str(item.age) if item.age is not None else '0', key, iv)
        e_gender = encrypt_data(
            str(item.gender) if item.gender is not None else '0', key, iv)
        e_type_of_wound = encrypt_data(
            str(item.type_of_wound) if item.type_of_wound is not None else '0', key, iv)
        e_wound_placement = encrypt_data(
            str(item.wound_placement) if item.wound_placement is not None else '0', key, iv)
        e_depth_of_wound = encrypt_data(
            str(item.depth_of_wound) if item.depth_of_wound is not None else '0', key, iv)
        e_circumference_of_the_wound = encrypt_data(
            str(item.circumference_of_the_wound) if item.circumference_of_the_wound is not None else '0', key, iv)

        # Create a block of encrypted data
        block_data = {
            'encrypted_name_of_the_patient': e_name_of_the_patient,
            'encrypted_age':e_age,
            'encrypted_gender':e_gender,
            'encrypted_type_of_wound':e_type_of_wound,
            'encrypted_wound_placement':e_wound_placement,
            'encrypted_depth_of_wound':e_depth_of_wound,
            'encrypted_circumference_of_the_wound':e_circumference_of_the_wound

        }

        # Add block to the blockchain
        blockchain.data = block_data
        block = blockchain.create_block(previous_hash=blockchain.get_last_block()['previous_hash'])

        # Update the existing record with encrypted data and blockchain information
        item.encrypted_name_of_the_patient = e_name_of_the_patient
        item.encrypted_age = e_age
        item.encrypted_gender = e_gender
        item.encrypted_type_of_wound = e_type_of_wound
        item.encrypted_wound_placement = e_wound_placement
        item.encrypted_depth_of_wound = e_depth_of_wound
        item.encrypted_circumference_of_the_wound = e_circumference_of_the_wound
        item.save()
    return render(request, 'exfoliation/exfo_req.html', {'data': data})


def getkey_exfo(request, project_id):
    data = demo.objects.get(project_id=project_id)
    key = get_random_bytes(32)  # AES-256 requires a 32-byte key

    # Encode the key for storage (base64 is a common choice)
    encoded_key = base64.b64encode(key).decode('utf-8')
    data.exfo_decryption_key = encoded_key
    data.save()

    send_mail(
        'Exfoliation: Decryption key',
        f'Hi Exfoliation,\nYour Decryption key for Decrypting "{data.project_id}" Record is "{data.exfo_decryption_key}".\n'
        'Please use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['kramesh.suryainfo@gmail.com'],
        fail_silently=False,
    )
    data.exfo_get_key = True
    data.save()
    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/exfo_requirements/')





def decrypt_data_exfo(request, project_id):
    d = demo.objects.get(project_id=project_id)
    if request.method == "POST":
        decryption_key = request.POST['decryption_key']


        if d.exfo_decryption_key == decryption_key:
            d.exfo_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Key Verified Successfully')
            return redirect('/exfo_requirements/')
        else:
            messages.info(request, f'{d.project_id}: Wrong Key, Kindly enter the correct key to continue.')
    return redirect('/exfo_requirements/')



# Exfo_scanning

def exfo_scan(request):
    data = demo.objects.filter(exfo_decrypt=True)
    context = {'data': data}
    return render(request,"exfoliation/exfo_scan.html",context)


def exfo_calculation(request,project_id):
        demo_object = demo.objects.get(project_id=project_id)

        wound_placement = demo_object.wound_placement
        circumference_of_the_wound = demo_object.circumference_of_the_wound

        if circumference_of_the_wound:
            circumference_of_the_wound = float(circumference_of_the_wound)
        else:
            # Handle the case where the value is None or empty
            circumference_of_the_wound = 0.0

        demo_object.circumference_of_skin_needed = circumference_of_the_wound * 1.0607
        demo_object.type_of_material = "Electric Dermatome"
        demo_object.holes_made_ratio = "2:1"

        # Determine place of skin peeling
        if wound_placement == 'thighs':
            demo_object.place_of_skin_peeling = 'buttocks'
        elif wound_placement == 'buttocks':
            demo_object.place_of_skin_peeling = 'thighs'
        else:
            demo_object.place_of_skin_peeling = 'thighs'

        demo_object.exfo_scanned = True
        demo_object.status = "Exfoliation Done"
        demo_object.save()

        messages.info(request, "Exfoliation Processed Successfully")
        data = demo.objects.all()
        # return render(request, 'exfoliation/exfo_file.html', {'data': data})
        return redirect("/exfo_file/")


# Exfo file

def exfo_file(request):
    data=demo.objects.filter(exfo_scanned=True)
    return render(request,"exfoliation/exfo_file.html",{'data':data})


# Logout

def exfo_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            del request.session['user_id']
            messages.info(request, 'Exfoliation Logout successful')
            return redirect('/')
        except demo.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('/')
    messages.info(request, 'Exfoliation Logout successful')
    return redirect('/')