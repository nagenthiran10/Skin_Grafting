from django.core.mail import send_mail

from admins.models import demo
from admins.models import main



#Home
def eval_home(request):
    return render(request,"evaluation/eval_homepage.html")


#Evaluation register and login
def eval_register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        main(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'Evaluation Registration Successful, Kindly check your email: {email} for Login Credentials.')
        return redirect('/')
    return render(request,'evaluation/reg_log.html')


def eval_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            data = main.objects.get(email=email, password=password)
            if main:
                messages.info(request, "Evaluation Login Successful")
                return redirect("/eval_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'evaluation/reg_log.html')
        except:
            messages.info(request, "Wrong Credentials")
            return render(request, 'evaluation/reg_log.html')
    return render(request, 'evaluation/reg_log.html')


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
def eval_req_result(request):
    data = demo.objects.all()
    blockchain = Blockchain()

    # Generate key and IV (should be stored securely and retrieved when needed)
    key, iv = generate_key_iv()

    for item in data:
        # Encrypt each field separately, handling None values
        e_time_taken_for_curing  = encrypt_data(
            str(item.time_taken_for_curing ) if item.time_taken_for_curing  is not None else '0', key, iv)
        e_types_of_food_to_follow = encrypt_data(
            str(item.types_of_food_to_follow) if item.types_of_food_to_follow is not None else '0', key, iv)
        e_patient_progress = encrypt_data(
            str(item.patient_progress) if item.patient_progress is not None else '0', key, iv)

        # Create a block of encrypted data
        block_data = {

            'encrypted_taken_for_curing': e_time_taken_for_curing ,
            'encrypted_types_of_food_to_follow':e_types_of_food_to_follow,
            'encrypted_patient_progress': e_patient_progress,

        }

        # Add block to the blockchain
        blockchain.data = block_data
        block = blockchain.create_block(previous_hash=blockchain.get_last_block()['previous_hash'])

        # Update the existing record with encrypted data and blockchain information
        item.encrypted_time_taken_for_curing = e_time_taken_for_curing
        item.encrypted_types_of_food_to_follow = e_types_of_food_to_follow
        item.encrypted_patient_progress = e_patient_progress
        item.save()
    return render(request, 'evaluation/monitor_reports.html', {'data': data})



def getkey_eval(request, project_id):
    data = demo.objects.get(project_id=project_id)
    key = get_random_bytes(32)  # AES-256 requires a 32-byte key

    # Encode the key for storage (base64 is a common choice)
    encoded_key = base64.b64encode(key).decode('utf-8')
    data.eval_decryption_key = encoded_key
    data.save()

    send_mail(

        'Evaluation: Decryption key',
        f'Hi Evaluation,\nYour Decryption key for Decrypting "{data.project_id}" Record is "{data.eval_decryption_key}".\n'
        'Please use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['kramesh.suryainfo@gmail.com'],
        fail_silently=False,
    )
    data.eval_get_key = True
    data.save()
    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/monitorreports/')



def decrypt_data_eval(request, project_id):
    d = demo.objects.get(project_id=project_id)
    if request.method == "POST":
        decryption_key = request.POST['decryption_key']

        if d.eval_decryption_key == decryption_key:
            d.eval_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Key Verified Successfully')
            return redirect('/monitorreports/')
        else:
            messages.info(request, f'{d.project_id}: Wrong Key, Kindly enter the correct key to continue.')
    return redirect('/monitorreports/')


def eval_scan(request):
    data = demo.objects.filter(eval_decrypt=True)
    context = {'data': data}
    return render(request,"evaluation/eval_scan.html",context)


def calculate_existing(request, project_id):
    # Retrieve the demo object using the project_id
    demo_object = demo.objects.get(project_id=project_id)

    # Fetch values from the database
    circumference_of_skin_needed = float(demo_object.circumference_of_skin_needed)
    mussel_glue_needed = float(demo_object.mussel_glue_needed)
    grafting_operation_time_taken = float(demo_object.grafting_operation_time_taken)
    time_taken_for_curing = float(demo_object.time_taken_for_curing)

    # Load existing dataset
    existing_dataset = pd.read_csv("E:/company_project/PROJECT/Skin grafting/existing skin grafting.csv")

    # Prepare data for Gradient Boosting Regressor
    X_existing = existing_dataset[['Circumference of Skin (cm)', 'Glue Needed (mg)', 'Grafting Time (hrs)', 'Time for Curing (months)']]
    y_existing_side_effects = existing_dataset['Side Effects (%)']
    y_existing_scar = existing_dataset['Scar (%)']

    # Append the database values as a new row to X_existing
    new_row = pd.DataFrame({
        'Circumference of Skin (cm)': [circumference_of_skin_needed],
        'Glue Needed (mg)': [mussel_glue_needed],
        'Grafting Time (hrs)': [grafting_operation_time_taken],
        'Time for Curing (months)': [time_taken_for_curing]
    })

    # Concatenate the new row with the existing dataset
    X_existing_with_db = pd.concat([X_existing, new_row], ignore_index=True)

    # Initialize the Gradient Boosting Regressor models
    model_side_effects = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model_scar = GradientBoostingRegressor(n_estimators=100, random_state=42)

    # Fit the models with the updated dataset (including the new row from the database)
    model_side_effects.fit(X_existing, y_existing_side_effects)
    model_scar.fit(X_existing, y_existing_scar)

    # Predict side effects and scar percentages for the entire dataset, including the new row
    predicted_existing_side_effects = model_side_effects.predict(X_existing_with_db)
    predicted_existing_scar = model_scar.predict(X_existing_with_db)

    # Extract the predictions for the new row (which corresponds to the last row in the dataset)
    new_predicted_side_effects = predicted_existing_side_effects[-1]
    new_predicted_scar = predicted_existing_scar[-1]

    # Update demo object with the predictions for the new row
    demo_object.predicted_existing_side_effects = round(new_predicted_side_effects)
    demo_object.predicted_existing_scar = round(new_predicted_scar)
    demo_object.eval_existing_scanned = True
    demo_object.status = "Existing Data Evaluation Done"
    demo_object.save()

    # Provide feedback and redirect
    messages.info(request, " Evaluation Existing Data  Processed Successfully")
    return redirect("/eval_scan/")



from django.shortcuts import redirect
from django.contrib import messages
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor



def calculate_proposed(request, project_id):

    # Retrieve the demo object using the project_id
    demo_object = demo.objects.get(project_id=project_id)

    # Fetch values from the database
    circumference_of_skin_needed = float(demo_object.circumference_of_skin_needed)
    mussel_glue_needed = float(demo_object.mussel_glue_needed)
    grafting_operation_time_taken = float(demo_object.grafting_operation_time_taken)
    time_taken_for_curing = float(demo_object.time_taken_for_curing)

    # Load proposed dataset
    proposed_dataset = pd.read_csv("E:/company_project/PROJECT/Skin grafting/proposed skin grafting.csv")

    # Prepare data for Gradient Boosting Regressor
    X_proposed = proposed_dataset[['Circumference of Skin (cm)', 'Glue Needed (mg)', 'Grafting Time (hrs)', 'Time for Curing (months)']]
    y_proposed_side_effects = proposed_dataset['Side Effects (%)']
    y_proposed_scar = proposed_dataset['Scar (%)']

    # Append the database values as a new row to X_proposed
    new_row = pd.DataFrame({
        'Circumference of Skin (cm)': [circumference_of_skin_needed],
        'Glue Needed (mg)': [mussel_glue_needed],
        'Grafting Time (hrs)': [grafting_operation_time_taken],
        'Time for Curing (months)': [time_taken_for_curing]
    })

    # Concatenate the new row with the proposed dataset
    X_proposed_with_db = pd.concat([X_proposed, new_row], ignore_index=True)

    # Initialize the Gradient Boosting Regressor models
    model_side_effects = GradientBoostingRegressor(n_estimators=100, random_state=42)
    model_scar = GradientBoostingRegressor(n_estimators=100, random_state=42)

    # Fit the models with the updated dataset (including the new row from the database)
    model_side_effects.fit(X_proposed, y_proposed_side_effects)
    model_scar.fit(X_proposed, y_proposed_scar)

    # Predict side effects and scar percentages for the entire dataset, including the new row
    predicted_proposed_side_effects = model_side_effects.predict(X_proposed_with_db)
    predicted_proposed_scar = model_scar.predict(X_proposed_with_db)

    # Extract the predictions for the new row (which corresponds to the last row in the dataset)
    new_predicted_side_effects = predicted_proposed_side_effects[-1]
    new_predicted_scar = predicted_proposed_scar[-1]

    # Update demo object with the predictions for the new row
    demo_object.predicted_proposed_side_effects = round(new_predicted_side_effects)
    demo_object.predicted_proposed_scar = round(new_predicted_scar)
    demo_object.eval_proposed_scanned = True
    demo_object.evaluation = True
    demo_object.rep = True
    demo_object.status = "Proposed Data Evaluation Done"
    demo_object.save()

    # Provide feedback and redirect
    messages.info(request, "Evaluation Proposed Data Processed Successfully")
    return redirect("/eval_file/")

from django.db.models import Q

def eval_file(request):
    # Use Q objects to apply OR condition
    data = demo.objects.filter(Q(eval_existing_scanned=True) | Q(eval_proposed_scanned=True))
    context = {'data': data}
    return render(request, 'evaluation/eval_file.html', context)


def eval_logout(request):
    if 'user_id' in request.session:
        user_id = request.session.get('user_id')
        try:
            del request.session['user_id']
            messages.info(request, 'Evaluation Logout successful')
            return redirect('/')
        except demo.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('/')
    messages.info(request, 'Evaluation Logout successful')
    return redirect('/')