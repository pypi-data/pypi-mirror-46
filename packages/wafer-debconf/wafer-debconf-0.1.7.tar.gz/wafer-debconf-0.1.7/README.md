# Wafer apps for DebConf

This package contains several Django apps used by the DebConf
conference.

## badges - Name tag generation

## bursary - Bursary requests and review

## debconf - Random bits and pieces

## front\_desk - Check-In

## invoices - Paid Attendee Invoicing

## register - Attendee Registration

## volunteers - On-site volunteer wrangling

# Configuration

Uses the following Django settings:

Invoicing:

* `DEBCONF_LOCAL_CURRENCY_RATE`: Decimal. The exchange rate. What does $1 USD buy in local currency.
* `DEBCONF_LOCAL_CURRENCY_SYMBOL`: String. The local currency symbol.
* `DEBCONF_LOCAL_CURRENCY`: String. The local currency code.
* `INVOICE_PREFIX`: String. Prefix to invoice IDs.
* `PAYPAL_DATA`: Dict. PayPal details.

Dates:

* `DEBCONF_BURSARY_DEADLINE`: Date. The date that bursaries need to be submitted by.
* `DEBCONF_CONFERENCE_DINNER_DAY`: Date. The day that has the conference dinner.
* `DEBCONF_CONFIRMATION_DEADLINE`: Date. The date that attendance needs to be confirmed by.
* `DEBCONF_DATES`: List of (Description, Start Date, End Date) for the parts of the conference.
* `VOLUNTEERS_FIRST_DAY`: Date. The first day of volunteering.
* `VOLUNTEERS_LAST_DAY`: Date. The last day of volunteering.

Registration:

* `BURSARIES_CLOSED`: Boolean. Can bursary requests still be submitted.
* `DEBCONF_BREAKFAST`: Boolean. Is DebConf providing breakfast for attendees.
* `DEBCONF_PAID_ACCOMMODATION`: Boolean. Is DebConf providing accommodation for self-paying attendees.
* `DEBCONF_SHOE_SIZES`: List of (Key, Description) for Shoe sizes.
* `DEBCONF_T_SHIRT_SIZES`: List of (Key, Description) for T-Shirt sizes.
* `RECONFIRMATION`: Boolean. Is there a reconfirmation round.

Content:

* `TRACKS_FILE`: String. path to a YAML file with the list of tracks to be loadede into the database
* `TALK_TYPES_FILE`: String. path to a YAML file with the list of talk types to be loaded into the database

Misc:

* `DEBCONF_CITY`: String. The name of the city hosting DebConf.
* `DEBCONF_NAME`: String. The name of the Debconf (e.g. "DebConf XX").
* `DCSCHEDULE_TOKEN`: String. Authentication token for the DCSchedule IRC bot to hit the API.
* `SANDBOX`: Boolean. Is this a development instance or production.
