
## Paquete con funciones de ayuda para envio de mensajeria sns, sqs de AWS (obligatorias) ##

Para poder operar con este paquete de forma correcta, no olvidar setear estas variables en su settings.py

**AWS_REGION_NAME** = os.environ.get('AWS_REGION_NAME')

**AWS_ACCESS_KEY_ID** = os.environ.get('AWS_ACCESS_KEY_ID')

**AWS_SECRET_ACCESS_KEY** = os.environ.get('AWS_SECRET_ACCESS_KEY')


## Variables de Entorno para disitntos Ambientes (no obligatorias) ##

**ENVIRONMENT** = "STAGING" OR "PRODUCTION" OR "DEVEL"

**COUNTRY_PREFIX** = "CL" OR "MX" 

# Estas variabes se agregaran automaticamente como atributo en los mensajes SNS


### Para instalar este paquete use pip de la siguiente forma: ###


**pip install django-sns-sqs-services**


### Para uso de este paquete, importe la libreria de la siguiente forma: ###


**from sns_sqs_services.services import SqsService, SnsService**


