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
#                              INVESTOR WAIT LIST OVER EMAIL TEMPLATE
#<==================================================================================================>
def wait_list_over_inv(user_email, first_name):
    RECIPIENT = [user_email]
    SENDER = CONSTANT.EMAIL_SENDER.value
    AWS_REGION = CONSTANT.EMAIL_REGION.value
    AWS_ACCESS_KEY = CONSTANT.ACCESS_KEY.value
    AWS_ACCESS_VALUE = CONSTANT.ACCESS_VALUE.value
    SUBJECT = f"Welcome to Angelfund.ai, {first_name}!"
    bs = "ok"
    BODY_HTML = f"""
<html>

<head>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" />
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
            font-weight: 700;
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

        .info-container {{
            width: 85% !important;
            padding: 1% 5% !important;
            display: block;
            margin: 10px auto 30px;
            box-shadow: 1px 1px 25px -5px #5e51f4;
            border-radius: 10px;
        }}

        .font-grey {{
            color: #707070 !important;
        }}

        .font-purple {{
            color: #5e51f4 !important;
        }}


        @media only screen and (max-width: 991px) {{
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


<div class="container">
    <div class="logo">
        <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/Icons/Angelfund.ai+Logo.png"
            style="height: 30px; width: 165px;" />
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
            <strong>You’ve made it! You’re off the waitlist!
            </strong> <br>
            We’re thrilled to start introducing you to relevant startups every week on
            Angelfund.ai.
        </p>

        <p class="sizing">
            Here's a quick refresher on how our platform
            works:
        </p>

        <div class="info-container">
            <p class="sizing font-grey">
                <strong>Set your investment preferences.</strong><br>
                You've told us what types of startups you're looking for.
            </p>
            <p class="sizing font-purple">
                <strong>Now, we'll show you relevant deals.</strong><br>
                Spend more time looking at startups you care about.
            </p>
            <p class="sizing font-purple">
                <strong>Get introduced to your favorite startups.</strong><br>
                We'll send a warm intro straight to your inbox.
            </p>
        </div>

        <div style="text-align: center;">

            <a target="_blank" href="https://www.angelfund.ai">
                     <button style=" color: white; text-decoration: none;"">
                View my deals!
                </button>
            </a>
        </div>
    </div>


</div>


<div class="footer">
    <div>
        <a target="_blank" href="https://twitter.com/angelfundAI">
            <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/twitter-512.png" style="
              height: 25px;
              width: 25px;
              text-decoration: none;
              margin-right: 10px;
              color: gray; 
              "></img>
        </a>
        <a target="_blank" href="https://www.linkedin.com/company/angelfundai">
            <img src="https://angelfund-company-images.s3-us-west-1.amazonaws.com/25325.png" style="
              height: 25px;
              width: 25px;
              text-decoration: none;
              color: gray;
              "></img>
        </a>
    </div>
    <p>
        2375 Zanker Road #250, San Jose, CA 95131
    </p>
    <footer>
        Copyright &copy;2020 Global Angel Fund, Inc.
    </footer>
</div>
</div>

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