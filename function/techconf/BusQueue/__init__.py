import logging
import os
from collections import namedtuple
from datetime import datetime

import azure.functions as func
import psycopg2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

attendee = namedtuple('attendee', "first_name email")
notification = namedtuple('notification', 'subject message')


def main(msg: func.ServiceBusMessage):
    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',
                 notification_id)

    try:
        logging.info('Got called!')
        attendees = []
        with psycopg2.connect(os.environ.get('pgdb')) as conn:
            with conn.cursor() as cur:
                stmt = """SELECT first_name, email FROM public.attendee"""
                cur.execute(stmt)
                for record in cur:
                    attendees.append(attendee(*record))

                stmt = f"""SELECT subject, message FROM public.notification WHERE id={notification_id}"""
                cur.execute(stmt)
                result = cur.fetchone()
                notif = notification(*result)

                for person in attendees:
                    subject = '{}: {}'.format(person.first_name, notif.subject)
                    send_email(person.email, subject, notification.message)

                completed_date = datetime.utcnow()
                status = 'Notified {} attendees'.format(len(attendees))
                stmt = f"""UPDATE public.notification 
                           SET completed_date = '{completed_date}', status='{status}'
                           WHERE id={notification_id}"""
                cur.execute(stmt)

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        logging.info('finishing call')


def send_email(email, subject, body):
    if not os.environ.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email='info@techconf.com',
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        sg.send(message)


if __name__ == '__main__':
    main()
