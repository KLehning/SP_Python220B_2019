# pylint: disable=W0401, W0614, W1203, R0913
"""
Create functionality to add, search, delete, update, and list customers.
"""

import logging
from peewee import *
from customer_model import Customer

LOG_FORMAT = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s %(message)s"
LOG_FILE = 'db.log'

FORMATTER = logging.Formatter(LOG_FORMAT)
FILE_HANDLER = logging.FileHandler(LOG_FILE, mode='w')
FILE_HANDLER.setFormatter(FORMATTER)

CONSOLE_HANDLER = logging.StreamHandler()

CONSOLE_HANDLER.setFormatter(FORMATTER)

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger()
LOGGER.addHandler(FILE_HANDLER)
LOGGER.addHandler(CONSOLE_HANDLER)

def add_customer(customer_id, name, lastname, home_address, phone_number,
                 email_address, status, credit_limit):
    """
    Add a new customer to the sqlite3 database.
    """
    try:
        new_customer = Customer.create(customer_id=customer_id,
                                       name=name,
                                       lastname=lastname,
                                       home_address=home_address,
                                       phone_number=phone_number,
                                       email_address=email_address,
                                       status=status,
                                       credit_limit=credit_limit)
        new_customer.save()
        LOGGER.info(f'Successfully added new customer with id {customer_id} ' +\
                    f'to the database.')
    except TypeError as err:
        LOGGER.info(f'Error creating = {customer_id}')
        LOGGER.info(err)
        raise err

def search_customer(customer_id):
    """
    Return a dictionary object with name, lastname, email address,
    and phone number of a customer or an empty dictionary object if
    no customer was found.
    """
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logging.info(f'Customer with id {customer_id} found! ' +\
                     f'Returning dictionary.')
        return {'name': acustomer.name,
                'lastname': acustomer.lastname,
                'emailaddress': acustomer.email_address,
                'phone_number': acustomer.phone_number}
    except DoesNotExist:
        LOGGER.warning(f'Customer with id {customer_id} could not be found' +\
                       f' in the database.')
        LOGGER.info(DoesNotExist)
        return {}

def delete_customer(customer_id):
    """
    Delete a customer from the database.
    """
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        LOGGER.info(f'Customer with id {customer_id} found. Deleting from ' +\
                    f'the database.')
        acustomer.delete_instance()
    except DoesNotExist:
        LOGGER.warning(f'Customer with id {customer_id} could not be found' +\
                       f' in the database. Deletion unsuccessful.')
        LOGGER.info(DoesNotExist)
        raise ValueError

def update_customer_credit(customer_id, credit_limit):
    """
    Search an existing customer by customer_id and update their credit limit
    """
    try:
        acustomer = Customer.get(Customer.customer_id == customer_id)
        logging.info(f'Customer with id {customer_id} found. Updating ' +\
                     f'credit limit to new value of {credit_limit}.')
        acustomer.credit_limit = credit_limit
        acustomer.save()
    except DoesNotExist:
        LOGGER.warning(f'Customer with id {customer_id} could not be found' +\
                       f' in the database. Credit limit update unsuccessful.')
        raise ValueError

def list_active_customers():
    """
    Return an integer with the number of customers whose status
    is currently active.
    """
    acustomer_count = Customer.select().where(Customer.status).count()
    LOGGER.info(f'This is the number of active customers: {acustomer_count}.')
    return acustomer_count

def list_active_customer_names():
    """
    Return names of active customers
    """
    acustomer_list = Customer.select().where(Customer.status)
    LOGGER.info('Retrieving the active customers in the database.')
    return [cust.name for cust in acustomer_list]

def filter_by_credit(min_credit):
    """
    Return names and the associated customer ID of active customers
    who meet the specified minimum credit limit criteria.
    """
    acustomer_list = Customer.select().where(Customer.status)
    LOGGER.info(f'Retrieving the active customers in the database '+\
                f'who meet the minimum credit criteria.')
    return [f'{cust.name} ({cust.customer_id})' for cust in acustomer_list
            if cust.credit_limit >= min_credit]
