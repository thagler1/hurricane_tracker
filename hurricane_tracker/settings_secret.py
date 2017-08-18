# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm5qa!!rx7pvmt6eby=h$o$t)v@1xmbftjg16r4=mz9e+u36uxz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['trackingcyclones.com','www.trackingcyclones.com','cyclconetracker.com','www.cyclconetracker.com','104.236.67.246']

DATABASES = {
	'default':{
	'ENGINE': 'django.contrib.gis.db.backends.postgis',
	'NAME': 'hurricane',
	'USER':'todd',
	'PASSWORD':'M82a1aPOT!4',
	'HOST':'localhost',
	'PORT':''
}
}
