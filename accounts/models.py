from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.db.models.signals import post_save
#from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField


import os

from . managers import UserManager


# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):
	user_type_data=((1,"HOD"),(2,"ClientUser"),(3,"CustomerUser"), (4,"Employee"))
	user_type=models.CharField(default=1,choices=user_type_data,max_length=10)

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	LOCATION_CHOICES = [
		('AF', 'Afghanistan'), ('AX', 'Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'),('AO', 'Angola'),('AI', 'Anguilla'), ('AQ', 'Antarctica'),
		('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'),
		('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BQ', 'Bonaire'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'),
		('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'),
		('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'),
		('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, Democratic Republic'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Cote d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'),
		('CW', 'Curacao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'),
		('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'),
		('Faroe Islands', 'FO'), ('Fiji', 'FJ'), ('Finland', 'FI'), ('France', 'FR'), ('French Guiana', 'GF'),
		('French Polynesia', 'PF'), ('French Southern Territories', 'TF'), ('Gabon', 'GA'), ('Gambia', 'GM'), ('Georgia', 'GE'),
		('Germany', 'DE'), ('Ghana', 'GH'), ('Gibraltar', 'GI'), ('Greece', 'GR'), ('Greenland', 'GL'), ('Grenada', 'GD'), ('Guadeloupe', 'GP'), ('Guam', 'GU'), ('Guatemala', 'GT'), ('Guernsey', 'GG'),
		('Guinea', 'GN'), ('Guinea-Bissau', 'GW'), ('Guyana', 'GY'), ('Haiti', 'HT'), ('Heard Island and McDonald Islands', 'HM'), ('Holy See (Vatican City State)', 'VA'), ('Honduras', 'HN'), ('Hong Kong', 'HK'), ('Hungary', 'HU'),
		('Iceland', 'IS'), ('India', 'IN'), ('Indonesia', 'ID'), ('Iran, Islamic Republic of', 'IR'),('Iraq', 'IQ'), ('Ireland', 'IE'), ('Isle of Man', 'IM'), ('Israel', 'IL'), ('Italy', 'IT'),
		('Jamaica', 'JM'), ('Japan', 'JP'), ('Jersey', 'JE'), ('Jordan', 'JO'), ('Kazakhstan', 'KZ'), ('Kenya', 'KE'), ('Kiribati', 'KI'), ("Korea, Democratic People's Republic of", 'KP'), ('Korea, Republic of', 'KR'), ('Kuwait', 'KW'), ('Kyrgyzstan', 'KG'),
		("Lao People's Democratic Republic", 'LA'), ('Latvia', 'LV'), ('Lebanon', 'LB'), ('Lesotho', 'LS'), ('Liberia', 'LR'), ('Libya', 'LY'), ('Liechtenstein', 'LI'), ('Lithuania', 'LT'),
		('Luxembourg', 'LU'), ('Macao', 'MO'), ('Macedonia, the Former Yugoslav Republic of', 'MK'), ('Madagascar', 'MG'), ('Malawi', 'MW'), ('Malaysia', 'MY'), ('Maldives', 'MV'), ('Mali', 'ML'),
		('Malta', 'MT'), ('Marshall Islands', 'MH'), ('Martinique', 'MQ'), ('Mauritania', 'MR'), ('Mauritius', 'MU'), ('Mayotte', 'YT'), ('Mexico', 'MX'), ('Micronesia, Federated States of', 'FM'),
		('Moldova, Republic of', 'MD'), ('Monaco', 'MC'), ('Mongolia', 'MN'), ('Montenegro', 'ME'), ('Montserrat', 'MS'), ('Morocco', 'MA'), ('Mozambique', 'MZ'), ('Myanmar', 'MM'), ('Namibia', 'NA'),
		('Nauru', 'NR'), ('Nepal', 'NP'), ('Netherlands', 'NL'), ('New Caledonia', 'NC'), ('New Zealand', 'NZ'), ('Nicaragua', 'NI'), ('Niger', 'NE'), ('Nigeria', 'NG'), ('Niue', 'NU'), ('Norfolk Island', 'NF'),
		('Northern Mariana Islands', 'MP'), ('Norway', 'NO'), ('Oman', 'OM'), ('Pakistan', 'PK'), ('Palau', 'PW'), ('Palestine, State of', 'PS'), ('Panama', 'PA'), ('Papua New Guinea', 'PG'), ('Paraguay', 'PY'), ('Peru', 'PE'),
		('Philippines', 'PH'), ('Pitcairn', 'PN'), ('Poland', 'PL'), ('Portugal', 'PT'), ('Puerto Rico', 'PR'), ('Qatar', 'QA'), ('Reunion', 'RE'), ('Romania', 'RO'), ('Russian Federation', 'RU'), ('Rwanda', 'RW'),
		('Saint BarthÃ©lemy', 'BL'), ('Saint Helena, Ascension and Tristan da Cunha', 'SH'), ('Saint Kitts and Nevis', 'KN'),
		('Saint Lucia', 'LC'), ('Saint Martin (French part)', 'MF'), ('Saint Pierre and Miquelon', 'PM'), ('Saint Vincent and the Grenadines', 'VC'), ('Samoa', 'WS'), ('San Marino', 'SM'), ('Sao Tome and Principe', 'ST'),
		('Saudi Arabia', 'SA'), ('Senegal', 'SN'), ('Serbia', 'RS'), ('Seychelles', 'SC'), ('Sierra Leone', 'SL'), ('Singapore', 'SG'), ('Sint Maarten (Dutch part)', 'SX'), ('Slovakia', 'SK'), ('Slovenia', 'SI'), ('Solomon Islands', 'SB'),
		('Somalia', 'SO'), ('South Africa', 'ZA'), ('South Georgia and the South Sandwich Islands', 'GS'), ('South Sudan', 'SS'), ('Spain', 'ES'), ('Sri Lanka', 'LK'), ('Sudan', 'SD'), ('Suriname', 'SR'),
		('Svalbard and Jan Mayen', 'SJ'), ('Swaziland', 'SZ'), ('Sweden', 'SE'), ('Switzerland', 'CH'), ('Syrian Arab Republic', 'SY'), ('Taiwan, Province of China', 'TW'), ('Tajikistan', 'TJ'), ('Tanzania, United Republic of', 'TZ'), ('Thailand', 'TH'), ('Timor-Leste', 'TL'), ('Togo', 'TG'),
		('Tokelau', 'TK'), ('Tonga', 'TO'), ('Trinidad and Tobago', 'TT'), ('Tunisia', 'TN'), ('Turkey', 'TR'), ('Turkmenistan', 'TM'), ('Turks and Caicos Islands', 'TC'), ('Tuvalu', 'TV'), ('Uganda', 'UG'), ('Ukraine', 'UA'),
		('United Arab Emirates', 'AE'), ('United Kingdom', 'GB'), ('United States', 'US'), ('United States Minor Outlying Islands', 'UM'),('Uruguay', 'UY'),('Uzbekistan', 'UZ'), ('Vanuatu', 'VU'), ('Venezuela, Bolivarian Republic of', 'VE'),
		('Viet Nam', 'VN'), ('Virgin Islands, British', 'VG'), ('Virgin Islands, U.S.', 'VI'), ('Wallis and Futuna', 'WF'), ('Western Sahara', 'EH'), ('Yemen', 'YE'), ('Zambia', 'ZM'), ('Zimbabwe', 'ZW'),
	]

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)


	email = models.EmailField(unique=True)
	name = models.CharField(max_length=120)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	date_of_birth = models.DateField(blank=True, null=True)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	uid = models.CharField(max_length=10, unique=True, verbose_name='User Identifier', default='')
	is_staff = models.BooleanField(default=False)
	is_customer = models.BooleanField(default=True)
	is_employee = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	date_joined = models.DateTimeField(default=timezone.now)
	modified_at = models.DateTimeField(auto_now=True)
	last_login = models.DateTimeField(null=True)
	location = models.CharField(max_length=120, choices=LOCATION_CHOICES, verbose_name='Location')


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['name', 'phone']


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.name.split()[0]	

class AdminHOD(models.Model):
    admin=models.OneToOneField(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    

class ClientUser(models.Model):

	MALE = 'MALE'
	FEMALE = 'FEMALE'

	GENDER_CHOICES = (
		(MALE, 'Male'),
		(FEMALE, 'Female'),
	)

	LOCATION_CHOICES = [
		('AF', 'Afghanistan'), ('AX', 'Islands'), ('AL', 'Albania'), ('DZ', 'Algeria'), ('AS', 'American Samoa'), ('AD', 'Andorra'),('AO', 'Angola'),('AI', 'Anguilla'), ('AQ', 'Antarctica'),
		('AG', 'Antigua and Barbuda'), ('AR', 'Argentina'), ('AM', 'Armenia'), ('AW', 'Aruba'), ('AU', 'Australia'), ('AT', 'Austria'), ('AZ', 'Azerbaijan'), ('BS', 'Bahamas'), ('BH', 'Bahrain'), ('BD', 'Bangladesh'),
		('BB', 'Barbados'), ('BY', 'Belarus'), ('BE', 'Belgium'), ('BZ', 'Belize'), ('BJ', 'Benin'), ('BM', 'Bermuda'),('BT', 'Bhutan'), ('BO', 'Bolivia'), ('BQ', 'Bonaire'), ('BA', 'Bosnia and Herzegovina'), ('BW', 'Botswana'), ('BV', 'Bouvet Island'),
		('BR', 'Brazil'), ('IO', 'British Indian Ocean Territory'), ('BN', 'Brunei Darussalam'), ('BG', 'Bulgaria'), ('BF', 'Burkina Faso'), ('BI', 'Burundi'), ('KH', 'Cambodia'), ('CM', 'Cameroon'),
		('CA', 'Canada'), ('CV', 'Cape Verde'), ('KY', 'Cayman Islands'), ('CF', 'Central African Republic'), ('TD', 'Chad'), ('CL', 'Chile'), ('CN', 'China'), ('CX', 'Christmas Island'), ('CC', 'Cocos (Keeling) Islands'),
		('CO', 'Colombia'), ('KM', 'Comoros'), ('CG', 'Congo'), ('CD', 'Congo, Democratic Republic'), ('CK', 'Cook Islands'), ('CR', 'Costa Rica'), ('CI', "Cote d'Ivoire"), ('HR', 'Croatia'), ('CU', 'Cuba'),
		('CW', 'Curacao'), ('CY', 'Cyprus'), ('CZ', 'Czech Republic'), ('DK', 'Denmark'), ('DJ', 'Djibouti'), ('DM', 'Dominica'), ('DO', 'Dominican Republic'), ('EC', 'Ecuador'), ('EG', 'Egypt'), ('SV', 'El Salvador'),
		('GQ', 'Equatorial Guinea'), ('ER', 'Eritrea'), ('EE', 'Estonia'), ('ET', 'Ethiopia'), ('FK', 'Falkland Islands (Malvinas)'),
		('Faroe Islands', 'FO'), ('Fiji', 'FJ'), ('Finland', 'FI'), ('France', 'FR'), ('French Guiana', 'GF'),
		('French Polynesia', 'PF'), ('French Southern Territories', 'TF'), ('Gabon', 'GA'), ('Gambia', 'GM'), ('Georgia', 'GE'),
		('Germany', 'DE'), ('Ghana', 'GH'), ('Gibraltar', 'GI'), ('Greece', 'GR'), ('Greenland', 'GL'), ('Grenada', 'GD'), ('Guadeloupe', 'GP'), ('Guam', 'GU'), ('Guatemala', 'GT'), ('Guernsey', 'GG'),
		('Guinea', 'GN'), ('Guinea-Bissau', 'GW'), ('Guyana', 'GY'), ('Haiti', 'HT'), ('Heard Island and McDonald Islands', 'HM'), ('Holy See (Vatican City State)', 'VA'), ('Honduras', 'HN'), ('Hong Kong', 'HK'), ('Hungary', 'HU'),
		('Iceland', 'IS'), ('India', 'IN'), ('Indonesia', 'ID'), ('Iran, Islamic Republic of', 'IR'),('Iraq', 'IQ'), ('Ireland', 'IE'), ('Isle of Man', 'IM'), ('Israel', 'IL'), ('Italy', 'IT'),
		('Jamaica', 'JM'), ('Japan', 'JP'), ('Jersey', 'JE'), ('Jordan', 'JO'), ('Kazakhstan', 'KZ'), ('Kenya', 'KE'), ('Kiribati', 'KI'), ("Korea, Democratic People's Republic of", 'KP'), ('Korea, Republic of', 'KR'), ('Kuwait', 'KW'), ('Kyrgyzstan', 'KG'),
		("Lao People's Democratic Republic", 'LA'), ('Latvia', 'LV'), ('Lebanon', 'LB'), ('Lesotho', 'LS'), ('Liberia', 'LR'), ('Libya', 'LY'), ('Liechtenstein', 'LI'), ('Lithuania', 'LT'),
		('Luxembourg', 'LU'), ('Macao', 'MO'), ('Macedonia, the Former Yugoslav Republic of', 'MK'), ('Madagascar', 'MG'), ('Malawi', 'MW'), ('Malaysia', 'MY'), ('Maldives', 'MV'), ('Mali', 'ML'),
		('Malta', 'MT'), ('Marshall Islands', 'MH'), ('Martinique', 'MQ'), ('Mauritania', 'MR'), ('Mauritius', 'MU'), ('Mayotte', 'YT'), ('Mexico', 'MX'), ('Micronesia, Federated States of', 'FM'),
		('Moldova, Republic of', 'MD'), ('Monaco', 'MC'), ('Mongolia', 'MN'), ('Montenegro', 'ME'), ('Montserrat', 'MS'), ('Morocco', 'MA'), ('Mozambique', 'MZ'), ('Myanmar', 'MM'), ('Namibia', 'NA'),
		('Nauru', 'NR'), ('Nepal', 'NP'), ('Netherlands', 'NL'), ('New Caledonia', 'NC'), ('New Zealand', 'NZ'), ('Nicaragua', 'NI'), ('Niger', 'NE'), ('Nigeria', 'NG'), ('Niue', 'NU'), ('Norfolk Island', 'NF'),
		('Northern Mariana Islands', 'MP'), ('Norway', 'NO'), ('Oman', 'OM'), ('Pakistan', 'PK'), ('Palau', 'PW'), ('Palestine, State of', 'PS'), ('Panama', 'PA'), ('Papua New Guinea', 'PG'), ('Paraguay', 'PY'), ('Peru', 'PE'),
		('Philippines', 'PH'), ('Pitcairn', 'PN'), ('Poland', 'PL'), ('Portugal', 'PT'), ('Puerto Rico', 'PR'), ('Qatar', 'QA'), ('Reunion', 'RE'), ('Romania', 'RO'), ('Russian Federation', 'RU'), ('Rwanda', 'RW'),
		('Saint BarthÃ©lemy', 'BL'), ('Saint Helena, Ascension and Tristan da Cunha', 'SH'), ('Saint Kitts and Nevis', 'KN'),
		('Saint Lucia', 'LC'), ('Saint Martin (French part)', 'MF'), ('Saint Pierre and Miquelon', 'PM'), ('Saint Vincent and the Grenadines', 'VC'), ('Samoa', 'WS'), ('San Marino', 'SM'), ('Sao Tome and Principe', 'ST'),
		('Saudi Arabia', 'SA'), ('Senegal', 'SN'), ('Serbia', 'RS'), ('Seychelles', 'SC'), ('Sierra Leone', 'SL'), ('Singapore', 'SG'), ('Sint Maarten (Dutch part)', 'SX'), ('Slovakia', 'SK'), ('Slovenia', 'SI'), ('Solomon Islands', 'SB'),
		('Somalia', 'SO'), ('South Africa', 'ZA'), ('South Georgia and the South Sandwich Islands', 'GS'), ('South Sudan', 'SS'), ('Spain', 'ES'), ('Sri Lanka', 'LK'), ('Sudan', 'SD'), ('Suriname', 'SR'),
		('Svalbard and Jan Mayen', 'SJ'), ('Swaziland', 'SZ'), ('Sweden', 'SE'), ('Switzerland', 'CH'), ('Syrian Arab Republic', 'SY'), ('Taiwan, Province of China', 'TW'), ('Tajikistan', 'TJ'), ('Tanzania, United Republic of', 'TZ'), ('Thailand', 'TH'), ('Timor-Leste', 'TL'), ('Togo', 'TG'),
		('Tokelau', 'TK'), ('Tonga', 'TO'), ('Trinidad and Tobago', 'TT'), ('Tunisia', 'TN'), ('Turkey', 'TR'), ('Turkmenistan', 'TM'), ('Turks and Caicos Islands', 'TC'), ('Tuvalu', 'TV'), ('Uganda', 'UG'), ('Ukraine', 'UA'),
		('United Arab Emirates', 'AE'), ('United Kingdom', 'GB'), ('United States', 'US'), ('United States Minor Outlying Islands', 'UM'),('Uruguay', 'UY'),('Uzbekistan', 'UZ'), ('Vanuatu', 'VU'), ('Venezuela, Bolivarian Republic of', 'VE'),
		('Viet Nam', 'VN'), ('Virgin Islands, British', 'VG'), ('Virgin Islands, U.S.', 'VI'), ('Wallis and Futuna', 'WF'), ('Western Sahara', 'EH'), ('Yemen', 'YE'), ('Zambia', 'ZM'), ('Zimbabwe', 'ZW'),
	]

	email = models.EmailField(unique=True)
	name = models.CharField(max_length=120)
	phone = PhoneNumberField(unique=True)
	first_name = models.CharField(max_length=120)
	last_name = models.CharField(max_length=120)
	gender = models.CharField(max_length=6, choices=GENDER_CHOICES, verbose_name='Gender')
	address = models.CharField(max_length=255)
	city = models.CharField(max_length=100)
	age = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	modifed_at = models.DateTimeField(auto_now=True)
	location = models.CharField(max_length=120, choices=LOCATION_CHOICES, verbose_name='Location')
	save_by = models.ForeignKey(User, on_delete=models.PROTECT)


	objects = UserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []


	def get_full_name(self):
		return f'{self.first_name }'+' '+ f'{self.last_name}'.title()

	def get_short_name(self):
		return self.name.split()[0]



class CustomerUser(models.Model):
	STATUS = [
		('customer', 'customer'),
		('employee', 'employee'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS, default='customer')

	def __str__(self):
		return self.get_full_name
 	

class Employee(models.Model):

	STATUS = [
		('customer', 'customer'),
		('employee', 'employee'),
	]

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	status = models.CharField(max_length=10, choices=STATUS, default='employee')

	def __str__(self):
		return self.get_full_name	


class CustomerProfile(models.Model):

	def image_upload_to(self, instance=None):
		if instance:
			return os.path.join("Users", self.username, instance)
		return None	

	user = models.OneToOneField(CustomerUser, on_delete=models.CASCADE)
	follows = models.ManyToManyField('self', 
		related_name='followed_by', 
		symmetrical=False, blank=True)
	image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
	description = models.TextField('Description', max_length=200, default='', blank=True)
	date_modified = models.DateTimeField(CustomerUser, auto_now=True)


	def __str__(self):
		return self.user.get_full_name


#Create Profile when new user Sign up
#@receiver(post_save, sender=CustomerUser)
def create_customerProfile(sender, instance, created, **kwargs):
	if created:
		user_customerProfile = CustomerUser(user=instance)
		user_customerProfile.save()

post_save.connect(create_customerProfile, sender=CustomerUser)	



class EmployeeProfile(models.Model):

	def image_upload_to(self, instance=None):
		if instance:
			return os.path.join("Users", self.username, instance)
		return None	

	user = models.OneToOneField(Employee, on_delete=models.CASCADE)
	follows = models.ManyToManyField('self', 
		related_name='followed_by', 
		symmetrical=False, blank=True)
	function = models.CharField('Designation', max_length=100)
	session_start_year=models.DateField()
	session_end_year=models.DateField()
	image = models.ImageField(default='default/user.jpg', upload_to=image_upload_to)
	description = models.TextField('Description', max_length=200, default='', blank=True)
	date_modified = models.DateTimeField(Employee, auto_now=True)


	def __str__(self):
		return self.user.get_full_name


#Create Profile when new user Sign up
#@receiver(post_save, sender=CustomerUser)
def create_employeeProfile(sender, instance, created, **kwargs):
	if created:
		user_employeeProfile = Employee(user=instance)
		user_employeeProfile.save()

post_save.connect(create_employeeProfile, sender=Employee)	


class Subjects(models.Model):
    subject_name=models.CharField(max_length=255)
    employee_id=models.ForeignKey(User,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.subject_name



class Attendance(models.Model):
    subject_id=models.ForeignKey(Subjects,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.subject_id.subject_name



class AttendanceReport(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name
    

class LeaveReportEmployee(models.Model):
    employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
    leave_date=models.CharField(max_length=255)
    leave_message=models.TextField()
    leave_status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name


class FeedBackEmployee(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name


class NotificationEmployee(models.Model):
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
    	return self.employee_id.user.name
		







