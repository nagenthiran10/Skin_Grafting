from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render,redirect
from admins.models import demo
from admins.models import main
from django.contrib import messages

# HOME

def dermato_home(request):
    return render(request,"dermatoplasty/dermato_homepage.html")



#dermatoplasty register and login



def dermato_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        main(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'Dermatoplasty Registration Successful, Kindly check your email: {email} for Login Credentials.')
        return redirect('/')
    return render(request,'dermatoplasty/reg_log.html')



def dermato_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            data = main.objects.get(email=email, password=password)
            if main:
                messages.info(request, "Dermatoplasty  Login Successful")
                return redirect("/dermato_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'dermatoplasty/reg_log.html')
        except:
            messages.info(request, "Wrong Credentials")
            return render(request, 'dermatoplasty/reg_log.html')
    return render(request, 'dermatoplasty/reg_log.html')





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
def dermato_req_result(request):
    data = demo.objects.all()
    blockchain = Blockchain()

    # Generate key and IV (should be stored securely and retrieved when needed)
    key, iv = generate_key_iv()

    for item in data:
        # Encrypt each field separately, handling None values
        e_mussel_glue_needed = encrypt_data(
            str(item.mussel_glue_needed) if item.mussel_glue_needed is not None else '0', key, iv)
        e_mussel_needed = encrypt_data(
            str(item.mussel_needed) if item.mussel_needed is not None else '0', key, iv)
        e_allantoin_needed= encrypt_data(
            str(item.allantoin_needed) if item.allantoin_needed is not None else '0', key, iv)
        e_egf_needed= encrypt_data(
            str(item.egf_needed) if item.egf_needed is not None else '0', key, iv)

        # Create a block of encrypted data
        block_data = {
            'encrypted_mussel_glue_needed': e_mussel_glue_needed,
            'encrypted_mussel_needed':e_mussel_needed,
            'encrypted_allantoin_needed':e_allantoin_needed,
            'encrypted_egf_needed':e_egf_needed,

        }

        # Add block to the blockchain
        blockchain.data = block_data
        block = blockchain.create_block(previous_hash=blockchain.get_last_block()['previous_hash'])

        # Update the existing record with encrypted data and blockchain information
        item.encrypted_mussel_glue_needed = e_mussel_glue_needed
        item.encrypted_mussel_needed = e_mussel_needed
        item.encrypted_allantoin_needed= e_allantoin_needed
        item.encrypted_egf_needed = e_egf_needed
        item.save()
    return render(request, 'dermatoplasty/bio_reports.html', {'data': data})



def getkey_dermato(request, project_id):
    data = demo.objects.get(project_id=project_id)
    key = get_random_bytes(32)  # AES-256 requires a 32-byte key

    # Encode the key for storage (base64 is a common choice)
    encoded_key = base64.b64encode(key).decode('utf-8')
    data.dermato_decryption_key = encoded_key
    data.save()

    send_mail(

        'Dermatoplasty: Decryption key',
        f'Hi Dermatoplasty,\nYour Decryption key for Decrypting "{data.project_id}" Record is "{data.dermato_decryption_key}".\n'
        'Please use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['kramesh.suryainfo@gmail.com'],
        fail_silently=False,
    )
    data.dermato_get_key = True
    data.save()
    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/bioreports/')





def decrypt_data_dermato(request, project_id):
    d = demo.objects.get(project_id=project_id)
    if request.method == "POST":
        decryption_key = request.POST['decryption_key']

        if d.dermato_decryption_key == decryption_key:
            d.dermato_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Key Verified Successfully')
            return redirect('/bioreports/')
        else:
            messages.info(request, f'{d.project_id}: Wrong Key, Kindly enter the correct key to continue.')
    return redirect('/bioreports/')

# bio-scan

def dermatoscan(request):
    data =demo.objects.filter(dermato_decrypt=True)
    context = {'data': data}
    return render(request,"dermatoplasty/dermato_scan.html",context)


# bio - calculation.....................


def dermato_calculation(request, project_id):
    # Retrieve the demo object using the project_id
    demo_object = demo.objects.get(project_id=project_id)

    grafting_operation_time_taken = " 2 "
    sterile_solution = " 250 "

    demo_object.grafting_operation_time_taken = grafting_operation_time_taken
    demo_object.sterile_solution = sterile_solution

    # Update the status
    demo_object.dermato_scanned = True
    demo_object.status = "Dermatoplasty  Done"
    demo_object.save()

    # Provide feedback and render the results
    messages.info(request, "Dermatoplasty Processed Successfully")
    data = demo.objects.all()
    return redirect("/dermatofile/")



# Bio file

def dermatofile(request):
    data=demo.objects.filter(dermato_scanned=True)
    return render(request,"dermatoplasty/dermato_file.html",{'data':data})


# logout

def dermato_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            del request.session['user_id']
            messages.info(request, 'Dermatoplasty Logout successful')
            return redirect('/')
        except demo.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('/')
    messages.info(request, 'Dermatoplasty Logout successful')
    return redirect('/')












