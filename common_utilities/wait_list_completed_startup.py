#<==================================================================================================>
#                                      IMPORTS
#<==================================================================================================>
import sys
import boto3
import logging
sys.path.append('../')
from common_utilities import CONSTANT
from botocore.exceptions import ClientError


#<==================================================================================================>
#                                        LOGGER
#<==================================================================================================>
logger = logging.getLogger(__name__)


#<==================================================================================================>
#                              STARTUP WAIT LIST OVER EMAIL TEMPLATE
#<==================================================================================================>
def wait_list_over_str(user_email, first_name):
    RECIPIENT = [user_email]
    SENDER = CONSTANT.EMAIL_SENDER.value
    AWS_REGION = CONSTANT.EMAIL_REGION.value
    AWS_ACCESS_KEY = CONSTANT.ACCESS_KEY.value
    AWS_ACCESS_VALUE = CONSTANT.ACCESS_VALUE.value
    SUBJECT = f"Welcome to Angelfund.ai, {first_name}!"
    BODY_HTML = f"""
<html>
   <head>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
      <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css"
         integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T"">
      <style>
         body,
         html {{
         margin: 0 !important;
         padding: 0 !important;
         }}
         .container {{
         display: block !important;
         width: 800px !important;
         margin: auto !important;
         font-family: "Roboto", sans-serif !important;
         border: 2px solid #f3f3f3 !important;
         box-shadow: 0px 2px 3px 0px #f2f2ff !important;
         margin-top: 5% !important;
         border-radius: 5px !important;
         }}
         p,
         h1,
         .sizing {{
         font-family: "Roboto", sans-serif !important;
         }}
         p {{
         margin: 30px 0 !important;
         }}
         .logo {{
         display: block !important;
         margin: auto !important;
         text-align: center !important;
         padding-top: 10px !important;
         }}
         .title {{
         padding-top: 30px;
         padding-bottom: 10px;
         padding-left: 10px;
         border-bottom: 2px solid #e6e6e6;
         }}
         .hook {{
         padding-top: 5px;
         text-align: left;
         padding-bottom: 10px;
         margin: 3%;
         }}
         .footer {{
         margin: auto !important;
         left: 0%;
         bottom: 0%;
         width: 800px;
         text-align: center;
         background-color: lightgrey;
         opacity: 0.3;
         padding: 2% 0;
         }}
         h1 {{
         font-size: 28px !important;
         font-family: Lato;
         font-weight: 500;
         color: #707070;
         }}
         strong {{
         font-weight: 500;
         }}
         .sizing {{
         font-size: 19px !important;
         }}
         a {{
         transition: all 0.5s ease-in-out;
         }}
         a:hover {{
         font-size: 18px;
         }}
         .font-roboto {{
         font-family: "Roboto", sans-serif;
         }}
         .font-color-prime {{
         color: #5e51f4;
         }}
         .font-18 {{
         font-size: 18px;
         }}
         .font-16 {{
         font-size: 16px;
         position: relative;
         top: -20px;
         }}
         .font-15 {{
         font-size: 15px;
         text-align: center;
         position: relative;
         top: -15px;
         }}
         .how-it-works-container {{
         position: relative;
         top: -15px;
         height: 525px;
         width: 100%;
         align-items: center;
         }}
         .how-it-works-container .processLine {{
         width: 24px;
         }}
         .how-it-works-container .row {{
         height: 160px;
         align-items: center;
         }}
         .how-it-works-container .row .img {{
         display: flex;
         justify-content: left;
         align-self: center;
         }}
         .how-it-works-container .row .img img {{
         width: 100px;
         margin-left: 5px;
         }}
         .col-10 {{
         padding-left: 30px;
         }}
         button {{
         height: 50px;
         width: 100%;
         margin: 10px 0 35px;
         padding: 10px 30px;
         background-color: #5e51f4;
         color: white;
         font-size: 16px;
         font-weight: bold;
         border-radius: 5px;
         box-shadow: none;
         border: none;
         transition: all 0.5s ease-in-out;
         }}
         button:hover {{
         transform: scale(1.1);
         }}
         @media only screen and (max-width: 800px) {{
         .logo {{
         padding-left: 5%;
         margin: 0px !important;
         text-align: left !important;
         }}
         .container {{
         margin: 0px !important;
         padding: 0% !important;
         border: none !important;
         box-shadow: none !important;
         width: 100% !important;
         }}
         .hook {{
         display: block;
         margin: auto;
         width: 80%;
         }}
         h1 {{
         font-size: 20px !important;
         }}
         .sizing {{
         font-size: 17px !important;
         }}
         .title {{
         padding-left: 5% !important;
         margin-left: 0% !important;
         }}
         .footer {{
         font-size: 15px;
         margin: 0%;
         width: 100%;
         }}
         button {{
         margin-left: 0px !important;
         }}
         .font-18 {{
         font-size: 16px !important;
         text-align: center !important;
         }}
         .w-25 {{
         display: block;
         margin: auto;
         }}
         }}
      </style>
   </head>
   <body>
      <div class="container">
         <div class="logo">
            <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/Angelfund.ai+Logo.png"
               style="height: 30px;" />
         </div>
         <div class="title">
            <h1>
               Welcome to Angelfund.ai, {first_name}! 🎉
            </h1>
         </div>
         <div class="hook">
            <p class="sizing">
               Hey {first_name}—
            </p>
            <p class="sizing">
               <strong>You've made it off the waitlist!</strong> We're thrilled to
               start introducing you to relevant investors on Angelfund.ai.
            </p>
            <p class="sizing">
               Before you get started, here's a quick refresher on how our platform
               works:
            </p>
            <!-- larger screen  -->
            <div class="container-lg d-none d-md-block">
               <div class="row how-it-works-container">
                  <div class="col-md-1">
                     <img class="processLine"
                        src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/Off+the+Waitlist+Arrows.png"
                        alt="process line"></img>
                  </div>
                  <div class="col-md-11 container-fluid">
                     <div class="row mb-0">
                        <div class="col-md-3  col-10 img">
                           <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/How+it+works+1.png"
                              alt="img one"></img>
                        </div>
                        <div class="col-md-9 col-10">
                           <p class="font-weight-bold font-18 font-roboto font-color-prime">
                              Tell us about your startup.
                           </p>
                           <span class="font-16 font-roboto">
                           You've already told us what your startup does and how much you're looking to raise.
                           </span>
                        </div>
                     </div>
                     <div class="row mb-0">
                        <div class="col-md-3 col-10 img">
                           <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/How+it+works+2.png"
                              alt="img two"></img>
                        </div>
                        <div class="col-md-9 col-10 ">
                           <p class="font-weight-bold font-18 font-roboto font-color-prime">
                              We'll show you relevant investors.
                           </p>
                           <p class="font-16 font-roboto">
                              Find and invite angel investors who actively invest in startups like yours.
                           </p>
                        </div>
                     </div>
                     <div class="row mb-0">
                        <div class="col-md-3 col-10 img">
                           <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/How+it+works+3.png"
                              alt="img three"></img>
                        </div>
                        <div class="col-md-9 col-10">
                           <p class="font-weight-bold font-18 font-roboto font-color-prime">
                              Get introduced to your favorites.
                           </p>
                           <p class="font-16 font-roboto">
                              We’ll send a warm intro via email connecting you with interested investors. <br>
                              If an investor passes on you, we'll let you know why.
                           </p>
                        </div>
                     </div>
                  </div>
               </div>
            </div>
            <!-- small screen  -->
            <div class="container-sm d-block d-md-none">
               <div class="container header-context-wrapper align-center  my-5">
                  <img class="w-25 mt-5" src="assets/how-it-works-startup.svg" alt="start up img"></img>
                  <div class="my-2">
                     <p class="font-weight-bold font-18 font-roboto font-color-prime">
                        Tell us about your startup.
                     </p>
                     <p class="font-15 font-roboto">
                        You've already told us what your startup does and how much you're looking to raise.
                     </p>
                  </div>
                  <img class="w-25 mt-3" src="assets/how-it-works-investor.svg" alt="investor img"></img>
                  <div class="my-2">
                     <p class="font-weight-bold font-18 font-roboto font-color-prime">
                        We'll show you relevant investors.
                     </p>
                     <p class="font-15 font-roboto">
                        Find and invite angel investors who actively invest in startups like yours.
                     </p>
                  </div>
                  <img class="w-25  mt-3" src="assets/how-it-works-feedback.svg" alt="investor img"></img>
                  <div class="my-2">
                     <p class="font-weight-bold font-18 font-roboto font-color-prime">
                        Get introduced to your favorites.
                     </p>
                     <p class="font-15 font-roboto">
                        We’ll send a warm intro via email connecting you with interested investors. <br>
                        If an investor passes on you, we'll let you know why.
                     </p>
                  </div>
               </div>
            </div>
            <div style="text-align: center;">
               <button target="_blank" href="https://www.angelfund.ai/login">
               <a style="color: white; text-decoration: none;">Let's get started!</a>
               </button>
            </div>
         </div>
      </div>
      <div class="footer">
         <div>
            <a href="#" class="fa fa-twitter"
               style="font-size: 25px;text-decoration: none;margin-right: 10px;color: gray; border-top 3px solid lightgray;"></a>
            <a href="#" class="fa fa-linkedin" style="
               font-size: 25px;
               text-decoration: none;
               background-color: gray;
               width: 30px;
               color: white;
               "></a>
         </div>
         <p style="font-weight: bold;">
            2375 Zanker Road #250, San Jose, CA 95131
         </p>
         <footer>
            Copyright &copy;2020 Global Angel Fund, Inc.
         </footer>
      </div>
      </div>
      <script src="https://code.jquery.com/jquery-3.3.1.slim.min.js"
         integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo"
         ></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"
         integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1"
         ></script>
      <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"
         integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM"
         ></script>
   </body>
</html>
                """
    CHARSET = "UTF-8"
    client = boto3.client('ses',
                          region_name=AWS_REGION,
                          aws_access_key_id=AWS_ACCESS_KEY,
                          aws_secret_access_key=AWS_ACCESS_VALUE
                          )
    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
        )
    except ClientError as e:
        logger.error(f"common utilities: email confirmation: failed {user_email}")
    else:
        logger.debug(f"common utilities: email confirmation: success {user_email}")