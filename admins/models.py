from django.db import models



class main(models.Model):

    # all modules register and login

    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    department= models.CharField(max_length=100, null=True)


    #user_id and mail password generation

    rh_id= models.CharField(max_length=100, null=True)
    password=models.PositiveBigIntegerField(null=True)



    # admin approve and reject

    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)

    # login and logout

    login = models.BooleanField(default=False)
    logout = models.BooleanField(default=False)



class demo(models.Model):

    # project_id........................................................

    project_id = models.CharField(max_length=100, null=True)

    # admin requirements and datas before ecryption.......................

    name_of_the_patient = models.CharField(max_length=100, null=True)
    age = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    type_of_wound = models.CharField(max_length=100, null=True)
    wound_placement = models.CharField(max_length=100, null=True)
    depth_of_wound = models.CharField(max_length=100, null=True)
    circumference_of_the_wound = models.CharField(max_length=100, null=True)




    # Module 1 - Exfoliation
    # admin requirements and datas after ecryption

    encrypted_name_of_the_patient = models.CharField(max_length=100, null=True)
    encrypted_age = models.CharField(max_length=100, null=True)
    encrypted_gender = models.CharField(max_length=100, null=True)
    encrypted_type_of_wound = models.CharField(max_length=100, null=True)
    encrypted_wound_placement = models.CharField(max_length=100, null=True)
    encrypted_depth_of_wound = models.CharField(max_length=100, null=True)
    encrypted_circumference_of_the_wound= models.CharField(max_length=100, null=True)


    # encryption key

    exfo_decryption_key = models.CharField(max_length=64,null=True)

    # get key and decrypt

    exfo_get_key = models.BooleanField(default=False,null=True)
    exfo_decrypt = models.BooleanField(default=False,null=True)


    # Exfo - Scanning

    circumference_of_skin_needed = models.CharField(max_length=100,null=True)
    type_of_material = models.CharField(max_length=100, null=True)
    place_of_skin_peeling = models.CharField(max_length=100, null=True)
    holes_made_ratio = models.CharField(max_length=10, null=True)

    #Module 2 - Bio Adhesion

    encrypted_circumference_of_skin_needed = models.CharField(max_length=100, null=True)
    encrypted_type_of_material = models.CharField(max_length=100, null=True)
    encrypted_place_of_skin_peeling = models.CharField(max_length=100, null=True)
    encrypted_holes_made_ratio = models.CharField(max_length=10, null=True)

    # encryption key

    bio_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    bio_get_key = models.BooleanField(default=False, null=True)
    bio_decrypt = models.BooleanField(default=False, null=True)

    # bio - Scanning

    mussel_glue_needed = models.CharField(max_length=100, null=True)
    mussel_needed = models.CharField(max_length=100, null=True)
    allantoin_needed = models.CharField(max_length=100, null=True)
    egf_needed = models.CharField(max_length=100, null=True)



    # Module - 3 - Dermatoplasty

    encrypted_mussel_glue_needed = models.CharField(max_length=100, null=True)
    encrypted_mussel_needed = models.CharField(max_length=100, null=True)
    encrypted_allantoin_needed = models.CharField(max_length=100, null=True)
    encrypted_egf_needed = models.CharField(max_length=100, null=True)

    # encryption key

    dermato_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    dermato_get_key = models.BooleanField(default=False, null=True)
    dermato_decrypt = models.BooleanField(default=False, null=True)

    # dermato - Scanning

    grafting_operation_time_taken = models.CharField(max_length=100, null=True)
    sterile_solution = models.CharField(max_length=100, null=True)



    # Module - 4 - monitoring

    encrypted_grafting_operation_time_taken= models.CharField(max_length=100, null=True)
    encrypted_sterile_solution = models.CharField(max_length=100, null=True)


    # encryption key

    monitor_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    monitor_get_key = models.BooleanField(default=False, null=True)
    monitor_decrypt = models.BooleanField(default=False, null=True)

    # monitor - Scanning

    time_taken_for_curing = models.CharField(max_length=100, null=True)
    types_of_food_to_follow = models.CharField(max_length=100, null=True)
    patient_progress = models.CharField(max_length=100, null=True)


    # Module - 5 - evaluation

    encrypted_time_taken_for_curing = models.CharField(max_length=100, null=True)
    encrypted_types_of_food_to_follow= models.CharField(max_length=100, null=True)
    encrypted_patient_progress = models.CharField(max_length=100, null=True)

    # encryption key

    eval_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    eval_get_key = models.BooleanField(default=False, null=True)
    eval_decrypt = models.BooleanField(default=False, null=True)

    # evaluation - scanning

         # existing grafting

    predicted_existing_side_effects = models.CharField(max_length=100, null=True)
    predicted_existing_scar = models.CharField(max_length=100, null=True)


        # proposed grafting

    predicted_proposed_side_effects = models.CharField(max_length=100, null=True)
    predicted_proposed_scar = models.CharField(max_length=100, null=True)


    ## all modules scanned name

    exfo_scanned = models.BooleanField(default=False)
    bio_scanned =  models.BooleanField(default=False)
    dermato_scanned = models.BooleanField(default=False)
    monitor_scanned = models.BooleanField(default=False)

    eval_existing_scanned = models.BooleanField(default=False)
    evaluation = models.BooleanField(default=False,null=True)
    eval_proposed_scanned = models.BooleanField(default=False)


    # all modules status

    status = models.CharField(default="Pending", null=True , max_length=100)

    # reports

    report = models.BooleanField(default=False)
    rep = models.BooleanField(default=False)

    f_report = models.FileField(null=True, upload_to="Final_Report/")














